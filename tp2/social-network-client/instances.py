import boto3
from boto3_type_annotations.ec2 import Instance


def retreive_instance() -> Instance:
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        if instance.state['Name'] != 'terminated':
            return instance
    return None