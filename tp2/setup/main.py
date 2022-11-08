
import boto3
import logging
from boto3_type_annotations.ec2 import ServiceResource as ec2ServiceResource
import security_groups, instances, vpcs, subnets


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Infos about what needs to be created
SECURITY_GROUP_NAME = 'tp2'
INSTANCE_INFOS = [
    {'type': 'm4.large', 'zone': 'us-east-1a'}
]



def main():
    '''
    The main function of the setup script.

    This function will setup the entire AWS envrionment and wait for the
    created instance to start answering to pings, meaning that the Docker
    container is up and running.
    '''
    ec2: ec2ServiceResource = boto3.resource('ec2')

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


if __name__ == "__main__":
    main()