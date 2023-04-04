import boto3
import json

# define the DynamoDB table that Lambda will connect to
tableName = "part2dynamo"

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

def lambda_handler(event, context):
    print(event)
 s
    
    def ddb_create(x):
        print(x)
        dynamo.put_item(**x)
        return x

    def ddb_read():
        response = dynamo.scan()
        return(response['Items'])
    def ddb_update(x):
        dynamo.update_item(**x)
        return x
        
    def ddb_delete(x):
        dynamo.delete_item(**x)

    def echo(x):
        return x

    operations = {
        'create': ddb_create,
        'read': ddb_read,
        'update': ddb_update,
        'delete': ddb_delete,
        'echo': echo,
    }
    
    if(event['httpMethod']!='GET'):
        body=json.loads(event['body'])
        operation=body['operation']
        payload = body['payload']
        if operation in operations:
            operations[operation](payload)
            statusCode=200
            data = "success"
            return{
                "statusCode":statusCode,
                "body":json.dumps(data),
                "headers":{
                    "Content-Type":"application/json"
                    
                }
            }
            
    else:
        data=ddb_read()
        statusCode=200
        return{
        "statusCode":statusCode,
        "body":json.dumps(data),
        "headers":{
            "Content-Type":"application/json"
        }
        }