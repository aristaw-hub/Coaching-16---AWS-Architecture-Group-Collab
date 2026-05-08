terraform {
  backend "s3" {
    bucket = "sctp-core-tfstate"
    key    = "shortener-demo.tfstate"
    region = "ap-southeast-1"
  }
  
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    http = {
      source  = "hashicorp/http"
      version = "~> 3.0"
    }
  }
}