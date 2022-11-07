import os, logging, requests, time
from typing import List
from boto3_type_annotations.ec2 import ServiceResource, SecurityGroup, Instance

USER_DATA_SCRIPT_FILE = 'instance_user_data.txt'
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, USER_DATA_SCRIPT_FILE)) as file:
    USER_DATA_SCRIPT = file.read()

def delete_all_instances(ec2: ServiceResource):
    logging.info('Terminating all instances...')
    for instance in ec2.instances.all():
        if instance.state['Name'] != 'terminated':
            instance.terminate()
    for instance in ec2.instances.all():
        if instance.state['Name'] != 'terminated':
            instance.wait_until_terminated()
            logging.info('  {}: Terminated.'.format(instance.id))


def create_instance(ec2: ServiceResource, instance_type: str, availability_zone: str, security_group: SecurityGroup) -> Instance:
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
    logging.info('Waiting for the instance to be running...')
    instance.wait_until_running()
    logging.info('  {}: Running.'.format(instance.id))

def wait_for_ping(instance: Instance):
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

def retreive_instances(ec2: ServiceResource, instance_type: str) -> List[Instance]:
    instances = []
    for instance in ec2.instances.all():
        if instance.state['Name'] == 'terminated':
            continue
        if instance.instance_type == instance_type:
            instances.append(instance)
    return instances