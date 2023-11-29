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
        
        # Lambda functions to handle user CRUD operations
        user_handler_create = _lambda.Function(
            self, 
            "UserHandlerCreate",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/create"),
            environment={
                "USER_TABLE_NAME": user_table.table_name
            },
            memory_size=256,
            timeout=Duration.minutes(1),
        )

        user_handler_delete = _lambda.Function(
            self, 
            "UserHandlerDelete",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/delete"),
            environment={
                "USER_TABLE_NAME": user_table.table_name
            },
            memory_size=256,
            timeout=Duration.minutes(1),
        )

        user_handler_get = _lambda.Function(
            self, 
            "UserHandlerGet",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/get"),
            environment={
                "USER_TABLE_NAME": user_table.table_name
            },
            memory_size=256,
            timeout=Duration.minutes(1),
        )

        user_handler_update = _lambda.Function(
            self, 
            "UserHandlerUpdate",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/update"),
            environment={
                "USER_TABLE_NAME": user_table.table_name
            },
            memory_size=256,
            timeout=Duration.minutes(1),
        )
        
        user_handler_login = _lambda.Function(
            self, 
            "UserHandlerLogin",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/login"),
            environment={
                "USER_TABLE_NAME": user_table.table_name
            },
            memory_size=256,
            timeout=Duration.minutes(1),
        )

        # Grant permissions to the Lambda function to access the DynamoDB table
        user_table.grant_read_write_data(user_handler_create)
        user_table.grant_read_write_data(user_handler_delete)
        user_table.grant_read_write_data(user_handler_get)
        user_table.grant_read_write_data(user_handler_update)
        user_table.grant_read_write_data(user_handler_login)

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
        user_integration_create = apigateway.LambdaIntegration(user_handler_create)
        user_integration_delete = apigateway.LambdaIntegration(user_handler_delete)
        user_integration_get = apigateway.LambdaIntegration(user_handler_get)
        user_integration_update = apigateway.LambdaIntegration(user_handler_update)

        # Create resource for user operations
        user_resource = api.root.add_resource("user")

        # Define API methods for CRUD operations
        user_resource.add_method("GET", user_integration_get)  # List users
        user_resource.add_method("POST", user_integration_update)  # Update user
        user_resource.add_method("PUT", user_integration_create)  # Create user
        user_resource.add_method("DELETE", user_integration_delete)  # Delete user

        # Create resource for login endpoint
        login_resource = api.root.add_resource("login")

        # Define Lambda integration for login
        login_integration = apigateway.LambdaIntegration(
            user_handler_login, request_templates={"application/json": '{"httpMethod": "POST"}'}
        )

        # Define API method for login
        login_resource.add_method("POST", login_integration)