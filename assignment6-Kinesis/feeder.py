import boto3
import json
import base64
import os
import datetime

dynamodb = boto3.resource('dynamodb')

s3 = boto3.client('s3')
kinesis = boto3.client('kinesis')
data=[]

kinesisDB=os.environ['dynamotable']
s3Bucket=os.environ['s3Bucket']
table = dynamodb.Table(kinesisDB)
fors3=[]

print(kinesisDB,s3Bucket)

def lambda_handler(event, context):
    print(event)
    
    for i in event['Records']:
        json1=json.loads(base64.b64decode(i['kinesis']['data']).decode('utf-8'))
        fors3.append(json.loads(base64.b64decode(i['kinesis']['data']).decode('utf-8')))
        # print(json1)
        table.put_item(
            Item={
                'ArtistId':json1
            })
        
        
 
    data=json.dumps(fors3)
    print(type(data))
    key=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".json"
    s3.put_object(Bucket=s3Bucket, Key=key, Body=data)
    


  
       

    

    



