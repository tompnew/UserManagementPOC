import json
import os
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb_table_name = os.environ['USER_TABLE_NAME']
    dynamodb_client = boto3.client('dynamodb')
    
    # List users
    try:
        response = dynamodb_client.scan(TableName=dynamodb_table_name)
        users = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps(users)
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error listing users: {str(e)}')
        }