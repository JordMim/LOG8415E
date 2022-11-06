from flask import Flask, request, abort
import logging, subprocess, os, shutil

JAR_DIR = os.environ.get('HADOOP_JAVA_FILES', '')
EXAMPLES_JAR_FILE = os.environ.get('HADOOP_EXAMPLES_JAR_FILE', '')
INPUT_DIR = os.environ.get('HADOOP_INPUT_DIR', '')
OUTPUT_DIR = os.environ.get('HADOOP_OUTPUT_DIR', '')
TIME_OUTPUT = os.environ.get('HADOOP_TIME_OUTPUT', '')
TIME_OUTPUT = os.environ.get('HADOOP_TIME_OUTPUT', '')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Create Flask app
app = Flask(__name__)

# Cluster 1
@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    jar_file = data['jar_file']
    main_class = data['main_class']
    input_file = data['input_file']

    # Mapreduce example file
    if jar_file == 'hadoop-mapreduce-examples.jar':
        jar_file_path = EXAMPLES_JAR_FILE
    
    # Other mapreduce files
    else:
        jar_file_path = os.path.join(JAR_DIR, jar_file)

    # Check if jar file exists
    if not os.path.isfile(jar_file_path):
        abort(404)
    
    # Check if input file exists
    input_file_path = os.path.join(INPUT_DIR, input_file)
    if not os.path.isfile(jar_file_path):
        abort(404)

    # Clear output directory
    if os.path.isdir(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    # Clear time output file
    if os.path.isfile(TIME_OUTPUT):
        os.unlink(TIME_OUTPUT)

    # Running hadoop
    args = ['time', '-v', '-o', TIME_OUTPUT, 'hadoop', 'jar', jar_file_path, main_class, input_file_path, OUTPUT_DIR]
    process = subprocess.run(args, capture_output=True)

    # Read time output
    with open(TIME_OUTPUT) as file:
        time_output = file.read()

    # Return values
    return {
        'time_output': time_output,
        'hadoop_output': process.stderr.decode()
    }

# Ping
@app.route('/ping')
def ping():
    return 'pong'

# Start in production mode
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)