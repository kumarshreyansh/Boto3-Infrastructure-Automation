import boto3
import time
import sys

ACCESS_KEY=sys.argv[1]
SECRET_KEY=sys.argv[2]
Capacity = sys.argv[3]
MachineId = sys.argv[4]

client = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name='us-east-1')


if client.describe_instance_attribute(Attribute='instanceType', InstanceId=MachineId)['InstanceType']['Value'] == Capacity:
    print('machine already at requested capacity')
    sys.exit()

if client.describe_instance_status(InstanceIds=[MachineId])['InstanceStatuses'][0]['InstanceState']['Name'] != 'stopped':


    response = client.stop_instances(
        InstanceIds=[
            MachineId,
        ],
        #Force=True|False
    )

while client.describe_instance_status(InstanceIds=[MachineId])['InstanceStatuses'][0]['InstanceState']['Name'] != 'stopped':
    time.sleep(2)

response = client.modify_instance_attribute(
    Attribute='instanceType',
    InstanceId=MachineId,
    InstanceType={
        'Value': Capacity
    }
)

while client.describe_instance_attribute(Attribute='instanceType', InstanceId=MachineId)['InstanceType']['Value'] != Capacity:
    time.sleep(5)

if client.describe_instance_attribute(Attribute='instanceType', InstanceId=MachineId)['InstanceType']['Value'] == Capacity:

    while client.describe_instance_status(InstanceIds=[MachineId])['InstanceStatuses'][0]['InstanceState']['Name'] != 'stopped':
        time.sleep(2)

    response = client.start_instances(
        InstanceIds=[
            MachineId,
        ],
    )

    while client.describe_instance_status(InstanceIds=[MachineId])['InstanceStatuses'][0]['InstanceState']['Name'] != 'running':
        time.sleep(2)

    print('Scaling was successful')