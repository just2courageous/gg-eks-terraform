# Discover AZs so we can make subnets cleanly
data "aws_availability_zones" "available" {
  state = "available"
}

# -------- VPC --------
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.5"

  name = "${var.cluster_name}-vpc"
  cidr = var.vpc_cidr

  azs             = slice(data.aws_availability_zones.available.names, 0, 3)
  public_subnets  = [cidrsubnet(var.vpc_cidr, 4, 0), cidrsubnet(var.vpc_cidr, 4, 1), cidrsubnet(var.vpc_cidr, 4, 2)]
  private_subnets = [cidrsubnet(var.vpc_cidr, 4, 3), cidrsubnet(var.vpc_cidr, 4, 4), cidrsubnet(var.vpc_cidr, 4, 5)]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }
}

# -------- EKS --------
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.24"

  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  enable_irsa = true                # for IAM Roles for Service Accounts (pods)

  enable_cluster_creator_admin_permissions = true
  
  # Emit control-plane logs to CloudWatch (safe & useful)
  cluster_enabled_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    default = {
      instance_types = var.instance_types
      min_size       = var.min_size
      desired_size   = var.desired_size
      max_size       = var.max_size
      subnets        = module.vpc.private_subnets
    }
  }

  tags = {
    Project = "gg-eks-terraform"
  }
}
