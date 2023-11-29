resource "aws_iam_role" "usermanager_lambda_role" {
  name               = "user-manager-execution-role-${terraform.workspace}"
  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "lambda.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

resource "aws_iam_policy" "usermanager_lambda_cloudwatch_policy" {

  name        = "user-manager-cloudwatch-policy-${terraform.workspace}"
  path        = "/UserManager/"
  description = "AWS IAM Policy"
  policy      = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
       "logs:CreateLogGroup",
       "logs:CreateLogStream",
       "logs:PutLogEvents"
     ],
     "Resource": "arn:aws:logs:*:*:*",
     "Effect": "Allow"
   }
 ]
}
EOF
}


resource "aws_iam_policy" "usermanager_lambda_dynamodb_policy" {
  name        = "user-manager-dynamodb-policy-${terraform.workspace}"
  path        = "/UserManager/"
  description = "AWS IAM Policy"
  policy      = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
  {
   "Effect": "Allow",
			"Action": [
				"dynamodb:BatchGetItem",
				"dynamodb:GetItem",
				"dynamodb:Query",
				"dynamodb:Scan",
				"dynamodb:BatchWriteItem",
				"dynamodb:PutItem",
				"dynamodb:UpdateItem"
			],
			"Resource": "${aws_dynamodb_table.user_manager_table.arn}"
    }
 ]
}
EOF
}


resource "aws_iam_role_policy_attachment" "usermanager_lambda_policy_cloudwatch_attachement" {
  role       = aws_iam_role.usermanager_lambda_role.name
  policy_arn = aws_iam_policy.usermanager_lambda_cloudwatch_policy.arn
}

resource "aws_iam_role_policy_attachment" "usermanager_lambda_policy_dynamo_attachement" {
  role       = aws_iam_role.usermanager_lambda_role.name
  policy_arn = aws_iam_policy.usermanager_lambda_dynamodb_policy.arn
}