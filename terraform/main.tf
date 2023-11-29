terraform {

  # removing remote state and dynamodb lock
  #backend "s3" {
  #  bucket = "state"
  #  key    = "terraform/state/usermanagement"
  #  region = "eu-west-1"
  #}

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}


data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  aws_account_id = data.aws_caller_identity.current.account_id
  aws_region     = data.aws_region.current.name
}


provider "aws" {
  region  = "eu-west-1"

  default_tags {
    tags = {
      Environment = "UserManager-${title(terraform.workspace)}"
      Owner       = "TomN"
    }
  }
}
