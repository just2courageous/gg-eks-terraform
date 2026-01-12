# 🧾 Evidence (gg-eks-terraform)

## ✅ Terraform [Infrastructure as Code] provisioning
- **Terraform apply complete**
  - `docs/screenshots/terraform-apply-complete.png`
- **Worker nodes Ready**
  - `docs/screenshots/kubectl-get-nodes.png`
- **Core system pods running**
  - `docs/screenshots/kube-system-pods.png`

## ✅ IRSA [IAM Roles for Service Accounts] + Fluent Bit [Log shipper] → CloudWatch Logs [Amazon CloudWatch Logs]
- **Log groups visible**
  - `docs/screenshots/p8/p8-logging-01-log-groups.png`
- **Log streams visible**
  - `docs/screenshots/p8/p8-logging-02-log-streams.png`
- **Sample log event**
  - `docs/screenshots/p8/p8-logging-03-stream-sample.png`
- **Fluent Bit output config / ConfigMap [Configuration Map]**
  - `docs/screenshots/p8/p8-logging-04-configmap-output.png`
- **DaemonSet [Daemon Set] rollout OK**
  - `docs/screenshots/p8/p8-logging-05-rollout-ok.png`
- **No AccessDenied (IRSA working)**
  - `docs/screenshots/p8/p8-logging-06-fluentbit-no-denied.png`
- **ServiceAccount [Kubernetes Service Account] annotated (IRSA)**
  - `docs/screenshots/p8/p8-logging-07-sa-irsa.png`
- **Helm values proof**
  - `docs/screenshots/p8/p8-logging-08-helm-values.png`

## ✅ Reliability demo (HPA [Horizontal Pod Autoscaler] + PDB [Pod Disruption Budget])
- **Metrics Server [metrics collector] ready**
  - `reliability/screenshots/p8-metrics-server-ready.png`
- **CPU demo pods running**
  - `reliability/screenshots/p8-cpu-demo-pods.png`
- **HPA scaling**
  - `reliability/screenshots/p8-hpa-scaling.png`
- **PDB created**
  - `reliability/screenshots/p8-pdb.png`
- **Self-heal proof**
  - `reliability/screenshots/p8-self-heal.png`
  - `reliability/screenshots/p8-self-heal-confirmed.png`
