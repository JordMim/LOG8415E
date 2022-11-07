
from time import sleep
from typing import List
import boto3
import logging
from boto3_type_annotations.elbv2 import Client as elbv2Client
from boto3_type_annotations.ec2 import ServiceResource as ec2ServiceResource
from boto3_type_annotations.ec2 import Instance
import security_groups, instances, load_balancers, vpcs, subnets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

SECURITY_GROUP_NAME = 'tp2'
INSTANCE_INFOS = [
    {'type': 'm4.large', 'zone': 'us-east-1a'}
]

ec2: ec2ServiceResource = boto3.resource('ec2')

elbv2: elbv2Client = boto3.client('elbv2')

# Retrieve default Vpc
vpc = vpcs.get_default_vpc(ec2)

# Retrieve subnets
subnets_list = subnets.get_subnets(ec2)

# Delete all old objects
instances.delete_all_instances(ec2)
security_groups.delete_security_group(ec2, SECURITY_GROUP_NAME)

# Create the security group
security_group = security_groups.create_security_group(ec2, SECURITY_GROUP_NAME)
security_group = security_groups.get_security_group(ec2, 'tp2')

# Create the instance
instance = instances.create_instance(ec2, 'm4.large', 'us-east-1a', security_group)

# Wait for instance to be running
instances.wait_for_running(instance)

# Wait for instance to be up
instances.wait_for_ping(instance)

# Get instance DNS name
logging.info('Instance public DNS: ' + instance.public_dns_name)

exit(0)