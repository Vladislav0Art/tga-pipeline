package org.plan.research.tga.runner.coverage.jacoco

import org.plan.research.tga.core.benchmark.Benchmark
import org.plan.research.tga.core.coverage.BranchId
import org.plan.research.tga.core.coverage.ClassCoverageInfo
import org.plan.research.tga.core.coverage.ClassId
import org.plan.research.tga.core.coverage.CoverageProvider
import org.plan.research.tga.core.coverage.ExtendedCoverageInfo
import org.plan.research.tga.core.coverage.InstructionId
import org.plan.research.tga.core.coverage.LineId
import org.plan.research.tga.core.coverage.MethodCoverageInfo
import org.plan.research.tga.core.coverage.MethodId
import org.plan.research.tga.core.dependency.DependencyManager
import org.plan.research.tga.core.tool.TestSuite
import org.plan.research.tga.core.util.TGA_PIPELINE_HOME
import org.plan.research.tga.runner.compiler.SystemJavaCompiler
import org.vorpal.research.kthelper.assert.ktassert
import org.vorpal.research.kthelper.collection.mapToArray
import org.vorpal.research.kthelper.deleteOnExit
import org.vorpal.research.kthelper.executeProcess
import org.vorpal.research.kthelper.logging.error
import org.vorpal.research.kthelper.logging.log
import org.vorpal.research.kthelper.resolve
import org.w3c.dom.Document
import org.w3c.dom.Element
import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import javax.xml.parsers.DocumentBuilderFactory
import kotlin.io.path.exists


