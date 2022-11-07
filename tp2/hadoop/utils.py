import os, shutil
from flask import abort
from datetime import datetime, timedelta

def verify_file(filepath):
    if os.path.isfile(filepath):
        return os.path.normpath(filepath)
    else:
        abort(404)

def verify_dir(dirpath):
    if os.path.isdir(dirpath):
        return os.path.normpath(dirpath)
    else:
        abort(404)

def delete_dir(dirpath):
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

def delete_file(filepath):
    if os.path.isfile(filepath):
        os.unlink(filepath)

def read_file(filepath):
    if os.path.isfile(filepath):
        with open(filepath) as file:
            return file.read()
    else:
        return None

def parse_time_output(raw_output):
    output = {}
    for line in raw_output.split('\n'):
        for word in line.split(' '):
            if 'user' in word:
                output['user'] = float(word.replace('user', ''))
            elif 'system' in word:
                output['system'] = float(word.replace('system', ''))
            elif 'elapsed' in word:
                t = datetime.strptime(word.replace('elapsed', ''),"%M:%S.%f")
                d = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
                output['elapsed'] = d.total_seconds()
            elif '%CPU' in word:
                output['cpu_usage'] = float(word.replace('%CPU', ''))
    return output