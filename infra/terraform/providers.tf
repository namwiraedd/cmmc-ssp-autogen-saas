terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
  endpoints {
    # For GovCloud, set provider alias and use appropriate region, e.g., us-gov-west-1
  }
}
