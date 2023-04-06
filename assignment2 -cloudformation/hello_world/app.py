import json
import boto3

dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table('statechanges')

def lambda_handler(event, context):
    print(event)
    instance_id=event['detail']['instance-id']
    curr_state=event['detail']['state']
    instance_launch_time=event['time']
    
    response = table.put_item(
        Item={
            'instance-id': instance_id,
            'curr_state': curr_state,
            'instance_launch_time' :instance_launch_time
        }
    )
    