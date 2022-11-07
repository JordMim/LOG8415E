import logging, requests, instances, json

INSTANCE = instances.retreive_instance()
INSTANCE.load()
DNS_NAME = INSTANCE.public_dns_name
BASE_URL = 'http://' + DNS_NAME

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

users = [
    924, 
    8941, 
    8942,
    9019, 
    9020, 
    9021, 
    9022, 
    9990, 
    9992, 
    9993
]

logging.info('Starting Hadoop MapReduce job...')
resp = requests.get(BASE_URL + '/hadoop/socialnetwork/soc-LiveJournal1Adj.txt', timeout=60*10)
logging.info('Processing results...')
recommendations = resp.json()['recommendations']
report = {}
for user in recommendations:
    if int(user) in users:
        report[user] = recommendations[user]
with open('output_all.json', 'w') as file:
    file.write(json.dumps(recommendations, indent=4))
with open('output_report.json', 'w') as file:
    file.write(json.dumps(report, indent=4))
logging.info('Results written to output_all.json and output_report.json')
