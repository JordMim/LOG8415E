import os, shutil
from flask import abort
from datetime import datetime, timedelta


def verify_file(filepath):
    '''
    Verifies if a file exists and return its normalized path.

        Parameters:
            filepath (str): The file path

        Returns:
            filepath (str): The normalized file path

        Throws:
            a 404 error if file does not exist
    '''
    if os.path.isfile(filepath):
        return os.path.normpath(filepath)
    else:
        abort(404)


def verify_dir(dirpath):
    '''
    Verifies if a directory exists and return its normalized path.

        Parameters:
            dirpath (str): The directory path

        Returns:
            dirpath (str): The normalized directory path
            
        Throws:
            a 404 error if the directory does not exist
    '''
    if os.path.isdir(dirpath):
        return os.path.normpath(dirpath)
    else:
        abort(404)


def delete_dir(dirpath):
    '''
    Deletes a directory and all of its content.

        Parameters:
            dirpath (str): The directory path
    '''
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)


def delete_file(filepath):
    '''
    Deletes a file.

        Parameters:
            filepath (str): The file path
    '''
    if os.path.isfile(filepath):
        os.unlink(filepath)


def read_file(filepath):
    '''
    Reads a file content.

        Parameters:
            filepath (str): The file path
        
        Returns:
            content (str): The file content, or None if the file does not exist
    '''
    if os.path.isfile(filepath):
        with open(filepath) as file:
            return file.read()
    else:
        return None


def parse_time_output(raw_output):
    '''
    Parse the output of the time command.

        Parameters:
            raw_output (str): The raw output of the time command
        
        Returns:
            output (dict): The formatted output
    '''
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