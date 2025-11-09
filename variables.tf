variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "aws_profile" {
  description = "AWS CLI profile to use"
  type        = string
  default     = "gg"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "gg-eks-p7"
}

variable "kubernetes_version" {
  description = "EKS Kubernetes version"
  type        = string
  default     = "1.32"
}

variable "vpc_cidr" {
  description = "VPC CIDR"
  type        = string
  default     = "10.0.0.0/16"
}

variable "desired_size" {
  type        = number
  default     = 2
}

variable "min_size" {
  type        = number
  default     = 2
}

variable "max_size" {
  type        = number
  default     = 3
}

variable "instance_types" {
  description = "Worker node instance types"
  type        = list(string)
  default     = ["t3.medium"]
}
