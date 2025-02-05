import argparse
import logging
from dataclasses import dataclass
from typing import List, Union
import os
import csv


# set to True to read the arguments from the command line. See the `parse_arguments` function below
READ_FROM_CLI = False



# CUT + 5 iterations
# rq1_config1 = [
    # # GPT-4
    # {
    #     "model": "GPT-4",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/GPT-4/config-I/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/GPT-4/config-I/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "gpt4-RQ1-CUT-5-iter",
    # },
    # # Llama-31-70B-Instruct
    # {
    #     "model": "Llama-31-70B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-70B-Instruct/config-I/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-70B-Instruct/config-I/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama70b-RQ1-CUT-5-iter",
    # },
    # # Llama-31-8B-Instruct
    # {
    #     "model": "Llama-31-8B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-8B-Instruct/config-I/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-8B-Instruct/config-I/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama8b-RQ1-CUT-5-iter",
    # },
    # Llama-32-3B-Instruct
    # {
    #     "model": "Llama-32-3B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-3B-Instruct/config-I/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-3B-Instruct/config-I/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama3b-RQ1-CUT-5-iter",
    # },
    # # Llama-32-1B-Instruct
    # {
    #     "model": "Llama-32-1B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-1B-Instruct/config-I/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-1B-Instruct/config-I/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama1b-RQ1-CUT-5-iter",
    # },
# ]



# CUT + 1 iteration
rq1_config2 = [
    # # GPT-4
    # {
    #     "model": "GPT-4",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/GPT-4/config-II/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/GPT-4/config-II/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "gpt4-RQ1-CUT-1-iter",
    # },
    # # Llama-31-70B-Instruct
    # {
    #     "model": "Llama-31-70B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-70B-Instruct/config-II/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-70B-Instruct/config-II/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama70b-RQ1-CUT-1-iter",
    # },
    # Llama-31-8B-Instruct
    # {
    #     "model": "Llama-31-8B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-8B-Instruct/config-II/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-31-8B-Instruct/config-II/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama8b-RQ1-CUT-1-iter",
    # },
    # # Llama-32-3B-Instruct
    {
        "model": "Llama-32-3B-Instruct",
        "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-3B-Instruct/config-II/TestSpark",
        "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-3B-Instruct/config-II/TestSpark/results.csv",
        "format": "reduced",
        "prompt_id": "llama3b-RQ1-CUT-1-iter",
    },
    # # Llama-32-1B-Instruct
    # {
    #     "model": "Llama-32-1B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-1B-Instruct/config-II/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ1/Llama-32-1B-Instruct/config-II/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama1b-RQ1-CUT-1-iter",
    # },
]




# METHODS_DECLARATION + 5 iterations
# rq2_config1 = [
    # GPT-4
    # {
    #     "model": "GPT-4",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/GPT-4/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/GPT-4/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "gpt4-RQ2",
    # },
    # Llama-31-70B-Instruct
    # {
    #     "model": "Llama-31-70B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-31-70B-Instruct/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-31-70B-Instruct/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama70b-RQ2",
    # },
    # # Llama-31-8B-Instruct
    # {
    #     "model": "Llama-31-8B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-31-8B-Instruct/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-31-8B-Instruct/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama8b-RQ2",
    # },
    # # Llama-32-3B-Instruct
    # {
    #     "model": "Llama-32-3B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-32-3B-Instruct/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-32-3B-Instruct/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama3b-RQ2",
    # },
    # Llama-32-1B-Instruct
    # {
    #     "model": "Llama-32-1B-Instruct",
    #     "project_filepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-32-1B-Instruct/TestSpark",
    #     "savefilepath": "/home/ubuntu/research-work-2024/evaluation/final/configurations/RQ2/Llama-32-1B-Instruct/TestSpark/results.csv",
    #     "format": "reduced",
    #     "prompt_id": "llama1b-RQ2",
    # },
# ]


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(name)s - %(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler("transform_csv.log"),
        logging.StreamHandler(),
    ]
)


TGA_PIPELINE_CSV_HEADER = "tool,runName,iteration,buildId,klass,compilationRateNumerator,compilationRateDenominator,compilationRatePercent,linesCovered,linesTotal,lineCoveragePercent,branchesCovered,branchesTotal,branchCoveragePercent,mutationScoreNumerator,mutationScoreDenominator,mutationScorePercent,benchmarkProperties"

REDUCED_CSV_HEADER = "build_id,cut_quialified_name,iteration,prompt_id,lines_covered,lines_total,branches_covered,branches_total,compilable_test_cases,total_test_cases"


