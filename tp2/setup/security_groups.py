from time import sleep
from typing import Collection
import logging, sys
from boto3_type_annotations.ec2 import ServiceResource, SecurityGroup


def get_security_group(ec2: ServiceResource, name: str):
    '''
    Returns the security group with the provided name.

        Parameters:
            ec2 (ServiceResource): The EC2 service resource object
            name (str):            The security group name
        
        Returns:
            security_group (SecurityGroup): The security group
    '''

    security_groups: Collection[SecurityGroup] = ec2.security_groups.all()
    for security_group in security_groups:
        if security_group.group_name == name:
            return security_group
    return None


def delete_security_group(ec2: ServiceResource, name: str):
    '''
    Deletes the security group with the provided name.

        Parameters:
            ec2 (ServiceResource): The EC2 service resource object
            name (str):            The security group name
    '''

    logging.info(f'Deleting security group...')
    security_group = get_security_group(ec2, name)
    if security_group is None:
        return
    for i in range(50):
        security_group.reload()
        try:
            if security_group.ip_permissions:
                security_group.revoke_ingress(IpPermissions=security_group.ip_permissions)
            security_group.delete()
            logging.info(f'  {name}: Deleted.')
            return
        except:
            sleep(2)
    logging.error('Unable to delete the security group. Please relaunch the script.')
    sys.exit(1)


def create_security_group(ec2: ServiceResource, name: str) -> SecurityGroup:
    '''
    Creates a security group with the provided name.

        Parameters:
            ec2 (ServiceResource): The EC2 service resource object
            name (str):            The security group name
        
        Returns:
            security_group (SecurityGroup): The created security group
    '''
    
    logging.info(f'Creating security group "{name}"...')
    security_group: SecurityGroup = ec2.create_security_group(
        GroupName=name, 
        Description='Default TP1 security group')
    security_group.authorize_ingress(
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 443,
             'ToPort': 443,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': '-1',
             'FromPort': -1,
             'ToPort': -1,
             'UserIdGroupPairs': [{ 'GroupId': security_group.group_id }]
            }
        ]
    )
    return security_group