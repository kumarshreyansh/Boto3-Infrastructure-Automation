import boto3
from pprint import pprint

ACCESS_KEY="paste access key here"
SECRET_KEY="paste secret key here"
client = boto3.client('ssm', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name='us-east-1')
ec2 = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name='us-east-1')

i=1
for each in ec2.instances.all():
    print(i)
    print(each.instance_id)
    i = i+1
    try:
        client.send_command(
            InstanceIds=[
                each.instance_id,
            ],
            DocumentName='AWS-RunShellScript',
            #DocumentVersion='[1]Default',
            DocumentHash='<paste document hash here>',
            DocumentHashType='Sha256',
            #TimeoutSeconds=123,
            Comment='string',
            Parameters={
                'commands': [
                    "#!/bin/bash",
                    "",
                    "hostname",
                    "cat /home/ec2-user/.aws/credentials 2>&1 & cat /home/ubuntu/.aws/credentials 2>&1"
                ]
            },
            CloudWatchOutputConfig={
                'CloudWatchLogGroupName': 'InstanceAccessKeyScanning',
                'CloudWatchOutputEnabled': True
            }
        )
    except Exception as e:
        print(e)
