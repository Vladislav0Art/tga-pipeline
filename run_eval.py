import argparse
import os
import subprocess
import logging


TGA_PIPELINE_HOME = "/home/ubuntu/research-work-2024/tga-pipeline"
TEST_SPARK_HOME = "/home/ubuntu/research-work-2024/TestSpark"
TOOL = 'TestSpark'

RUNNER_HOST = 'localhost'
RUNNER_PORT = 8000

configs = [
    dict({
        'model': 'Code-Llama-70B-Instruct',
        'output': '/home/ubuntu/research-work-2024/evaluation/configurations/RQ1/Llama-31-70B-Instruct/configuration-II/local',
    }),
    dict({
        'model': 'Llama-3-8B-Instruct',
        'output': '/home/ubuntu/research-work-2024/evaluation/configurations/RQ1/Llama-31-8B-Instruct/configuration-II/local',
    }),
    dict({
        'model': 'llama3.2', # Llama3.2-3B
        'output': '/home/ubuntu/research-work-2024/evaluation/configurations/RQ1/Llama-32-3B-Instruct/configuration-II/local',
    }),
    dict({
        'model': 'llama3.2:1b', # Llama3.2-1B
        'output': '/home/ubuntu/research-work-2024/evaluation/configurations/RQ1/Llama-32-1B-Instruct/configuration-II/local',
    }),
]


# Configure logging to output both to a file and to STDOUT
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(name)s - %(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler("run_eval.log"),
        logging.StreamHandler(),
    ]
)


def execute_pipeline_for_config(args):
    os.environ['TGA_PIPELINE_HOME'] = TGA_PIPELINE_HOME
    os.environ['TEST_SPARK_HOME'] = TEST_SPARK_HOME

    benchmarks_config = args['config']
    port = args['port']
    run_name = args['runName']
    runs = args['runs']
    timeout = args['timeout']

    host = args['host']
    tool = args['tool']
    llm_token = args['llmToken']
    space_user = args['spaceUser']
    space_token = args['spaceToken']


    for config in configs:
        model, output = config['model'], config['output']

        logging.info(f"Model: {model}; output: '{output}'")

        # TODO: you stop a wrong process! it should be TestSpark, not runner
        logging.info("Stopping gradle deamons...")
        subprocess.Popen(
            ['./gradlew', '--stop'],
            cwd=TGA_PIPELINE_HOME,
        ).wait()
        logging.info("Gradle deamons stopped successfully.")

        # runner
        runner_args = [
            f"--args=--config {benchmarks_config} --output {output} --port {port} --runName {run_name} --runs {runs} --timeout {timeout}"
        ]
        runner_command = ['./gradlew', ':tga-runner:run'] + runner_args

        logging.info(f"Execute runner command: {' '.join(runner_command)}")
        runner_process = subprocess.Popen(
            runner_command,
            cwd=TGA_PIPELINE_HOME,
            env=os.environ
        )

        # tool
        tool_args = [
            f"--args=-i {host} -p {port} -t {tool} --toolArgs '--llm {model} --llmToken {llm_token} --spaceUser {space_user} --spaceToken {space_token}'"
        ]
        tool_command = ['./gradlew', ':tga-tool:run'] + tool_args

        logging.info(f"Execute tool command: {' '.join(tool_command)}")
        tool_process = subprocess.Popen(
            tool_command,
            cwd=TGA_PIPELINE_HOME,
            env=os.environ
        )
        runner_stdout, runner_stderr = runner_process.communicate()
        tool_stdout, tool_stderr = tool_process.communicate()

        if runner_stdout:
            logging.info(f"Runner stdout: {runner_stdout.decode('utf-8')}")
        if runner_stderr:
            logging.error(f"Runner stderr: {runner_stderr.decode('utf-8')}")

        if tool_stdout:
            logging.info(f"Tool stdout: {tool_stdout.decode('utf-8')}")
        if tool_stderr:
            logging.error(f"Tool stderr: {tool_stderr.decode('utf-8')}")



