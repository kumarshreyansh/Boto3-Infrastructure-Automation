import os
import time
import boto3
from pprint import pp, pprint
import sys
import pandas as pd

#Update Profile name with your aws named profile
session=boto3.session.Session(profile_name='<paste profile name here>')
client = session.client('apigateway', region_name='us-east-1')

MessageBodyForCSV = []
for each in client.get_domain_names()['items']:
    list1 = []
    print(each['domainName'])
    list1.append(each['domainName'])
    print(each['securityPolicy'])
    list1.append(each['securityPolicy'])
    MessageBodyForCSV.append(list1)
    del list1

my_df = pd.DataFrame(MessageBodyForCSV)
headerList = ['Custom Domain Name', 'Security Policy']

my_df.to_csv(os.getcwd()+'/apigatewaytlsreport.csv', index=False, header=headerList)