@dataclass
class MetricsCollection:
    # compilation metric
    compilation_rate_numerator: int
    compilation_rate_denominator: int
    compilation_rate_percent: float

    # line coverage metric
    lines_covered: int
    lines_total: int
    line_coverage_percent: float

    # branch coverage metric
    branches_covered: int
    branches_total: int
    branch_coverage_percent: float

    # mutation score metric
    mutation_score_numerator: int
    mutation_score_denominator: int
    mutation_score_percent: float

    benchmark_properties: str | None



@dataclass
class ExecutationStatistics:
    tool: str
    runName: str
    iteration: int
    build_id: str
    klass: str # qualified name of a class
    metrics: MetricsCollection



def collect_iterations_executation_data(project_filepath: str) -> List[ExecutationStatistics]:
    f"""
    Assembles generated runtime statistics from the CSV files generated by tga-pipeline's
    coverage collection module. The expected columns of these CSV files are as follows:
    ```
    {TGA_PIPELINE_CSV_HEADER}
    ```

    Returns a list of `ExecutationStatistics` instances that represent the runtime statistics of a single iteration.
    """
    statistics: List[ExecutationStatistics] = []

    for dir_name in os.listdir(project_filepath):
        dir_path = os.path.join(project_filepath, dir_name)

        if os.path.isdir(dir_path):
            # expecting the directory name to be in the format of 'runName-iteration'
            parts = dir_name.split('-')
            if len(parts) != 2:
                logging.warning(f"Skipping directory '{dir_name}' as it does not match the expected format 'runName-iteration'")
                continue

            run_name, iteration = parts
            # locate the CSV file with the runtime statistics
            csv_filename = f"TestSpark-{run_name}-{iteration}.csv"
            csv_filepath = os.path.join(dir_path, csv_filename)

            if os.path.exists(csv_filepath):
                logging.info(f"CSV file for '{run_name}-{iteration}' successfully located")
                logging.info(f"Reading CSV file '{csv_filepath}'")

                with open(csv_filepath, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)

                    logging.info(f"Assuming a header row is present. Skipping it...")
                    logging.info(f"The header row skipped")

                    count = 0
                    # reader starts directly from the data rows, skipping the header row
                    for row in reader:
                        count += 1

                        metrics = MetricsCollection(
                            compilation_rate_numerator=int(row['compilationRateNumerator']),
                            compilation_rate_denominator=int(row['compilationRateDenominator']),
                            compilation_rate_percent=float(row['compilationRatePercent']),

                            lines_covered=int(row['linesCovered']),
                            lines_total=int(row['linesTotal']),
                            line_coverage_percent=float(row['lineCoveragePercent']),

                            branches_covered=int(row['branchesCovered']),
                            branches_total=int(row['branchesTotal']),
                            branch_coverage_percent=float(row['branchCoveragePercent']),

                            mutation_score_numerator=int(row['mutationScoreNumerator']),
                            mutation_score_denominator=int(row['mutationScoreDenominator']),
                            mutation_score_percent=float(row['mutationScorePercent']),

                            benchmark_properties=row['benchmarkProperties'] if row['benchmarkProperties'] else None
                        )

                        stat = ExecutationStatistics(
                            tool=row['tool'],
                            runName=row['runName'],
                            iteration=int(row['iteration']),
                            build_id=row['buildId'],
                            klass=row['klass'],

                            metrics=metrics
                        )

                        statistics.append(stat)
                        logging.info(f"The row '{stat.build_id}:{stat.klass}:{stat.runName}-{stat.iteration}' processed")

                    logging.info(f"CSV file '{csv_filepath}' successfully processed. {count} rows read")
            else:
                logging.warning(f"File '{csv_filepath}' not found. Ensure the CSV file name conforms to the `TestSpark-[runName]-[iteration].csv` format. Skipping...")

    return statistics



