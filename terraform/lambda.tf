data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/get/"
  output_path = "${path.module}/lambda/get/user_handler_get.zip.zip"
}

resource "aws_lambda_function" "user_handler_get_function" {
  filename      = "../lambda/get/user_handler_get.zip"
  function_name = "UserManagerGet"
  role          = aws_iam_role.usermanager_lambda_role.arn
  handler       = "index.handler"
  runtime       = "python3.9" # probably need to up this for 3.11
  environment {
    variables = {
      "USER_TABLE_NAME" = "${aws_dynamodb_table.user_manager_table.name}"
    }
  }
  depends_on = [aws_iam_role.usermanager_lambda_role]
}