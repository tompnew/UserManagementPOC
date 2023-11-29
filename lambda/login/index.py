import json
import os
import boto3
from datetime import date
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb_table_name = os.environ['USER_TABLE_NAME']
    dynamodb_client = boto3.client('dynamodb')
    
    # Login user
    user_data = json.loads(event['body'])
    try:
        # Todo: Check if User Exists
        response = dynamodb_client.get_item(
            TableName=dynamodb_table_name,
            Key={
                'email': {'S': user_data['email']}
            }
        )

        password = response['Item']["password"]
        login_password = {'S': user_data['password']}

        if password != login_password:
            return {
              'statusCode': 400,
              'body': json.dumps(f'Incorrect Password!!')
            }
        
        today = date.today()

        response = dynamodb_client.update_item(
            TableName=dynamodb_table_name,
            Key={'email': {'S': user_data['email']}},
            UpdateExpression="set last_login_date=:l",
            ExpressionAttributeValues={":l": {'S': today.strftime("%d/%m/%Y %H:%M:%S")}},
            ReturnValues="UPDATED_NEW",
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f'Login Successful')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error logging in user: {str(e)}')
        }

