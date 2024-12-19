import argparse
import os
import subprocess
import logging


TGA_PIPELINE_HOME = "/home/ubuntu/research-work-2024/tga-pipeline"

config = {
    # tool's name will be attached to this path
    # /home/ubuntu/research-work-2024/evaluation/configurations/RQ1/Llama-31-70B-Instruct/configuration-I/local/
    "resultsPath": "/home/ubuntu/research-work-2024/headless-out/test",
    "benchmarksPath": "/home/ubuntu/research-work-2024/evaluation/benchmark/benchmarks",
    "benchmarksPatchedPath": "/home/ubuntu/research-work-2024/evaluation/benchmark/benchmarks/benchmarks.json",
    "tool": "TestSpark",
    "threads": 2,
}


# Configure logging to output both to a file and to STDOUT
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(name)s - %(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler("run_analysis.log"),
        logging.StreamHandler(),
    ]
)


def execute_analysis(config):
    results_path = config['resultsPath']
    benchmarks_path = config['benchmarksPath']
    benchmarks_patched_path = config['benchmarksPatchedPath']
    threads = config['threads']
    tool = config['tool']

    analysis_args = [
        f"--args=--resultsPath {results_path} --benchmarksPath {benchmarks_path} --benchmarksPatchedPath {benchmarks_patched_path} --threads {threads} --tool {tool}",
    ]

    analysis_command = ["./gradlew", ":tga-analysis:run"] + analysis_args
    logging.info(f"Execute analysis command: '{' '.join(analysis_command)}'")

    # NOTE: setting tga-pipeline home into ENV
    os.environ['TGA_PIPELINE_HOME'] = TGA_PIPELINE_HOME

    analysis_process = subprocess.Popen(
        analysis_command,
        cwd=TGA_PIPELINE_HOME,
        env=os.environ
    )

    analysis_stdout, analysis_stderr = analysis_process.communicate()

    if analysis_stdout:
        logging.info(f"Runner stdout: {analysis_stdout.decode('utf-8')}")
    if analysis_stderr:
        logging.error(f"Runner stderr: {analysis_stderr.decode('utf-8')}")



if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Run analysis evaluation with specified parameters.')
    # parser.add_argument('--runs', type=str, required=True, help='Runs to execute (see tga-pipeline\'s format).')
    # args = parser.parse_args()

    logging.info('Starting analysis evaluation...')
    logging.info(f"resultsPath: {config['resultsPath']}")
    logging.info(f"benchmarksPath: {config['benchmarksPath']}")
    logging.info(f"benchmarksPatchedPath: {config['benchmarksPatchedPath']}")
    logging.info(f"threads: {config['threads']}")
    logging.info(f"tool: {config['tool']}")

    execute_analysis(config)