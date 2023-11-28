import json
import os
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb_table_name = os.environ['USER_TABLE_NAME']
    dynamodb_client = boto3.client('dynamodb')
    
    if event['httpMethod'] == 'POST':
        # Create user
        user_data = json.loads(event['body'])
        try:
            dynamodb_client.put_item(
                TableName=dynamodb_table_name,
                Item={
                    'email': {'S': user_data['email']},
                    'name': {'S': user_data['name']},
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

    elif event['httpMethod'] == 'GET':
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

    # Add logic for handling other HTTP methods (PUT, DELETE, and login) here

    return {
        'statusCode': 400,
        'body': json.dumps('Invalid request')
    }
