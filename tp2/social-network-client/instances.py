import boto3
from boto3_type_annotations.ec2 import Instance


def retreive_instance() -> Instance:
    '''
    Retreives the first running EC2 instance found.

        Returns:
            instance (Instance): A running EC2 instance

    '''
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        if instance.state['Name'] != 'terminated':
            return instance
    return None