from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    Stack,
    Duration,    
)
from constructs import Construct

class UserManagementStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB table for storing user data
        user_table = dynamodb.Table(
            self, "Users",
            partition_key=dynamodb.Attribute(name="email", type=dynamodb.AttributeType.STRING),
        )
        
        # Lambda function to handle user CRUD operations
        user_handler = _lambda.Function(
            self, 
            "UserHandler",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "USER_TABLE_NAME": user_table.table_name
            },
            memory_size=1024,
            timeout=Duration.minutes(5),
        )
        
        # Grant permissions to the Lambda function to access the DynamoDB table
        user_table.grant_read_write_data(user_handler)

        # Create API Gateway
        #api = apigateway.LambdaRestApi(
        api = apigateway.RestApi(
            self,
            "UserApi",
         #   handler=user_handler,
            endpoint_configuration=apigateway.EndpointConfiguration(
                types=[apigateway.EndpointType.REGIONAL]
            ),
            deploy=False
        )

        # Define Lambda integration for the API
        user_integration = apigateway.LambdaIntegration(user_handler)

        # Create resource for user operations
        user_resource = api.root.add_resource("user")

        # Define API methods for CRUD operations
        user_resource.add_method("GET", user_integration)  # List users
        user_resource.add_method("POST", user_integration)  # Create user
        user_resource.add_method("PUT", user_integration)  # Update user
        user_resource.add_method("DELETE", user_integration)  # Delete user

        # Create resource for login endpoint
        login_resource = api.root.add_resource("login")

        # Define Lambda integration for login
        login_integration = apigateway.LambdaIntegration(
            user_handler, request_templates={"application/json": '{"httpMethod": "POST"}'}
        )

        # Define API method for login
        login_resource.add_method("POST", login_integration)


