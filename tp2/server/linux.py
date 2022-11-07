import os, utils, subprocess


INPUT_DIR  = os.environ.get('INPUT_DIR', '')
TIME_FILE  = os.environ.get('TIME_FILE', '')
WORDCOUNT_SCRIPT = os.environ.get('LINUX_WORDCOUNT_SCRIPT', '')


def word_count(input: str):

	# Set the base variables
    time_file         = TIME_FILE
    input_file        = utils.verify_file(os.path.join(INPUT_DIR, input))
    wordcount_script  = utils.verify_file(WORDCOUNT_SCRIPT)

	# Delete the old time file
    utils.delete_file(time_file)

    # Run Hadoop
    args = ['time', '-o', TIME_FILE, wordcount_script, input_file]
    process = subprocess.run(args, capture_output=True)

    # Process output
    output_raw = process.stdout.decode(encoding='windows-1252')
    output = {}
    for line in output_raw.split('\n'):
        # Remove spaces each sides
        line = line.strip()
        # Split with spaces
        line = line.split(' ')
        # Extract word and count
        if len(line) == 2 and int(line[0]) > 0:
            output[str(line[1])] = int(line[0])

	# Return values
    return {
		'time': utils.parse_time_output(utils.read_file(time_file)),
		'wordcount': output
	}
