import logging, requests, tqdm, random, boto3, instances, json
from typing import List


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Get the AWS instance base url
INSTANCE = instances.retreive_instance()
INSTANCE.load()
DNS_NAME = INSTANCE.public_dns_name
BASE_URL = 'http://' + DNS_NAME


def benchmark(tech_1: str, tech_2: str, dataset: List[str], repeat: int):
    '''
    Runs MapReduce tasks for provided technologies.

        Parameters:
            tech_1 (str):       1st technology to compare ('hadoop', 'spark' or 'linux')
            tech_2 (str):       2nd technology to compare ('hadoop', 'spark' or 'linux')
            tech_2 (List[str]): List of input filenames
            repeat (int):       Number of times to repeat each comparison

        Returns:
            results (dict): The comparison results
    '''
    # Fetch result n number of times, for each technologies, over all input files
    results = {}
    with tqdm.tqdm(total=len(dataset)*2*repeat) as pbar:
        for data in dataset:
            results[data] = {tech_1: [], tech_2: []}
            for i in range(repeat):
                for t in (tech_1, tech_2):
                    resp = requests.get(BASE_URL + '/' + t + '/wordcount/' + data)
                    results[data][t].append(resp.json()['time'])
                    pbar.update(1)

    # Parse the results
    parsed_results = {
        'per_file': {},
        'total': {}
    }
    totals = {tech_1: 0.0, tech_2: 0.0}
    for file in results:
        totals_file = {tech_1: 0.0, tech_2: 0.0}
        for tech in results[file]:
            for test in results[file][tech]:
                totals[tech]      += test['elapsed']
                totals_file[tech] += test['elapsed']
        parsed_results['per_file'][file] = {
            tech_1: { 'average_time': totals_file[tech_1] / repeat },
            tech_2: { 'average_time': totals_file[tech_2]  / repeat }
        }
    parsed_results['total'] = {
        tech_1: { 'average_time': totals[tech_1] / ( repeat * len(dataset) ) },
        tech_2: { 'average_time': totals[tech_2]  / ( repeat * len(dataset) ) }
    }
    return parsed_results



def main():
    '''
    The main function of the bechmarking script.

    This function will execute two comparisons and output rhe results in files.
    The first comparison is Hadoop vs Linux, which runs 10 times with 
    'pg4300.txt' file as input, which means that a total of 20 MapReduce tasks
    are done for thsi comparison.

    The second comparison is Hadoop vs Spark, which runs 3 times for every file
    provided in the dataset (total of 9 files), which means that a total of 
    54 MapReduce task are done for this comparison.

    Files generated by this functions are:
    - hadoop_vs_linux.json
    - hadoop_vs_spark.json
    '''

    # Run Hadoop vs Linux benchmark
    logging.info('HADOOP vs LINUX')
    hadoop_vs_linux = benchmark(
        'hadoop',
        'linux', 
        [
            'pg4300.txt'
        ],
        10
    )
    with open('hadoop_vs_linux.json', 'w') as file:
        file.write(json.dumps(hadoop_vs_linux, indent=4))
    logging.info('Results written to hadoop_vs_linux.json.')

    # Run Hadoop vs Spark benchmark
    logging.info('HADOOP vs SPARK')
    hadoop_vs_spark = benchmark(
        'hadoop',
        'spark', 
        [
            'buchanj-midwinter-00-t.txt',
            'carman-farhorizons-00-t.txt',
            'charlesworth-scene-00-t.txt',
            'cheyneyp-darkbahama-00-t.txt',
            'colby-champlain-00-t.txt',
            'delamare-bumps-00-t.txt',
            'delamare-lucy-00-t.txt',
            'delamare-myfanwy-00-t.txt',
            'delamare-penny-00-t.txt'
        ],
        3
    )
    with open('hadoop_vs_spark.json', 'w') as file:
        file.write(json.dumps(hadoop_vs_spark, indent=4))
    logging.info('Results written to hadoop_vs_spark.json.')



if __name__ == "__main__":
    main()