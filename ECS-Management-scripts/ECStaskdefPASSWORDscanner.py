import boto3
from pprint import pprint
import os

session=boto3.session.Session(profile_name='<enter profile name here>')
client = session.client(service_name='ecs', region_name='us-east-1')

paginator = client.get_paginator('list_clusters')

service_paginator = client.get_paginator('list_services')

cluster_iterator = paginator.paginate()

MessageBody = []

i = 1
for each_page in cluster_iterator:
    j = 1
    for each_arn in each_page['clusterArns']:
        service_iterator = service_paginator.paginate(
            cluster=each_arn,
            #launchType='EC2'|'FARGATE'|'EXTERNAL',
            #schedulingStrategy='REPLICA',
        )
        for each_service_list_page in service_iterator:
            for each_service_arn in each_service_list_page['serviceArns']:
                #print(f"taskdef: {client.describe_services(cluster=each_arn, services=[each_service_arn],)['services'][0]['taskDefinition'].split('/')[1]}")
                for each_env in client.describe_task_definition(taskDefinition=client.describe_services(cluster=each_arn, services=[each_service_arn],)['services'][0]['taskDefinition'],)['taskDefinition']['containerDefinitions'][0]['environment']:
                    if 'pass' in each_env['name'] or 'PASS' in each_env['name'] or 'Pass' in each_env['name']:
                        print(f"Cluster{j}: {each_arn.split('/')[1]}")
                        MessageBody.append(f"Cluster{j}: {each_arn.split('/')[1]}")
                        print(f"taskdef: {client.describe_services(cluster=each_arn, services=[each_service_arn],)['services'][0]['taskDefinition'].split('/')[1]}")
                        MessageBody.append(f"taskdef: {client.describe_services(cluster=each_arn, services=[each_service_arn],)['services'][0]['taskDefinition'].split('/')[1]}")
                        print('\x1b[1;30;47m' + each_env['name'] +':'+ each_env['value'] + '\x1b[0m')
                        MessageBody.append(f"{each_env['name']}: {each_env['value']}")
        j += 1
    i += 1
#print("\n".join(MessageBody))

#open text file
text_file = open(os.getcwd()+"/passwordscanningreport.txt", "w")

#write string to file
text_file.write("\n".join(MessageBody))

#close file
text_file.close()
