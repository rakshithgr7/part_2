import json
import boto3

client = boto3.client('ec2')

def lambda_handler(event, context):
    print(event)
    InstanceID=event['Item']['existing_instance_id']
    response = client.create_image(InstanceId=InstanceID,Name="My-custom-AMI", NoReboot=True)
    sendAMI = response['ImageId']
    print(type(response['ImageId']))
    # output=f"{'ami': {sendAMI}, 'event': {event}}"
    output="ami: {0}, event: {1}".format(sendAMI,event)
    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }