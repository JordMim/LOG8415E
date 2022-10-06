import json, requests, threading, time, logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def call_endpoint_http():
    url = 'http://localhost'
    response = requests.get(url)

def thread_1_fct():
    for i in range(1000):
        call_endpoint_http()
    logging.info('Thread 1 ended.')

def thread_2_fct():
    for i in range(500):
        call_endpoint_http()
    time.sleep(60)
    for i in range(1000):
        call_endpoint_http()
    logging.info('Thread 2 ended.')

if __name__ == "__main__":

    thread_1 = threading.Thread(target=thread_1_fct)
    thread_2 = threading.Thread(target=thread_2_fct)
    logging.info('Running thread 1...')
    thread_1.start()
    logging.info('Running thread 2...')
    thread_2.start()
    thread_1.join()
    thread_2.join()
    logging.info('Program ended.')
