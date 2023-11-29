resource "aws_dynamodb_table" "user_manager_table" {
  name           = "UserManager"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "email"

  attribute {
    name = "email"
    type = "S"
  }


}