def execute_pipeline(args):
    os.environ['TGA_PIPELINE_HOME'] = TGA_PIPELINE_HOME
    os.environ['TEST_SPARK_HOME'] = TEST_SPARK_HOME

    for run in range(args['runs']):
        logging.info(f"Run {run + 1}/{args['runs']}")

        logging.info("Stopping gradle deamons...")
        subprocess.Popen(
            ['./gradlew', '--stop'],
            cwd=TGA_PIPELINE_HOME,
        ).wait()
        logging.info("Gradle deamons stopped successfully.")

        # runner
        runner_args = [
            f"--args=--config {args['config']} --output {args['output']} --port {args['port']} --runName {args['runName']} --runs {run} --timeout {args['timeout']}"
        ]
        runner_command = ['./gradlew', ':tga-runner:run'] + runner_args

        logging.info(f"Execute runner command: {' '.join(runner_command)}")
        runner_process = subprocess.Popen(
            runner_command,
            cwd=TGA_PIPELINE_HOME,
            env=os.environ
        )


        # tool
        tool_args = [
            f"--args=-i {args['host']} -p {args['port']} -t {args['tool']} --toolArgs '--llm {args['llm']} --llmToken {args['llmToken']} --spaceUser {args['spaceUser']} --spaceToken {args['spaceToken']}'"
        ]
        tool_command = ['./gradlew', ':tga-tool:run'] + tool_args

        logging.info(f"Execute tool command: {' '.join(tool_command)}")
        tool_process = subprocess.Popen(
            tool_command,
            cwd=TGA_PIPELINE_HOME,
            env=os.environ
        )
        runner_stdout, runner_stderr = runner_process.communicate()
        tool_stdout, tool_stderr = tool_process.communicate()

        if runner_stdout:
            logging.info(f"Runner stdout: {runner_stdout.decode('utf-8')}")
        if runner_stderr:
            logging.error(f"Runner stderr: {runner_stderr.decode('utf-8')}")

        if tool_stdout:
            logging.info(f"Tool stdout: {tool_stdout.decode('utf-8')}")
        if tool_stderr:
            logging.error(f"Tool stderr: {tool_stderr.decode('utf-8')}")


def main():
    parser = argparse.ArgumentParser(description='Run evaluation with specified parameters.')
    parser.add_argument('--runs', type=str, required=True, help='Runs to execute (see tga-pipeline\'s format).')
    # parser.add_argument('--model', type=str, required=True, help='AI model name')
    # parser.add_argument('--output', type=str, required=True, help='Output file path')
    parser.add_argument('--llmToken', type=str, required=True, help='LLM token')
    parser.add_argument('--spaceUser', type=str, required=True, help='Space username')
    parser.add_argument('--spaceToken', type=str, required=True, help='Space token')
    parser.add_argument('--benchmarks_filepath', type=str, required=True, help='Path to benchmarks file')
    parser.add_argument('--timeout', type=int, required=True, help='Timeout in seconds')

    args = parser.parse_args()

    logging.info(f'Runs: {args.runs}')
    # logging.info(f'Model: {args.model}')
    # logging.info(f'Output: {args.output}')
    logging.info(f'Space User: {args.spaceUser}')
    logging.info(f'Benchmarks Filepath: {args.benchmarks_filepath}')
    logging.info(f'Timeout: {args.timeout}')

    pipeline_args = {
        'config': args.benchmarks_filepath,
        # 'output': args.output,
        # 'llm': args.model,
        'host': RUNNER_HOST,
        'port': RUNNER_PORT,
        'runName': 'run',
        'runs': args.runs,
        'timeout': args.timeout,
        'tool': TOOL,
        'llmToken': args.llmToken,
        'spaceUser': args.spaceUser,
        'spaceToken': args.spaceToken,
    }

    execute_pipeline_for_config(args=pipeline_args)

    # execute_pipeline(args=pipeline_args)


if __name__ == '__main__':
    main()