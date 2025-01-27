import argparse
import os
import subprocess
import logging


TGA_PIPELINE_HOME = "/home/ubuntu/research-work-2024/tga-pipeline"


common_config = {
    "benchmarksPath": "/home/ubuntu/research-work-2024/evaluation/benchmark/benchmarks",
    "benchmarksPatchedPath": "/home/ubuntu/research-work-2024/evaluation/benchmark/benchmarks/benchmarks.json",
    "tool": "TestSpark",
    "threads": 2,
}



# CUT + 5 iterations
# rq1_config1 = [
#     # GPT-4
#     {
#         "name": "GPT-4",
#         "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/GPT-4/config-I",
#     },
#     # Llama-70B
#     {
#         "name": "Llama-70B",
#         "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-70B-Instruct/config-I",
#     },
#     # Llama-8B
#     {
#         "name": "Llama-8B",
#         "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-8B-Instruct/config-I",
#     },
#     # Llama-3B
#     {
#         "name": "Llama-3B",
#         "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-3B-Instruct/config-I",
#     },
#     # Llama-1B
#     {
#         "name": "Llama-1B",
#         "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-1B-Instruct/config-I",
#     },
# ]


# CUT + 1 iterations
# rq1_config2 = [
#     # GPT-4
#     {
#         "name": "GPT-4",
#         "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/GPT-4/config-II",
#     },
#     # Llama-70B
#     {
#         "name": "Llama-70B",
#         "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-70B-Instruct/config-II",
#     },
#     # Llama-8B
#     {
#         "name": "Llama-8B",
#         "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-8B-Instruct/config-II",
#     },
#     # Llama-3B
#     {
#         "name": "Llama-3B",
#         "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-3B-Instruct/config-II",
#     },
#     # Llama-1B
#     {
#         "name": "Llama-1B",
#         "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-1B-Instruct/config-II",
#     },
# ]


# METHODS_DECLARATION + 5 iterations
rq2_config1 = [
    # GPT-4
    # {
    #     "name": "GPT-4",
    #     "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/GPT-4",
    # },
    # # Llama-70B
    # {
    #     "name": "Llama-70B",
    #     "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-31-70B-Instruct",
    # },
    # # Llama-8B
    # {
    #     "name": "Llama-8B",
    #     "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-31-8B-Instruct",
    # },
    # Llama-3B
    {
        "name": "Llama-3B",
        "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-32-3B-Instruct",
    },
    # # Llama-1B
    # {
    #     "name": "Llama-1B",
    #     "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-32-1B-Instruct",
    # },
]





# Old solution (obsolete)
# config = {
#     # tool's name will be attached to this path
#     # /home/ubuntu/research-work-2024/evaluation/configurations/RQ1/Llama-31-70B-Instruct/configuration-I/local/
#     # /home/ubuntu/research-work-2024/headless-out/test
#     # "/home/ubuntu/research-work-2024/evaluation/configurations/RQ2/GPT-4/configuration-I/test",
#     "resultsPath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-31-70B-Instruct",
#     "benchmarksPath": "/home/ubuntu/research-work-2024/evaluation/benchmark/benchmarks",
#     "benchmarksPatchedPath": "/home/ubuntu/research-work-2024/evaluation/benchmark/benchmarks/benchmarks.json",
#     "tool": "TestSpark",
#     "threads": 2,
# }


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



def main():
    """
    Execute the generated tests for every model from configs
    and collect line and branch coverage statistics, and compilation rate, and mutation score,
    storing it into a CSV file under `resultsPath/[tool]`.
    """
    for model_config in rq2_config1:
        config = { **common_config, **model_config }

        logging.info(f"==== Running analysis evaluation for '{model_config['name']}' ====")

        logging.info('Starting analysis evaluation...')
        logging.info(f"resultsPath: {config['resultsPath']}")
        logging.info(f"benchmarksPath: {config['benchmarksPath']}")
        logging.info(f"benchmarksPatchedPath: {config['benchmarksPatchedPath']}")
        logging.info(f"threads: {config['threads']}")
        logging.info(f"tool: {config['tool']}")

        execute_analysis(config)
        logging.info(f"==== Analysis evaluation for '{model_config['name']}' finished ====")



if __name__ == '__main__':
    main()