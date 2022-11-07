import logging, requests, tqdm, random, boto3, instances

INSTANCE = instances.retreive_instance()
INSTANCE.load()
DNS_NAME = INSTANCE.public_dns_name
BASE_URL = 'http://' + DNS_NAME

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def benchmark(tech_1, tech_2, dataset, repeat):
    results = {}
    with tqdm.tqdm(total=len(dataset)*2*repeat) as pbar:
        for data in dataset:
            results[data] = {tech_1: [], tech_2: []}
            for i in range(repeat):
                for t in (tech_1, tech_2):
                    resp = requests.get(BASE_URL + '/' + t + '/wordcount/' + data)
                    results[data][t].append(resp.json()['time'])
                    pbar.update(1)
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

logging.info('HADOOP vs LINUX')
hadoop_vs_linux = benchmark(
    'hadoop',
    'linux', 
    [
        'pg4300.txt'
    ],
    10
)
print(hadoop_vs_linux)

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
print(hadoop_vs_spark)