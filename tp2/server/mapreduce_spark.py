import os, datetime, utils, subprocess, ast


INPUT_DIR        =  os.environ.get('INPUT_DIR', '')
OUTPUT_DIR       = os.environ.get('SPARK_OUTPUT_DIR', '')
TIME_FILE        = os.environ.get('TIME_FILE', '')
WORDCOUNT_SCRIPT = os.environ.get('SPARK_WORDCOUNT_SCRIPT', '')


def word_count(input: str):
    '''
    The Spark WordCount wrapper function.

    This runs a Spark WordCount task and returns the results of it.

        Parameters:
            input (str): The input file to use as input for the task.
        Returns:
            results (dict): The time and data output of the task.
    '''

    # Set the base variables
    time_file         = TIME_FILE
    input_file        = os.path.join(INPUT_DIR, input)
    output_dir        = os.path.join(OUTPUT_DIR, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    wordcount_script  = utils.verify_file(WORDCOUNT_SCRIPT)

    # Delete the old time file
    utils.delete_file(time_file)

    # Run Hadoop
    args = ['time', '-o', TIME_FILE, 'python3', wordcount_script, input_file, output_dir]
    process = subprocess.run(args, capture_output=True)

    # Process output
    output_raw = utils.read_file(output_dir + '/part-00000')
    output = {}
    for line in output_raw.split('\n'):
        try:
            word_count = ast.literal_eval(line)
            output[str(word_count[0])] = int(word_count[1])
        except:
            pass
    
    return {
        'time': utils.parse_time_output(utils.read_file(time_file)),
        'wordcount': output
    }