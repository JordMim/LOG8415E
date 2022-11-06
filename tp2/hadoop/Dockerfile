FROM ubuntu:20.04
EXPOSE 80

WORKDIR /root

# ENVIRONMENT
ENV DEBIAN_FRONTEND "noninteractive"
ENV JAVA_HOME "/usr/lib/jvm/java-11-openjdk-amd64"
ENV HADOOP_HOME "/usr/local/hadoop-3.3.4"
ENV HADOOP_EXAMPLES_JAR_FILE "$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.4.jar"
ENV PATH "$JAVA_HOME:$PATH"
ENV PATH "$HADOOP_HOME/bin:$PATH"

# PACKAGES
RUN apt update
RUN apt install -y default-jdk
RUN apt install -y curl 
RUN apt install -y python3 
RUN apt install -y python3-pip 
RUN apt install -y time

# Input files
ENV HADOOP_INPUT_DIR "/root/input"
RUN mkdir $HADOOP_INPUT_DIR
RUN curl https://www.gutenberg.org/cache/epub/4300/pg4300.txt --output $HADOOP_INPUT_DIR/pg4300.txt

# Output directory
ENV HADOOP_OUTPUT_DIR "/root/output"
RUN mkdir $HADOOP_OUTPUT_DIR

# Time output file
ENV HADOOP_TIME_OUTPUT "/root/time.txt"

# HADOOP Installation
RUN curl https://dlcdn.apache.org/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz --output hadoop-3.3.4.tar.gz
RUN tar -xf hadoop-3.3.4.tar.gz -C /usr/local/
RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Flask app
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r requirements.txt
COPY app.py /root/app.py

ENTRYPOINT python3 ./app.py
