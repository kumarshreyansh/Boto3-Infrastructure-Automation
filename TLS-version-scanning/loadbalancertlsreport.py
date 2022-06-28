import os
import time
import boto3
from pprint import pp, pprint
import sys
import pandas as pd

#Update Profile name with your aws named profile
session=boto3.session.Session(profile_name='<paste profile name here>')
elbv2client = session.client('elbv2', region_name='us-east-1')
elbclient = session.client('elb', region_name='us-east-1')

i = 1
MessageBody = []
MessageBodyForCSV = []
response = elbv2client.describe_load_balancers(PageSize=10)
for each in response['LoadBalancers']:
    print(i)
    list1 = []
    list2 = []
    print(each['LoadBalancerName'])
    list1.append(f"Load balancer name: {each['LoadBalancerName']} Policies: ")
    list2.append(each['LoadBalancerName'])
    for every_item in elbv2client.describe_listeners(LoadBalancerArn=each['LoadBalancerArn'])['Listeners']:
        if 'SslPolicy' in every_item:
            pprint(every_item['SslPolicy'])
            list1.append(every_item['SslPolicy'])
            list2.append(every_item['SslPolicy'])
    data = " ".join(list1)
    MessageBody.append(data)
    MessageBodyForCSV.append(list2)
    del data
    del list1
    del list2
    i = i+1
while 'NextMarker' in response:
    response = elbv2client.describe_load_balancers(Marker=response['NextMarker'],PageSize=10)
    for each in response['LoadBalancers']:
        print(i)
        list1 = []
        list2 = []
        print(each['LoadBalancerName'])
        list1.append(f"Load balancer name: {each['LoadBalancerName']} Policies: ")
        list2.append(each['LoadBalancerName'])
        for every_item in elbv2client.describe_listeners(LoadBalancerArn=each['LoadBalancerArn'],)['Listeners']:
            if 'SslPolicy' in every_item:
                pprint(every_item['SslPolicy'])
                list1.append(every_item['SslPolicy'])
                list2.append(every_item['SslPolicy'])
        data = " ".join(list1)
        MessageBody.append(data)
        MessageBodyForCSV.append(list2)
        del data
        del list1
        del list2
        i = i+1


elbv1response = elbclient.describe_load_balancers(PageSize=10)
for each in elbv1response['LoadBalancerDescriptions']:
    print(i)
    list1 = []
    list2 = []
    pprint(each['LoadBalancerName'])
    list1.append(f"Load balancer name: {each['LoadBalancerName']} Policies: ")
    list2.append(each['LoadBalancerName'])
    if len(each['ListenerDescriptions'][0]['PolicyNames']) != 0:
        for each_element in each['ListenerDescriptions'][0]['PolicyNames']:
            print(each_element)
            list1.append(each_element)
            list2.append(each_element)
    if len(each['Policies']['OtherPolicies']) != 0:
        for each_element in each['Policies']['OtherPolicies']:
            print(each_element)
            list1.append(each_element)
            list2.append(each_element)
    data = " ".join(list1)
    MessageBody.append(data)
    MessageBodyForCSV.append(list2)
    del data
    del list1
    del list2
    i = i+1
while 'NextMarker' in elbv1response:
    elbv1response = elbclient.describe_load_balancers(Marker=elbv1response['NextMarker'],PageSize=10)
    for each in elbv1response['LoadBalancerDescriptions']:
        print(i)
        list1 = []
        list2 = []
        pprint(each['LoadBalancerName'])
        list1.append(f"Load balancer name: {each['LoadBalancerName']} Policies: ")
        list2.append(each['LoadBalancerName'])
        if len(each['ListenerDescriptions'][0]['PolicyNames']) != 0:
            for each_element in each['ListenerDescriptions'][0]['PolicyNames']:
                print(each_element)
                list1.append(each_element)
                list2.append(each_element)
        if len(each['Policies']['OtherPolicies']) != 0:
            for each_element in each['Policies']['OtherPolicies']:
                print(each_element)
                list1.append(each_element)
                list2.append(each_element)
        data = " ".join(list1)
        MessageBody.append(data)
        MessageBodyForCSV.append(list2)
        del data
        del list1
        del list2
        i = i+1


MessageBodyParsed = "\n".join(MessageBody)

#open text file
text_file = open(os.getcwd()+"/loadbalancerreport.txt", "w")

#write string to file
text_file.write("\n".join(MessageBody))

#close file
text_file.close()

list_len = [len(i) for i in MessageBodyForCSV]
headerlength = max(list_len)

my_df = pd.DataFrame(MessageBodyForCSV)
headerList = ['LoadBalancer Name']
for _ in range(headerlength-1):
    headerList.append('Policy')

my_df.to_csv(os.getcwd()+'/loadbalancertlsreport.csv', index=False, header=headerList)