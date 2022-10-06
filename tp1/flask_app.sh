#!/bin/bash
yum update -y
yum install git tmux htop -y
cd ~
git clone https://github.com/JordMim/LOG8415E.git
cd LOG8415E
git pull
cd tp1/flask_app
pip3 install -r requirements.txt
nohup python3 app.py &