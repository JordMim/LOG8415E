FROM ubuntu:20.04



# --------------------------------------------------------------------------- #
# Common                                                                      #
# --------------------------------------------------------------------------- #

# Directory structure
WORKDIR /root
ENV ROOT_DIR   "/root"
ENV OUTPUT_DIR    "$ROOT_DIR/output"
ENV INPUT_DIR     "$ROOT_DIR/input"
ENV TIME_FILE     "$ROOT_DIR/time.txt"
RUN mkdir $OUTPUT_DIR

# Update package repository
RUN apt update

# Install required packages
RUN apt install -y curl

# Copy input files
COPY input /root/input



# --------------------------------------------------------------------------- #
# Hadoop                                                                      #
# --------------------------------------------------------------------------- #

# Install required packages
ENV DEBIAN_FRONTEND "noninteractive"
RUN apt install -y default-jdk
ENV JAVA_HOME "/usr/lib/jvm/java-11-openjdk-amd64"
ENV PATH "$JAVA_HOME:$PATH"

# Install Hadoop
RUN curl https://dlcdn.apache.org/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz --output hadoop-3.3.4.tar.gz
RUN tar -xf hadoop-3.3.4.tar.gz -C /usr/local/

# Set Hadoop environment variables
ENV HADOOP_HOME "/usr/local/hadoop-3.3.4"
ENV PATH "$HADOOP_HOME/bin:$PATH"
RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Set Hadoop directories
ENV HADOOP_OUTPUT_DIR    "$OUTPUT_DIR/hadoop"

# MapReduce files
ENV HADOOP_MAPREDUCE_EXAMPLES "$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.4.jar"



# --------------------------------------------------------------------------- #
# Spark                                                                       #
# --------------------------------------------------------------------------- #

# Set Spark directories
ENV SPARK_OUTPUT_DIR "$OUTPUT_DIR/spark"
RUN mkdir $SPARK_OUTPUT_DIR



# --------------------------------------------------------------------------- #
# Flask API                                                                   #
# --------------------------------------------------------------------------- #

# Expose Flask port
EXPOSE 80

# Install required packages
RUN apt install -y python3 python3-pip time

# Install Python requirements
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r requirements.txt

# Copy Flask app
COPY app.py /root/app.py
COPY utils.py /root/utils.py
COPY mapreduce_spark.py /root/mapreduce_spark.py
COPY mapreduce_hadoop.py /root/mapreduce_hadoop.py
COPY linux.py /root/linux.py


# --------------------------------------------------------------------------- #
# Linux                                                                       #
# --------------------------------------------------------------------------- #

COPY scripts/linux_wordcount.sh /root/linux_wordcount.sh
ENV LINUX_WORDCOUNT_SCRIPT "$ROOT_DIR/linux_wordcount.sh"
COPY scripts/spark_wordcount.py /root/spark_wordcount.py
ENV SPARK_WORDCOUNT_SCRIPT "$ROOT_DIR/spark_wordcount.py"

# Set Flask app as the running application
ENTRYPOINT python3 ./app.py
