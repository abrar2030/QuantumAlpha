# Terraform Backend Configuration
# For local development, uses local backend
# For production, configure S3 backend with DynamoDB locking

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Local backend for development
  # Uncomment and configure for production:
  # backend "s3" {
  #   bucket         = "quantumalpha-terraform-state"
  #   key            = "dev/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "quantumalpha-terraform-locks"
  #   kms_key_id     = "arn:aws:kms:region:account-id:key/key-id"
  # }
}
