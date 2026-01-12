from diagrams import Diagram, Cluster, Edge

from diagrams.onprem.client import User
from diagrams.onprem.iac import Terraform

from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet, NATGateway, InternetGateway
from diagrams.aws.compute import EKS, EC2
from diagrams.aws.security import IAM, IAMRole
from diagrams.aws.management import Cloudwatch

from diagrams.k8s.infra import Node
from diagrams.k8s.compute import Pod, DaemonSet


# ---- Dark theme styling (Graphviz [Graph Visualization Software]) ----
graph_attr = {
    "pad": "0.8",
    "splines": "spline",
    "nodesep": "0.7",
    "ranksep": "1.0",
    "fontsize": "14",
    "dpi": "300",
    "bgcolor": "#0B1220",
    "fontcolor": "#E5E7EB",
}
node_attr = {
    "fontsize": "12",
    "fontcolor": "#E5E7EB",
    "color": "#334155",
    "style": "filled",
    "fillcolor": "#111827",
}
edge_attr = {
    "color": "#94A3B8",
    "fontcolor": "#E5E7EB",
    "fontsize": "10",
}

with Diagram(
    "Green-Guard: Terraform → EKS + IRSA + CloudWatch Logs",
    show=False,
    filename="docs/diagrams/gg-eks-terraform-arch",
    outformat="png",
    direction="LR",
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr,
):
    # ---- Local (your laptop) ----
    dev = User("You\n(local)")
    tf = Terraform("Terraform\n(IaC [Infrastructure as Code])")

    dev >> Edge(label="terraform init / plan / apply") >> tf

    # ---- AWS [Amazon Web Services] ----
    with Cluster("AWS [Amazon Web Services]"):
        cw = Cloudwatch("CloudWatch Logs\n(control-plane + Fluent Bit)")

        with Cluster("Networking: VPC [Virtual Private Cloud] 10.0.0.0/16"):
            igw = InternetGateway("Internet Gateway")
            nat = NATGateway("NAT [Network Address Translation]\n(Single)")

            pub = PublicSubnet("Public subnets\n(3 AZs [Availability Zones])")
            priv = PrivateSubnet("Private subnets\n(3 AZs [Availability Zones])")

            # Typical routing story (simplified)
            pub >> igw
            priv >> nat >> igw

            vpc = VPC("VPC")

        with Cluster("EKS [Elastic Kubernetes Service]"):
            eks = EKS("EKS cluster")
            ng = EC2("Managed node group\n(t3.medium)")

            with Cluster("Kubernetes [Container Orchestration]"):
                nodes = Node("Worker nodes")
                pods = Pod("Workloads / Pods")
                fluentbit = DaemonSet("aws-for-fluent-bit\n(DaemonSet [Daemon Set])")

        # ---- IRSA [IAM Roles for Service Accounts] ----
        oidc = IAM("OIDC [OpenID Connect]\nprovider")
        role = IAMRole("IRSA role\n(gg-fluentbit-irsa)")

    # ---- Terraform provisions infra ----
    tf >> Edge(label="creates") >> vpc
    tf >> Edge(label="creates") >> eks
    tf >> Edge(label="creates") >> ng

    vpc >> Edge(label="private subnets") >> eks
    ng >> Edge(label="runs") >> nodes >> pods

    # ---- Cluster logging (control plane logs) ----
    eks >> Edge(label="control-plane logs") >> cw

    # ---- IRSA chain for Fluent Bit ----
    eks >> Edge(label="enable_irsa = true") >> oidc
    oidc >> Edge(label="trust policy") >> role
    role >> Edge(label="annotate ServiceAccount\nlogging/fluent-bit") >> fluentbit
    fluentbit >> Edge(label="ship pod logs") >> cw
