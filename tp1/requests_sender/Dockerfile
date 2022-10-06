FROM python:3.10-buster
COPY requests_sender.py requests_sender.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD [ "python",  "./requests_sender.py" ]