import json
import os
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb_table_name = os.environ['USER_TABLE_NAME']
    dynamodb_client = boto3.client('dynamodb')
    
    # Login user
    user_data = json.loads(event['body'])
    try:
        # Todo: Check if User Exists
        response = dynamodb_client.update_item(
            TableName=dynamodb_table_name,
            Key={'email': {'S': user_data['email']}},
            UpdateExpression="set username=:n, password=:p",
            ExpressionAttributeValues={":n": {'S': user_data['username']}, ":p": {'S': user_data['password']} },
            ReturnValues="UPDATED_NEW",
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f'User Updated Successfully')
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error updating in user: {str(e)}')
        }

