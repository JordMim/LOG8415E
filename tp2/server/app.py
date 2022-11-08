import flask, logging, mapreduce_hadoop, mapreduce_spark, linux

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Create Flask app
app = flask.Flask(__name__)


@app.route('/hadoop/wordcount/<input>', methods=['GET'])
def hadoop_wordcount(input: str):
    '''
    The /hadoop/wordcount/<input> route implementation.

    This runs a Hadoop WordCount task and returns the results of it.

        Parameters:
            input (str): The input file to use as input for the task.
    '''
    return mapreduce_hadoop.word_count(input)


@app.route('/hadoop/socialnetwork/<input>', methods=['GET'])
def hadoop_social_network(input: str):
    '''
    The /hadoop/socialnetwork/<input> route implementation.

    This runs a Hadoop SocialNetwork task and returns the results of it.

        Parameters:
            input (str): The input file to use as input for the task.
    '''
    return mapreduce_hadoop.social_network(input)


@app.route('/spark/wordcount/<input>', methods=['GET'])
def spark_wordcount(input: str):
    '''
    The /spark/wordcount/<input> route implementation.

    This runs a Spark WordCount task and returns the results of it.

        Parameters:
            input (str): The input file to use as input for the task.
    '''
    return mapreduce_spark.word_count(input)


@app.route('/linux/wordcount/<input>', methods=['GET'])
def linux_wordcount(input: str):
    '''
    The /linux/wordcount/<input> route implementation.

    This runs a Linux WordCount task and returns the results of it.

        Parameters:
            input (str): The input file to use as input for the task.
    '''
    return linux.word_count(input)


@app.route('/ping')
def ping():
    '''
    The /ping route implementation.

    This simply returns 'pong', indicating that the server is up and running.
    '''

    return 'pong'

# Start in production mode
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)