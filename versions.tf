terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region    # us-east-2
  profile = var.aws_profile   # gg

  # ✅ Correct place for default tags in v5
  default_tags {
    tags = {
      Project     = "green-guard"
      Environment = "demo"
      Owner       = "Courage"
    }
  }
}
