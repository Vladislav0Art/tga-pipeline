package org.plan.research.tga.core.tool

import java.nio.file.Path
import kotlin.time.Duration

interface TestGenerationTool {
    val name: String

    fun init(
        root: Path,
        classPath: List<Path>,
    )

    fun run(target: String, timeLimit: Duration, outputDirectory: Path)

    fun report(): TestSuite
}