def collect_and_transform_csv_files(config):
    project_filepath = config['project_filepath']
    savefilepath = config['savefilepath']
    format = config['format']
    prompt_id = config['prompt_id']

    available_formats = ['tga-pipeline', 'reduced']
    if format not in available_formats:
        raise ValueError(f"Invalid format '{format}', one of {available_formats} expected")

    if format == 'reduced' and prompt_id is None:
        raise ValueError(f"The 'prompt_id' argument is required for the 'reduced' format, got {prompt_id}")

    logging.info("Project filepath: '%s'", project_filepath)
    logging.info("Save filepath: '%s'", savefilepath)
    logging.info("Selected format: '%s'", format)

    # collect the runtime statistics from all iterations of the provided configuration
    statistics: List[ExecutationStatistics] = collect_iterations_executation_data(project_filepath)

    statistics.sort(key=lambda stat: (stat.build_id, stat.iteration))

    # write the collected statistics into a single CSV file
    with open(savefilepath, 'w') as savefile:
        if format == 'tga-pipeline':
            savefile.write(f"{TGA_PIPELINE_CSV_HEADER}\n")

            for stat in statistics:
                metrics: MetricsCollection = stat.metrics

                entry = ",".join(map(str, [
                    stat.tool,
                    stat.runName,
                    stat.iteration,
                    stat.build_id,
                    stat.klass,

                    # metrics
                    # compilation rate
                    metrics.compilation_rate_numerator,
                    metrics.compilation_rate_denominator,
                    metrics.compilation_rate_percent,
                    # line coverage
                    metrics.lines_covered,
                    metrics.lines_total,
                    metrics.line_coverage_percent,
                    # branch coverage
                    metrics.branches_covered,
                    metrics.branches_total,
                    metrics.branch_coverage_percent,
                    # mutation score
                    metrics.mutation_score_numerator,
                    metrics.mutation_score_denominator,
                    metrics.mutation_score_percent,

                    metrics.benchmark_properties if (metrics.benchmark_properties is not None) else "",
                ]))

                savefile.write(f"{entry}\n")
                logging.info(f"Entry '{stat.build_id}:{stat.klass}:{stat.runName}-{stat.iteration}' saved")

        elif format == 'reduced':
            savefile.write(f"{REDUCED_CSV_HEADER}\n")

            for stat in statistics:
                metrics: MetricsCollection = stat.metrics

                entry = ",".join(map(str, [
                    stat.build_id,
                    # TODO: rename, there is a typo 'quialified'
                    stat.klass, # cut_quialified_name
                    stat.iteration,
                    prompt_id,

                    # metrics
                    # line coverage
                    metrics.lines_covered,
                    metrics.lines_total,
                    # branch coverage
                    metrics.branches_covered,
                    metrics.branches_total,
                    # compilation rate
                    metrics.compilation_rate_numerator, # compilable_test_cases
                    metrics.compilation_rate_denominator, # total_test_cases
                ]))

                savefile.write(f"{entry}\n")
                logging.info(f"Entry '{stat.build_id}:{stat.klass}:{stat.runName}-{stat.iteration}' saved")

    logging.info("All statistics are saved into '%s'", savefilepath)


def main():
    if READ_FROM_CLI is True:
        description = """
        Transforms a set of CSV files generated by the pipeline's coverage collection module,
        and stored in a single generation configuration, into a single CSV file with one of
        the available CSV formats:

        I. The first format matches the format of the input CSV files, which is:
        ```
        tool,runName,iteration,buildId,klass,compilationRateNumerator,compilationRateDenominator,compilationRatePercent,linesCovered,linesTotal,lineCoveragePercent,branchesCovered,branchesTotal,branchCoveragePercent,mutationScoreNumerator,mutationScoreDenominator,mutationScorePercent,benchmarkProperties
        ```

        II. The second format has the following columns:
        ```
        build_id,cut_quialified_name,iteration,prompt_id,lines_covered,lines_total,branches_covered,branches_total,compilable_test_cases,total_test_cases
        ```

        In other words, the script combines all per-iteration artifacts with runtime execution data into a single file.
        """

        def parse_arguments():
            parser = argparse.ArgumentParser(description=description)
            parser.add_argument('project_filepath', type=str, help='The directory path with the iterations of generation, should include the `TestSpark` suffix, e.g. `configuration-1/RQ2/GPT-4/TestSpark -> contains iterations`')

            parser.add_argument('savefilepath', type=str, help='Where to save the resulting CSV file. The file content will be overwritten if it already exists.')
            parser.add_argument('format', type=str, choices=['tga-pipeline', 'reduced'], help='The format of the resulting CSV file', default='tga-pipeline')
            parser.add_argument('prompt_id', type=Union[str, None], help='An identifier or a name of the prompt used for test generation. Only needed for the reduced format. Default is None', default=None)

            return parser.parse_args()

        args = parse_arguments()

        config = {
            "project_filepath": args.project_filepath,
            "savefilepath": args.savefilepath,
            "format": args.format,
            "prompt_id": args.prompt_id,
        }

        logging.info(f"Processing configuration: {config}")
        collect_and_transform_csv_files(config)

    else:
        """
        Configs should be of the following format:
        ```
            {
                "project_filepath": "path/to/TestSpark/execution/iterations" (include 'TestSpark' suffix!),
                "savefilepath": "save/location/for/resulting/csv",
                "format": "reduced" | "tga-pipeline",
                "prompt_id": "" | None (required when format is 'reduced'),
            }
        ```
        """
        for config in rq1_config2:
            logging.info(f"Processing configuration: {config}")
            collect_and_transform_csv_files(config)



if __name__ == '__main__':
    main()