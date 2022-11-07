import os, utils, subprocess, re


INPUT_DIR  = os.environ.get('INPUT_DIR', '')
OUTPUT_DIR = os.environ.get('HADOOP_OUTPUT_DIR', '')
TIME_FILE  = os.environ.get('TIME_FILE', '')


def word_count(input: str):

	# Set the base variables
	examples_jar_file = utils.verify_file(os.environ.get('HADOOP_MAPREDUCE_EXAMPLES', ''))
	mapreduce_class   = 'wordcount'
	time_file         = TIME_FILE
	input_file        = utils.verify_file(os.path.join(INPUT_DIR, input))
	output_dir        = OUTPUT_DIR

	# Delete the output directory if it exists
	utils.delete_dir(output_dir)

	# Delete the old time file
	utils.delete_file(time_file)

	# Run Hadoop
	args = ['time', '-o', TIME_FILE, 'hadoop', 'jar', examples_jar_file, mapreduce_class, input_file, output_dir]
	process = subprocess.run(args, capture_output=True)

	# Process output
	output_raw = utils.read_file(os.path.join(OUTPUT_DIR, 'part-r-00000'))
	output = {}
	for line in output_raw.split('\n'):
		# Remove spaces each sides
		line = line.strip()
		# Split with spaces
		line = line.split('\t')
		# Extract word and count
		if len(line) == 2 and int(line[1]) > 0:
			output[str(line[0])] = int(line[1])

	# Return values
	return {
		'time': utils.parse_time_output(utils.read_file(time_file)),
		'wordcount': output,
		'stdout': process.stderr.decode(),
	}

def social_network(input: str):

	# Set the base variables
	social_network_jar_file = utils.verify_file(os.environ.get('HADOOP_MAPREDUCE_SOCIAL_NETWORK', ''))
	mapreduce_class   = 'SocialNetwork'
	time_file         = TIME_FILE
	input_file        = utils.verify_file(os.path.join(INPUT_DIR, input))
	output_dir        = OUTPUT_DIR

	# Delete the output directory if it exists
	utils.delete_dir(output_dir)

	# Delete the old time file
	utils.delete_file(time_file)

	# Run Hadoop
	args = ['time', '-o', TIME_FILE, 'hadoop', 'jar', social_network_jar_file, mapreduce_class, input_file, output_dir]
	process = subprocess.run(args, capture_output=True)

	# Process output
	output_raw = utils.read_file(os.path.join(OUTPUT_DIR, 'part-r-00000'))
	output = {}
	for line in output_raw.split('\n'):
		# Remove spaces each sides
		line = line.strip()
		# Split with spaces
		line = line.split('\t')
		# Extract word and count
		if len(line) == 2:
			recommendations_str = ','.split(line[1])
			recommendations = []
			for recommendation in recommendations_str:
				recommendations.append(int(recommendation))
			output[int(line[0])] = recommendations
		elif len(line) == 2:
			output[int(line[0])] = []

	# Return values
	return {
		'time': utils.parse_time_output(utils.read_file(time_file)),
		'recommendations': output,
		'stdout': process.stderr.decode(),
	}