#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root using sudo .\run.sh"
  exit
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# ------------------------------------------------------------------#
# AWS CONFIGURATION                                                 #
# ------------------------------------------------------------------#

echo ""
echo "=============================================="
echo "|                  LOG8415E                  |"
echo "|                     TP2                    |"
echo "|         2009913 - Jordan Mimeault          |"
echo "|         2018968 - Antoine Lombardo         |"
echo "|         2020511 - Jacob Dupuis             |"
echo "|         2024785 - Alexandre Dufort         |"
echo "=============================================="
echo ""

# Set the workdir
cd "$SCRIPT_DIR"

# Ask for new AWS credentials
read -p "Do you want to enter new AWS credentials? (y/n) " yn
echo ""

case $yn in 
	[yY] ) echo "Please enter your credentials."
        echo "You can find them by executing this command in the AWS CLI online:"
        echo "cat ~/.aws/credentials"
        echo ""
        read -p "AWS Access Key ID: " aws_access_key_id
        read -p "AWS Secret Access Key: " aws_secret_access_key
        read -p "AWS Session Token: " aws_session_token
        # Configure aws
        aws configure set aws_access_key_id $aws_access_key_id
        aws configure set aws_secret_access_key $aws_secret_access_key
        aws configure set aws_session_token $aws_session_token
        aws configure set default.region us-east-1
        echo "AWS configured successfully!"
        echo ""
		;;
	[nN] ) 
        aws_access_key_id=$(aws configure get aws_access_key_id)
        aws_secret_access_key=$(aws configure get aws_secret_access_key)
        aws_session_token=$(aws configure get aws_session_token);;
	* ) echo "Invalid response, please enter 'y' or 'n'"
    exit;;
esac

# Check AWS credentials
echo "Checking your AWS credentials..."
aws_response=$(aws sts get-caller-identity 2>&1 >/dev/null)
if [[ "$aws_response" == *"An error occurred"* ]] || [[ "$aws_response" == *"Unable to locate credentials"* ]]; then
  echo "Invalid AWS credentials. Please enter new ones."
  exit
fi
echo "AWS credentials validated."




# ------------------------------------------------------------------#
# SESSION CONFIGURATION                                             #
# ------------------------------------------------------------------#

echo ""
echo "Please choose one of the options below:"
echo "1. Configure AWS."
echo "2. Run benchmarks."
echo "3. Do everything."
echo ""
read -p "What do you want to do? " selection
echo ""

script_aws=false
script_benchmark=false

case $selection in 
	1 ) script_aws=true;;
    2 ) script_benchmark=true;;
    3 ) script_aws=true
        script_benchmark=true;;
	* ) echo "Invalid response, please retry.";
esac


# ------------------------------------------------------------------#
# SCRIPT: AWS                                                       #
# ------------------------------------------------------------------#

if [ "$script_aws" = true ] ; then
    echo ""
    echo "=============================================="
    echo "|                AWS SETUP                   |"
    echo "=============================================="
    echo ""
    cd "$SCRIPT_DIR"
    cd setup
    echo "Installing requirements..."
    pip3 install -r requirements.txt 2>&1 >/dev/null
    echo "Starting AWS setup..."
    python3 main.py
    ret=$?
    if [ $ret -ne 0 ]; then
        echo "AWS setup exited with error code $ret"
        exit
    fi
fi





# ------------------------------------------------------------------#
# SCRIPT: BENCHMARK                                                 #
# ------------------------------------------------------------------#

if [ "$script_benchmark" = true ] ; then
    echo ""
    echo "=============================================="
    echo "|                BENCHMARK                   |"
    echo "=============================================="
    echo ""
    cd "$SCRIPT_DIR"
    cd benchmark
    echo "Installing requirements..."
    pip3 install -r requirements.txt 2>&1 >/dev/null
    echo "Starting Benchmark..."
    python3 benchmark.py
    ret=$?
    if [ $ret -ne 0 ]; then
        echo "Benchmark exited with error code $ret"
        exit
    fi
fi





# ------------------------------------------------------------------#
# SCRIPT: METRICS RETRIEVER                                         #
# ------------------------------------------------------------------#

if [ "$script_metrics" = true ] ; then
    echo ""
    echo "=============================================="
    echo "|            METRICS RETRIEVER               |"
    echo "=============================================="
    echo ""
    # if we just sent the request, we should wait one minute for the metrics to appear
    if [ "$script_requests" = true ] ; then
        echo "Waiting 1 minute before retrieving metrics..."
        sleep 60
    fi
    cd "$SCRIPT_DIR"
    cd metrics
    echo "Installing requirements..."
    pip3 install -r requirements.txt 2>&1 >/dev/null
    echo "Starting metrics retriever..."
    python3 main.py
    ret=$?
    if [ $ret -ne 0 ]; then
        echo "Metrics resolver exited with error code $ret"
        exit
    fi

fi