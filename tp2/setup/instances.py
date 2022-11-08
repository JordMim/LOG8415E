import os, logging, requests, time
from typing import List
from boto3_type_annotations.ec2 import ServiceResource, SecurityGroup, Instance


# Read the user_data file
USER_DATA_SCRIPT_FILE = 'instance_user_data.txt'
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, USER_DATA_SCRIPT_FILE)) as file:
    USER_DATA_SCRIPT = file.read()


def delete_all_instances(ec2: ServiceResource):
    '''
    Deletes all running instances

        Parameters:
            ec2 (ServiceResource): The EC2 service resource object
    '''

    logging.info('Terminating all instances...')
    for instance in ec2.instances.all():
        if instance.state['Name'] != 'terminated':
            instance.terminate()
    for instance in ec2.instances.all():
        if instance.state['Name'] != 'terminated':
            instance.wait_until_terminated()
            logging.info('  {}: Terminated.'.format(instance.id))


def create_instance(ec2: ServiceResource, instance_type: str, availability_zone: str, security_group: SecurityGroup) -> Instance:
    '''
    Creates an instance

        Parameters:
            ec2 (ServiceResource):          The EC2 service resource object
            instance_type (str):            The instance type     (ex. 'm4.large')
            availability_zone (str):        The availability zone (ex. 'us-east-1a')
            security_group (SecurityGroup): The security group to be applied to the instance
        
        Returns:
            instance (Instance): The created instance
    '''

    logging.info(f'Creating an "{instance_type}" instance in zone "{availability_zone}"...')
    instance: Instance = ec2.create_instances(
        ImageId='ami-026b57f3c383c2eec',
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        UserData=USER_DATA_SCRIPT,
        KeyName='vockey',
        Placement={
            'AvailabilityZone': availability_zone,
        },
        SecurityGroupIds=[security_group.id]
    )[0]
    return instance


def wait_for_running(instance: Instance):
    '''
    Waits for an instance to be running.

        Parameters:
            instance (Instance): The instance to wait for
    '''

    logging.info('Waiting for the instance to be running...')
    instance.wait_until_running()
    logging.info('  {}: Running.'.format(instance.id))


def wait_for_ping(instance: Instance):
    '''
    Waits for an instance to start answering to the /ping route.

        Parameters:
            instance (Instance): The instance to wait for
    '''
    logging.info('Waiting for the instance to respond to pings...')
    instance.load()
    dns_name = instance.public_dns_name
    while True:
        try:
            resp = requests.get('http://' + dns_name + '/ping')
            if resp.status_code == 200:
                logging.info('  {}: Up.'.format(instance.id))
                return
        except:
            pass
        time.sleep(5)