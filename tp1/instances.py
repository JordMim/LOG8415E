import boto3, os
from boto3_type_annotations.ec2 import Client, ServiceResource

USER_DATA_SCRIPT_FILE = 'instance_user_data.txt'
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, USER_DATA_SCRIPT_FILE)) as file:
    USER_DATA_SCRIPT = file.read()

def create_instance(ec2: ServiceResource, tag, instance_type):

    ec2.create_instances(
        ImageId='ami-026b57f3c383c2eec',
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        UserData=USER_DATA_SCRIPT,
        KeyName='vockey'
    )