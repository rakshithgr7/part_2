import json
import boto3
import time


client = boto3.client('ec2')
def lambda_handler(event, context):
    print(event)
    print(type(event))
    

    ami1 = event['Payload']['body']
    print(ami1)
    step_func_name=ami1.split(",")[1].split(':')[-1].replace("'",'')
    ami=ami1.split(",")[0].split(':')[1]
    ami=ami.replace(" ","")
    
    print(ami)
    time.sleep(120)
    response = client.run_instances(
    ImageId=ami,
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,)
    print(response)
    instance_id=response['Instances'][0]['InstanceId']
    ami_id=response['Instances'][0]['ImageId']
    print(instance_id)
    final=(f"{instance_id}:{step_func_name}")
    print(final)
    return {
        'statusCode': 200,
        'body': json.dumps(instance_id)
    }