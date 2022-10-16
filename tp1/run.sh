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
aws configure set aws_access_key_id ASIAT2AXJQQWOVMNIAXK
aws configure set aws_secret_access_key npq1jXl/NEvs6ImbNXmqDZ76tax5JX2jLlxvmv6a
aws configure set aws_session_token FwoGZXIvYXdzED8aDI3GOfW2mtMO+q8RFCLDATX/YD2n8fw29xzaNRySeIBMSlCvySLsAO5jEZXSuT8LAz2B3nSzukKtMV+9V0UXexQcKqfG8Tj2Y3s8XQmgCnzJ40Cj/cl7s4S8Xggyi34wY2VxKZFynP3ADyL/5UaCJIQsz09OQcoJ38vHssTJe1dPZY2EaMCvHfLHiSu2DmF2F4QIR17wejBf4J1AoGw98Fa1V1yGU1+YRV2DqFW43kmVY1qyl3jhgdQvaokKeeRuIbsBzwYikYv211WWGQouoeKguijD7LGaBjItFyeGo0T0LRPDnnL9R2T5ffXH15h18rJ6e8X1Zbw7JX8WHpzNnBHzBGZtCp6A
aws configure set default.region us-east-1

# Launch main script
python3 main.py