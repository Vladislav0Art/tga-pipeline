plugins {
    id("org.plan.research.tga-pipeline-base")
}

dependencies {
    api(project(":tga-core"))
}


task<JavaExec>("run") {
    classpath = sourceSets["main"].runtimeClasspath
    mainClass.set("org.plan.research.tga.tool.MainKt")
}

//tasks.register<Wrapper>("wrapper") {
//    gradleVersion = "7.2"
//}

tasks.register("prepareKotlinBuildScriptModel"){}
