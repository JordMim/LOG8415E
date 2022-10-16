from typing import Collection
import boto3, os
from boto3_type_annotations.ec2 import ServiceResource, SecurityGroup

def delete_security_group(ec2: ServiceResource, name: str):
    security_groups: Collection[SecurityGroup] = ec2.security_groups.all()
    for security_group in security_groups:
        if security_group.group_name == name:
            security_group.delete()
            return

def create_security_group(ec2: ServiceResource, name: str) -> SecurityGroup:
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