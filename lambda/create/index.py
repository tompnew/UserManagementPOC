import json
import os
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb_table_name = os.environ['USER_TABLE_NAME']
    dynamodb_client = boto3.client('dynamodb')
    
    # Create user
    user_data = json.loads(event['body'])
    try:
        # todo: Validate paylod
        dynamodb_client.put_item(
            TableName=dynamodb_table_name,
            Item={
                'email': {'S': user_data['email']},
                'username': {'S': user_data['username']},
                'password': {'S': user_data['password']},
                'last_login_date': {'S': user_data['last_login_date']}
            }
        )
        return {
            'statusCode': 201,
            'body': json.dumps('User created successfully')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error creating user: {str(e)}')
        }

