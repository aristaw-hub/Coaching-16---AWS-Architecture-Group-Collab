terraform {
  # 1. Backend Configuration
  # Ensure the bucket "sctp-ce12-tfstate-bucket" exists before running 'terraform init'
  backend "s3" {
    bucket = "sctp-ce12-tfstate-bucket"
    key    = "arista.tfstate"
    region = "ap-southeast-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# 2. Provider Configuration
provider "aws" {
  region = "ap-southeast-1"
}

# 3. Data Sources
# These fetch existing infrastructure details for your Custom Domain and SSL Cert
data "aws_route53_zone" "sctp_zone" {
  name = "sctp-sandbox.com"
}

data "aws_acm_certificate" "cert" {
  domain      = "*.sctp-sandbox.com"
  statuses    = ["ISSUED"]
  most_recent = true
}

# 4. S3 Bucket Resource
# This creates a new bucket for your application use (separate from the backend bucket)
resource "aws_s3_bucket" "s3_tf" {
  bucket_prefix = "arista-ce12-7may-bucket" # AWS requires lowercase for bucket names
  
  tags = {
    Name        = "Arista Bucket"
    Environment = "Dev"
    Group       = "Group5"
  }
}

# Optional: Enable versioning for your new bucket
resource "aws_s3_bucket_versioning" "s3_versioning" {
  bucket = aws_s3_bucket.s3_tf.id
  versioning_configuration {
    status = "Enabled"
  }
}
