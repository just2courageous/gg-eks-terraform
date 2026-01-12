# gg-eks-terraform — Terraform [Infrastructure as Code] EKS [Elastic Kubernetes Service] platform

## 🎯 Goal
Provision an **EKS [Elastic Kubernetes Service]** cluster using **Terraform [Infrastructure as Code]** (no AWS Console [Amazon Web Services Console]):

- **VPC [Virtual Private Cloud]** with public/private subnets + NAT [Network Address Translation]
- **EKS [Elastic Kubernetes Service]** control plane + managed node group
- **IRSA [IAM Roles for Service Accounts]** via OIDC [OpenID Connect]
- Control-plane logging to **CloudWatch Logs [Amazon CloudWatch Logs]**
- (Add-on) Fluent Bit [Log shipper] to CloudWatch Logs using IRSA [IAM Roles for Service Accounts]
- (Add-on) Reliability demo: HPA [Horizontal Pod Autoscaler] + PDB [Pod Disruption Budget]

## 🧭 Architecture
![EKS Terraform architecture](docs/diagrams/gg-eks-terraform-arch.png)

**Editable backup**
- `docs/diagrams/gg-eks-terraform-arch.drawio`
- Generator: `docs/diagrams/arch.py`

## 📍 Environment (demo)
- **AWS [Amazon Web Services] Account:** 399717050894
- **Region:** us-east-2
- **AWS CLI [Command Line Interface] profile:** gg

> Note: `variables.tf` defaults `cluster_name` to `gg-eks-p7`.  
> If you want `green-guard-gg-eks`, set `-var="cluster_name=green-guard-gg-eks"` when applying.

## 📦 Repo structure (source of truth)
- `main.tf`, `versions.tf`, `variables.tf` — Terraform [Infrastructure as Code] (VPC [Virtual Private Cloud] + EKS [Elastic Kubernetes Service])
- `fluentbit-values.yaml` — Helm [Helm package manager] values for CloudWatch Logs [Amazon CloudWatch Logs]
- `manifests/irsa/` — IRSA [IAM Roles for Service Accounts] trust/policy JSON [JavaScript Object Notation]
- `docs/screenshots/` — proof screenshots
- `docs/evidence.md` — claim → proof mapping
- `docs/runbook.md` — recreate steps (for later rebuild)
- `reliability/` — HPA [Horizontal Pod Autoscaler] + PDB [Pod Disruption Budget] demo manifests + proofs

## 🧾 Proof
See `docs/evidence.md`.

## 🧹 Cost control
This repo is designed to be created with `terraform apply` and torn down with `terraform destroy` to control AWS [Amazon Web Services] cost.

## ⚠ Safety
Never commit AWS [Amazon Web Services] secrets (Access Keys [Credential Keys]) or kubeconfig [Kubernetes config] files.
