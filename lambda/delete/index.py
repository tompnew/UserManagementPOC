import json
import os
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb_table_name = os.environ['USER_TABLE_NAME']
    dynamodb_client = boto3.client('dynamodb')
    
     # Delete user
    user_data = json.loads(event['body'])
    try:
        # Todo: Validation does user exist
        dynamodb_client.delete_item(
            TableName=dynamodb_table_name,
            Key={
                'email': {'S': user_data['email']}               
            }
        )
        return {
            'statusCode': 200, # OK
            'body': json.dumps('User Deleted')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error deleting user: {str(e)}')
        }
       
    
