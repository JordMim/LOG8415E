#!/bin/bash

# Set the workdir
cd "$(dirname "$0")"

# Ask for AWS credentials
echo "Please enter your credentials."
echo "You can find them by executing this command in the AWS CLI online:"
echo "cat ~/.aws/credentials"
echo AWS Access Key ID:
#read aws_access_key_id
echo AWS Secret Access Key:
#read aws_secret_access_key
echo AWS Session Token:
#read aws_session_token

aws_access_key_id=ASIAT2AXJQQWILQRVGIJ
aws_secret_access_key=fr3DrFKypdhPe19OU9viF0Gvc6dV/aLO8C+
aws_session_token=FwoGZXIvYXdzEDsaDGXkpLYZcSlmZj+JwSLDAesxfKHN4YvghUJYsJ09rI4TgAT3arPwiL+1vKBdBZd5aVuQeyBA5Ld+aCJM55GPNlU+pgP7B9glZFZEAywSe7ZOooU58QQJ2Frz6/6A4S4AQpFaJX9ZDmkjTAl597haCUeEbTStmRltVOZQtd5YqoXqgbBb0D59UMK2pCAO4hOT3od7HHH9aptk4us9JBHtuF7syHlU7GhQT1F1B5KVMSzlLC3QCumuTEA4vOamwoTYUsCjKPtIO5oNZSZFshM3nWML0Si/+LCaBjItfrKqUGneYbBwrNZnF9K4sxiNdlgHlQ42SEG09dqqa2G6cK9Thi6xRKB+qkB0
aws_region=us-east-1

# Configure aws
aws configure set aws_access_key_id ASIAT2AXJQQWILQRVGIJ
aws configure set aws_secret_access_key fr3DrFKypdhPe19OU9viF0Gvc6dV/aLO8C+NKYY4
aws configure set aws_session_token FwoGZXIvYXdzEDsaDGXkpLYZcSlmZj+JwSLDAesxfKHN4YvghUJYsJ09rI4TgAT3arPwiL+1vKBdBZd5aVuQeyBA5Ld+aCJM55GPNlU+pgP7B9glZFZEAywSe7ZOooU58QQJ2Frz6/6A4S4AQpFaJX9ZDmkjTAl597haCUeEbTStmRltVOZQtd5YqoXqgbBb0D59UMK2pCAO4hOT3od7HHH9aptk4us9JBHtuF7syHlU7GhQT1F1B5KVMSzlLC3QCumuTEA4vOamwoTYUsCjKPtIO5oNZSZFshM3nWML0Si/+LCaBjItfrKqUGneYbBwrNZnF9K4sxiNdlgHlQ42SEG09dqqa2G6cK9Thi6xRKB+qkB0
aws configure set default.region us-east-1

# Launch main script
python3 main.py