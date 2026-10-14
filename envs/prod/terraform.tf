terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  # Bucket created by bootstrap/ in this account. S3 native locking, no DynamoDB.
  backend "s3" {
    bucket       = "sqlhelper-tfstate-333333333333"
    key          = "prod/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
