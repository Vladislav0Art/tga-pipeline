package org.plan.research.tga.tool.kex

import org.plan.research.tga.core.dependency.Dependency
import org.plan.research.tga.core.tool.TestGenerationTool
import org.plan.research.tga.core.tool.TestSuite
import org.plan.research.tga.core.util.javaString
import org.vorpal.research.kthelper.assert.unreachable
import org.vorpal.research.kthelper.buildProcess
import org.vorpal.research.kthelper.logging.log
import org.vorpal.research.kthelper.terminateOrKill
import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import kotlin.io.path.exists
import kotlin.streams.toList
import kotlin.time.Duration
import kotlin.time.Duration.Companion.milliseconds


class KexCliTool(private val args: List<String>) : TestGenerationTool {
    override val name = "kex"

    companion object {
        private val KEX_HOME = Paths.get(System.getenv("KEX_HOME"))
            ?: unreachable { log.error("No \$KEX_HOME environment variable") }
    }

    private lateinit var classPath: List<Path>
    private lateinit var outputDirectory: Path

    override fun init(root: Path, classPath: List<Path>) {
        this.classPath = classPath
    }

    override fun run(target: String, timeLimit: Duration, outputDirectory: Path) {
        this.outputDirectory = outputDirectory
        var process: Process? = null
        try {
            process = buildProcess(
                "python3",
                "${KEX_HOME.resolve("kex.py")}",
                "--classpath", classPath.joinToString(File.pathSeparator!!),
                "--target", target,
                "--mode", "concolic",
                "--output", outputDirectory.toString(),
                "--option", "concolic:timeLimit:${timeLimit.inWholeSeconds}",
                "--option", "kex:computeCoverage:false",
                *args.toTypedArray()
            ) {
                redirectOutput(ProcessBuilder.Redirect.DISCARD)
                redirectError(ProcessBuilder.Redirect.DISCARD)
                log.debug("Starting Kex with command: {}", command())
            }
            process.waitFor()
        } catch (e: InterruptedException) {
            log.error("Kex was interrupted on target $target")
        } finally {
            process?.terminateOrKill(attempts = 10U, waitTime = 500.milliseconds)
        }
    }

    override fun report(): TestSuite {
        val testSrcPath = outputDirectory.resolve("tests")
        val javaFiles = when {
            testSrcPath.exists() -> Files.walk(testSrcPath).filter { it.fileName.toString().endsWith(".java") }
                .map { testSrcPath.relativize(it).toString().javaString.removeSuffix(".java") }
                .toList()

            else -> emptyList()
        }
        val testSources = javaFiles.filterNot { it.endsWith("Utils") }
        val testDependencies = javaFiles.filter { it.endsWith("Utils") }
        return TestSuite(
            testSrcPath,
            testSources,
            testDependencies,
            listOf(
                Dependency("junit", "junit", "4.13.2"),
                Dependency("org.mockito", "mockito-core", "4.11.0"),
            )
        )
    }
}
