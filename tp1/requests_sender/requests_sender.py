import json, requests, threading, time, logging

BASE_URL = 'http://tp1-1158016110.us-east-1.elb.amazonaws.com'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def call_endpoint_http(url):
    response = requests.get(url)

def thread_1_fct(url):
    for i in range(1000):
        call_endpoint_http(url)
    logging.info('-> Thread 1 ended.')

def thread_2_fct(url):
    for i in range(500):
        call_endpoint_http(url)
    time.sleep(60)
    for i in range(1000):
        call_endpoint_http(url)
    logging.info('-> Thread 2 ended.')

if __name__ == "__main__":

    for cluster in ('cluster1', 'cluster2'):
        logging.info('Sending requests to ' + cluster)
        url = BASE_URL + '/' + cluster
        thread_1 = threading.Thread(target=thread_1_fct, args=(url,))
        thread_2 = threading.Thread(target=thread_2_fct, args=(url,))
        logging.info('-> Running thread 1...')
        thread_1.start()
        logging.info('-> Running thread 2...')
        thread_2.start()
        thread_1.join()
        thread_2.join()
        logging.info('-> Ended.')
