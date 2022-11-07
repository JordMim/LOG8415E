import pyspark, sys

input_file  = sys.argv[1]
output_dir = sys.argv[2]
context = pyspark.SparkContext('local', 'TP2 - Word Count')
context.setLogLevel('ERROR')
words = context.textFile(input_file).flatMap(lambda line: line.split(" "))
word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)
word_counts.saveAsTextFile(output_dir)