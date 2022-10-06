#!/bin/bash
yum update -y
yum install git tmux htop -y
cd ~
git clone https://github.com/JordMim/LOG8415E.git
cd LOG8415E
git pull
cd tp1/flask_app
pip3 install -r requirements.txt
tmux kill-session -t flask
tmux new-session -d -s flask
tmux send-keys 'sudo python3 app.py' C-m
tmux detach -s flask