import flask, logging, mapreduce_hadoop, mapreduce_spark, linux

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Create Flask app
app = flask.Flask(__name__)

# Hadoop: Word Count
@app.route('/hadoop/wordcount/<input>', methods=['GET'])
def hadoop_wordcount(input: str):
    return mapreduce_hadoop.word_count(input)

# Hadoop: Social Network
@app.route('/hadoop/socialnetwork/<input>', methods=['GET'])
def hadoop_social_network(input: str):
    return mapreduce_hadoop.social_network(input)

# Spark: Word Count
@app.route('/spark/wordcount/<input>', methods=['GET'])
def spark_wordcount(input: str):
    return mapreduce_spark.word_count(input)

# Linux: Word Count
@app.route('/linux/wordcount/<input>', methods=['GET'])
def linux_wordcount(input: str):
    return linux.word_count(input)



# Ping
@app.route('/ping')
def ping():
    return 'pong'

# Start in production mode
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)