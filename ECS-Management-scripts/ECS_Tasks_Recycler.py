import json
import boto3
from pprint import pprint
import os
import sys
import time
from datetime import datetime,date

session=boto3.session.Session(profile_name='<paste profile name here>')

current_time = datetime.now().strftime("%H:%M")
if current_time == "10:00":
    cluster_name="<cluster name>"
    service_name="<service name>"
else:
    print("Will not perform recycling as no condition matches")
    sys.exit()
print(f"working on service: {service_name} of cluster: {cluster_name}")

client = session.client('ecs')
current_date=str(date.today())
desired_count=client.describe_services(cluster=cluster_name, services=[service_name,],)['services'][0]['deployments'][0]['desiredCount']
print("\n")
print(f"desired running task count should be: {desired_count}")

print("\n")
print(f"current date is : {current_date}")
print("\n")
print("==================================================================")
def no_of_task_func():
    task_list=[]
    for i in client.list_tasks(cluster=cluster_name, serviceName=service_name, desiredStatus='RUNNING')['taskArns']:
        task_list.append(i)
    global total_no_of_task
    total_no_of_task=len(task_list)
no_of_task_func()
print("\n")
print(f"total tasks running as of now: {total_no_of_task}")
print("\n")
src_for_evaluation=[]
for i in client.list_tasks(cluster=cluster_name, serviceName=service_name, desiredStatus='RUNNING')['taskArns']:
    task_creation_list=client.describe_tasks(cluster=cluster_name, tasks=[i])['tasks']
    for j in task_creation_list:
        creation_time=str(j['createdAt'])
        src_str=creation_time+" "+i
        src_for_evaluation.append(src_str)
src_for_evaluation.sort(key = lambda x: x.split()[0])
primary_task_list=src_for_evaluation
print("\n")
print("Tasks running in the beginning: ")
print("\n")
print(primary_task_list)
print("\n")
no_of_task_func()
for each_task_stamp in src_for_evaluation:
    print("==================================================================")
    print("\n")
    print(f"we are verifying {each_task_stamp}")
    print("\n")
    date_of_each_running_task=each_task_stamp.split()[0]  #.split('-')[2])
    no_of_task_func()
    if total_no_of_task == desired_count:
        no_of_task_func()
        if date_of_each_running_task < current_date:
            print("==================================================================")
            print("\n")
            print(f"we'll be trying to stop {each_task_stamp.split()[2]} created at {date_of_each_running_task}")
            print("\n")
            client.stop_task(
                cluster=cluster_name,
                task=each_task_stamp.split()[2]
            )
            while client.describe_tasks(cluster=cluster_name, tasks=[each_task_stamp.split()[2],],)['tasks'][0]['containers'][0]['lastStatus'] != 'STOPPED':
                time.sleep(2)
            print(f"{each_task_stamp.split()[2]} stopped successfully")
            print("==================================================================")
            print("\n")
            time.sleep(25)
            no_of_task_func()
            print("==================================================================")
            print(f"total tasks running as of now: {total_no_of_task}")
        else:
            print(f"{each_task_stamp.split()[2]} is not outdated")
            continue
    else:
        print("\n")
        print("we are running below task limit")
no_of_task_func()
print("\n")
print("==================================================================")
print(f"total tasks running at final check: {total_no_of_task}")
print("\n")
print("and the brief list of same: ")
print("\n")
final_list=[]
for k in client.list_tasks(cluster=cluster_name, serviceName=service_name, desiredStatus='RUNNING')['taskArns']:
    final_task_creation_list=client.describe_tasks(cluster=cluster_name, tasks=[k])['tasks']
    for l in final_task_creation_list:
        final_creation_time=str(l['createdAt'])
        final_src_str=final_creation_time+" "+k
        final_list.append(final_src_str)
final_list.sort(key = lambda x: x.split()[0])
print(final_list)