class JacocoCliCoverageProvider(
    private val dependencyManager: DependencyManager
) : CoverageProvider {
    private val tgaTempDir = Files.createTempDirectory("tga-runner").also {
        deleteOnExit(it)
    }.toAbsolutePath()
    private val compiledDir: Path = tgaTempDir.resolve("compiled").toAbsolutePath().also {
        it.toFile().mkdirs()
    }

    companion object {
        private val JACOCO_CLI_PATH = TGA_PIPELINE_HOME.resolve("lib").resolve("jacococli.jar")
        private val JACOCO_AGENT_PATH = TGA_PIPELINE_HOME.resolve("lib").resolve("jacocoagent.jar")
    }


    override fun computeCoverage(benchmark: Benchmark, testSuite: TestSuite): ClassCoverageInfo {
        log.debug("Computing coverage: compiledDir='{}'", compiledDir)

        // set of sources containing both test cases and the test suite
        val allTests = testSuite.tests.associateWith { testSuite.testSrcPath.resolve(it.asmString + ".java") }
        // set of sources containing the single test suite
        val testSuiteOnly = if (testSuite.testSuiteQualifiedName.isNotEmpty()) {
            testSuite.testSuiteQualifiedName.let { testSuiteName ->
                listOf(testSuiteName).associateWith { testSuite.testSrcPath.resolve(it.asmString + ".java") }
            }
        } else {
            null
        }
        // set of sources containing only test cases without the test suite
        val testCasesOnly = if (testSuite.testCasesOnly.isNotEmpty()) {
            testSuite.testCasesOnly.associateWith { testSuite.testSrcPath.resolve(it.asmString + ".java") }
        } else {
            null
        }

        /**
         * Provide up to three sets of source files suitable for compilation and
         * try to collect coverage for at least one of them since all 3 represent
         * the same coverage set:
         * 1. All the compilable test cases and the test suite (test suite contains only compilable test cases).
         * 2. All the compilable test cases alone.
         * 3. The test suite alone.
         */
        val compilationAttempts = mutableListOf(allTests)
        testSuiteOnly?.also { compilationAttempts.add(it) }
        testCasesOnly?.also { compilationAttempts.add(it) }

        val classPath = benchmark.classPath + testSuite.dependencies.flatMap { dependencyManager.findDependency(it) }
        val compiler = SystemJavaCompiler(classPath)

        var selectedTestSet: Map<String, Path> = emptyMap()

        for ((index, attempt) in compilationAttempts.withIndex()) {
            log.debug(
                "Attempting to compile {}-th set of tests: [\n{}\n\t]",
                index,
                attempt.keys.joinToString(separator = "\n") { "\t\t$it," },
            )

            try {
                val result = compiler.compile(attempt.values.toList(), compiledDir)
                selectedTestSet = attempt
                log.debug("Compilation succeeded with result: {}", result)
                break
            } catch (e: Throwable) {
                log.error(e)
                // TODO: should compiledDir be cleaned up before next attempt?
            }
        }


        val pkg = benchmark.klass.substringBeforeLast('.')
        val name = benchmark.klass.substringAfterLast('.')
        val fullTestCP = listOf(*classPath.toTypedArray(), compiledDir)
        val execFiles = mutableListOf<Path>()

        for ((testName, _) in selectedTestSet) {
            val execFile = testSuite.testSrcPath.resolve("$testName.exec")
            executeProcess(
                "java",
                "-cp",
                fullTestCP.joinToString(separator = File.pathSeparator),
                "-javaagent:${JACOCO_AGENT_PATH.toAbsolutePath()}=destfile=${execFile.toAbsolutePath()}",
                "org.junit.runner.JUnitCore",
                testName,
            )
            execFiles.add(execFile)
        }

        val xmlCoverageReport = testSuite.testSrcPath.resolve("coverage.xml")
        executeProcess(
            "java",
            "-jar",
            JACOCO_CLI_PATH.toString(),
            "report",
            *execFiles.mapToArray { it.toString() },
            "--classfiles",
            "${benchmark.bin.resolve(*pkg.split('.').toTypedArray(), "$name.class")}",
            "--sourcefiles",
            "${benchmark.src.resolve(*pkg.split('.').toTypedArray(), "$name.java")}",
            "--xml",
            xmlCoverageReport.toString(),
        )

        return parseCoverageXml(benchmark, xmlCoverageReport)
    }

    @Suppress("UNUSED_VARIABLE")
    private fun parseCoverageXml(benchmark: Benchmark, path: Path): ClassCoverageInfo {
        if (!path.exists()) return ClassCoverageInfo(ClassId(benchmark.klass), emptySet())
        val pkg = benchmark.klass.substringBeforeLast('.')
        val name = benchmark.klass.substringAfterLast('.')

        val builder = DocumentBuilderFactory.newInstance().also {
            it.isValidating = false
            it.isNamespaceAware = true
            it.setFeature("http://xml.org/sax/features/namespaces", false)
            it.setFeature("http://xml.org/sax/features/validation", false)
            it.setFeature("http://apache.org/xml/features/nonvalidating/load-dtd-grammar", false)
            it.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false)
        }.newDocumentBuilder()
        val doc = builder.parse(path.toFile())
        doc.documentElement.normalize()

        val reportElement = doc.getElementByTag("report", 0)
        val packageElement = reportElement.getElementByTag("package", 0)
        ktassert(packageElement.getAttribute("name") == pkg.replace('.', '/'))
        val classElement = packageElement.getElementByTag("class", 0)
        ktassert(classElement.getAttribute("name") == benchmark.klass.replace('.', '/'))

        val methodBounds = classElement.getAllElementsByTag("method").map { methodElement ->
            val methodName = methodElement.getAttribute("name")
            val methodDescriptor = methodElement.getAttribute("desc")
            val startLine = methodElement.getAttribute("line").toInt()
            val length = methodElement.getAllElementsByTag("counter").first { it.getAttribute("type") == "LINE" }.let {
                val missed = it.getAttribute("missed").toInt()
                val covered = it.getAttribute("covered").toInt()
                missed + covered
            }
            Triple(MethodId(methodName, methodDescriptor), startLine, length)
        }.sortedBy { it.second }

        val sourceFileElement = packageElement.getElementByTag("sourcefile", 0)
        val sourceFileName = sourceFileElement.getAttribute("name")
        ktassert(sourceFileName == classElement.getAttribute("sourcefilename"))

        var length = -1
        var index = 0
        var lines = mutableMapOf<LineId, Boolean>()
        var instructions = mutableMapOf<InstructionId, Boolean>()
        var branches = mutableMapOf<BranchId, Boolean>()

        val methodCoverages = mutableSetOf<MethodCoverageInfo>()
        for (lineElement in sourceFileElement.getAllElementsByTag("line").sortedBy { it.getAttribute("nr").toInt() }) {
            val lineNumber = lineElement.getAttribute("nr").toInt()
            if (lineNumber == methodBounds[index].second) {
                length = 0
            }
            if (length < 0) continue

            val missedInstructions = lineElement.getAttribute("mi").toInt()
            val coveredInstructions = lineElement.getAttribute("ci").toInt()
            val totalInstructions = missedInstructions + coveredInstructions
            val missedBranches = lineElement.getAttribute("mb").toInt()
            val coveredBranches = lineElement.getAttribute("cb").toInt()
            val totalBranches = missedBranches + coveredBranches

            if (totalInstructions == 0) continue
            val lineId = LineId(sourceFileName, lineNumber.toUInt())
            lines[lineId] = (coveredInstructions > 0)

            for (inst in 0 until totalInstructions) {
                val id = InstructionId(lineId, inst.toUInt())
                instructions[id] = (inst < coveredInstructions)
            }

            for (branch in 0 until totalBranches) {
                val id = BranchId(lineId, branch.toUInt())
                branches[id] = (branch < coveredBranches)
            }
            ++length

            if (length == methodBounds[index].third) {
                methodCoverages += MethodCoverageInfo(
                    methodBounds[index].first,
                    ExtendedCoverageInfo(instructions),
                    ExtendedCoverageInfo(lines),
                    ExtendedCoverageInfo(branches),
                )
                instructions = mutableMapOf()
                lines = mutableMapOf()
                branches = mutableMapOf()
                length = -1
                ++index
            }
        }

        return ClassCoverageInfo(ClassId(benchmark.klass), methodCoverages)
    }

    private fun Document.getElementByTag(name: String, index: Int): Element =
        this.getElementsByTagName(name).item(index) as Element

    private fun Element.getElementByTag(name: String, index: Int): Element =
        this.getElementsByTagName(name).item(index) as Element

    private fun Element.getAllElementsByTag(name: String): Iterable<Element> {
        val elements = this.getElementsByTagName(name)
        return (0 until elements.length).map { elements.item(it) as Element }
    }
}