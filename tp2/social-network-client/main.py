import logging, requests, instances, json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Get the AWS instance base url
INSTANCE = instances.retreive_instance()
INSTANCE.load()
DNS_NAME = INSTANCE.public_dns_name
BASE_URL = 'http://' + DNS_NAME

# List of all users recomendations requested for the report
REPORT_USERS = [
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

# The file to be used as input file for the MapReduce
INPUT_FILE = 'soc-LiveJournal1Adj.txt'



def main():
    '''
    The main function of the social network client script.
    
    This function will execute the Social Network MapReduce on the AWS 
    container using the file "soc-LiveJournal1Adj.txt" as input, wait for the
    execution to end, then will process the returned values and save the output
    in JSON and raw formats.
    '''

    # Run Hadoop request to the AWS instance
    logging.info('Starting Hadoop MapReduce job...')
    resp = requests.get(BASE_URL + '/hadoop/socialnetwork/' + INPUT_FILE, timeout=60*10)

    # Process instance response
    logging.info('Processing results...')
    recommendations = resp.json()['recommendations']
    raw_recommendations = resp.json()['raw_recommendations']
    report = {}
    for user in recommendations:
        if int(user) in REPORT_USERS:
            report[user] = recommendations[user]

    # Save results to files
    with open('output_all.json', 'w') as file:
        file.write(json.dumps(recommendations, indent=4))
    logging.info('All recommendations written to output_all.json.')
    with open('output_report.json', 'w') as file:
        file.write(json.dumps(report, indent=4))
    logging.info('Report recommendations written to output_report.json.')
    with open('output_raw.txt', 'w') as file:
        file.write(raw_recommendations)
    logging.info('Raw recommendations written to output_raw.txt')



if __name__ == "__main__":
    main()