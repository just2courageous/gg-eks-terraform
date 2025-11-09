# gg-eks-terraform

## 💼 Project Goal
Provision an Amazon EKS (Elastic Kubernetes Service) cluster on AWS using 100% Terraform (Infrastructure as Code), not the AWS console.

This includes:
- VPC (Virtual Private Cloud) with subnets
- EKS control plane
- Managed node group (worker nodes)
- IAM (Identity and Access Management) roles for the nodes
- OIDC (OpenID Connect) support so pods can assume IAM roles later (IRSA)

After `terraform apply`, I connect with `kubectl` and verify the cluster is alive.

After testing, I run `terraform destroy` to shut everything down and stop spending money.

## 📍 Environment
- AWS Account ID: 399717050894
- Region: us-east-2
- AWS CLI profile: gg
- Planned cluster name: green-guard-gg-eks

## 🔄 Workflow (what this repo proves)
1. `terraform init && terraform apply`  
   → Creates the entire Kubernetes platform (EKS cluster + node group + networking).

2. `aws eks update-kubeconfig --name green-guard-gg-eks --region us-east-2 --profile gg`  
   → Point kubectl at the new cluster.

3. `kubectl get nodes -o wide`  
   → Prove worker nodes joined successfully.

4. `terraform destroy -auto-approve`  
   → Tear everything down to cut cost.

## 🖼 Evidence / Screenshots
All proof screenshots will go in `docs/screenshots/`:
- `terraform-apply-complete.png` – successful apply showing resources created
- `kubectl-get-nodes.png` – nodes Ready in the new cluster
- `terraform-destroy-complete.png` – successful destroy with 0 leftovers

These screenshots are what I show in interviews.

## 🛡 Cost Control
This repo is part of a bigger story:
I only keep clusters up while I'm working.  
When I'm done, I destroy them.  
This is how I control AWS cost.

This will connect later to P9 (cost guardrails / teardown discipline).

## ⚠ Notes
- This repo is meant to be public and reviewed by hiring managers.
- Do NOT commit AWS secrets or keys.
- The account / region info is here because it's part of the demonstration environment.



## 📦 P8 — CloudWatch Logging with Fluent Bit + IRSA

**Goal:** Ship pod logs to **Amazon CloudWatch Logs** using **aws-for-fluent-bit** with **IRSA (IAM Roles for Service Accounts)**.

**Key settings**
- **Region:** us-east-2
- **Log Group:** `/aws/eks/fluentbit-cloudwatch/logs`
- **ServiceAccount:** `logging/fluent-bit` (IRSA annotated)
- **Retention:** 7 days

**Install/upgrade (what I ran)**
```bash
MSYS_NO_PATHCONV=1 \
helm upgrade --install aws-for-fluent-bit aws/aws-for-fluent-bit \
  -n logging \
  --reuse-values \
  --set region=us-east-2 \
  --set cloudWatch.region=us-east-2 \
  --set-string cloudWatch.logGroupName=/aws/eks/fluentbit-cloudwatch/logs \
  --set cloudWatch.logRetentionDays=7 \
  --set serviceAccount.create=true \
  --set serviceAccount.name=fluent-bit \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"="$ROLE_ARN"

kubectl -n logging rollout status ds/aws-for-fluent-bit