import boto3
from boto3_type_annotations.ec2 import ServiceResource
from instances import *
import security_groups

SECURITY_GROUP_NAME = 'tp1'

ec2: ServiceResource = boto3.resource('ec2')

# Create the security group
security_groups.delete_security_group(ec2, SECURITY_GROUP_NAME)
security_group = security_groups.create_security_group(ec2, SECURITY_GROUP_NAME)

# Create an instance



