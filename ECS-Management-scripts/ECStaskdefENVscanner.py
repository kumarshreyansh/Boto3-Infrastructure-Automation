import boto3
from pprint import pprint

session=boto3.session.Session(profile_name='<enter profile name here>')
client = session.client(service_name='ecs', region_name='us-east-1')


paginator = client.get_paginator('list_clusters')

service_paginator = client.get_paginator('list_services')

cluster_iterator = paginator.paginate()



i = 1
for each_page in cluster_iterator:
    print(i)
    j = 1
    for each_arn in each_page['clusterArns']:
        print('=================================================================================')
        print('\x1b[1;30;47m' + 'arn name is {} and cluster count is {}'.format(each_arn, j) + '\x1b[0m')
        service_iterator = service_paginator.paginate(
            cluster=each_arn,
            #launchType='EC2'|'FARGATE'|'EXTERNAL',
            #schedulingStrategy='REPLICA',
        )
        for each_service_list_page in service_iterator:
            #pprint(each_service_list_page['serviceArns'])
            for each_service_arn in each_service_list_page['serviceArns']:
                print('\x1b[2;30;43m'+ 'task definiton is {}'.format(client.describe_services(
                    cluster=each_arn,
                    services=[each_service_arn],
                )['services'][0]['taskDefinition']) + '\x1b[0m')
                pprint(client.describe_task_definition(
                    taskDefinition=client.describe_services(cluster=each_arn,
                    services=[each_service_arn],
                )['services'][0]['taskDefinition'],
                )['taskDefinition']['containerDefinitions'][0]['environment'])
        j += 1
    i += 1
