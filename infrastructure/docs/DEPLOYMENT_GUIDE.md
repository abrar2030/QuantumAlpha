# QuantumAlpha Infrastructure - Deployment Guide

## Prerequisites

### Required Tools and Versions

| Tool         | Min Version | Install Command                                                                                |
| ------------ | ----------- | ---------------------------------------------------------------------------------------------- |
| Terraform    | >= 1.0      | `brew install terraform` or download from https://www.terraform.io/downloads                   |
| kubectl      | >= 1.24     | `brew install kubectl` or `curl -LO https://dl.k8s.io/release/v1.28.0/bin/linux/amd64/kubectl` |
| Helm         | >= 3.0      | `brew install helm` or https://helm.sh/docs/intro/install/                                     |
| AWS CLI      | >= 2.0      | `brew install awscli` or https://aws.amazon.com/cli/                                           |
| yamllint     | latest      | `pip install yamllint`                                                                         |
| ansible-lint | latest      | `pip install ansible-lint`                                                                     |

### AWS Credentials Setup

```bash
# Configure AWS credentials
aws configure
# Or export environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

## Terraform Deployment

### Step 1: Initialize Terraform

```bash
cd terraform/environments/dev

# Copy and configure variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values (see below)

# Initialize Terraform
terraform init

# Optional: Configure remote backend (recommended for production)
# Edit backend.tf and uncomment the S3 backend configuration
```

### Step 2: Configure Variables

Edit `terraform.tfvars`:

```hcl
# Required variables
aws_region = "us-east-1"
environment = "dev"

# Network configuration
vpc_cidr = "10.0.0.0/16"
public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
private_subnets = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]

# RDS password - SET VIA ENVIRONMENT VARIABLE
# export TF_VAR_rds_master_password="your-secure-password-here"
```

### Step 3: Validate and Plan

```bash
# Format all Terraform files
terraform fmt -recursive

# Validate configuration
terraform validate

# Review planned changes
terraform plan -out=tfplan

# Review the plan carefully before applying
```

### Step 4: Apply Infrastructure

```bash
# Apply the infrastructure
terraform apply tfplan

# Save outputs for Kubernetes configuration
terraform output -json > outputs.json
```

## Kubernetes Deployment

### Step 1: Configure kubectl

```bash
# Get EKS cluster credentials
aws eks update-kubeconfig --region us-east-1 --name quantumalpha-dev

# Verify connection
kubectl cluster-info
kubectl get nodes
```

### Step 2: Prepare Secrets

```bash
cd kubernetes/base

# Create actual secret files from examples
cp ../../secrets/postgres_password.txt.example ../../secrets/postgres_password.txt
cp ../../secrets/influxdb_password.txt.example ../../secrets/influxdb_password.txt
cp ../../secrets/influxdb_token.txt.example ../../secrets/influxdb_token.txt

# Edit these files with actual secure passwords
# IMPORTANT: These files are gitignored and must be managed securely
```

### Step 3: Validate Kubernetes Manifests

```bash
# Validate YAML syntax
yamllint .

# Dry-run apply (validate against cluster)
kubectl apply --dry-run=client -k .

# Check for deprecated APIs
kubectl apply --dry-run=server -k .
```

### Step 4: Deploy to Kubernetes

```bash
# Deploy base configuration
kubectl apply -k kubernetes/base/

# Verify deployments
kubectl get all -n quantumalpha
kubectl get pods -n quantumalpha

# Check pod logs
kubectl logs -n quantumalpha <pod-name>
```

### Step 5: Deploy Environment-Specific Overlays

```bash
# For development
kubectl apply -k kubernetes/overlays/dev/

# For staging
kubectl apply -k kubernetes/overlays/staging/

# For production
kubectl apply -k kubernetes/overlays/prod/
```

## Monitoring Setup

### Access Prometheus

```bash
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Open http://localhost:9090
```

### Access Grafana

```bash
kubectl port-forward -n monitoring svc/grafana 3000:3000
# Open http://localhost:3000
# Default credentials: admin/admin (change immediately)
```

## Validation Commands

### Terraform Validation

```bash
cd terraform/environments/dev

# Format check
terraform fmt -check -recursive

# Initialize without backend
terraform init -backend=false

# Validate
terraform validate

# Security scan (if tfsec installed)
tfsec .
```

### Kubernetes Validation

```bash
cd kubernetes/base

# YAML lint
yamllint .

# Dry-run validation
kubectl apply --dry-run=client -k .

# Check resource limits
kubectl get pods -n quantumalpha -o json | \
  jq '.items[] | select(.spec.containers[].resources.limits == null)'
```

## Troubleshooting

### Terraform Issues

**Issue**: Module not found

```bash
# Solution: Re-initialize
terraform init -upgrade
```

**Issue**: State lock error

```bash
# Solution: Force unlock (use carefully)
terraform force-unlock <lock-id>
```

### Kubernetes Issues

**Issue**: Pod stuck in Pending

```bash
# Check events
kubectl describe pod <pod-name> -n quantumalpha

# Check node resources
kubectl top nodes
```

**Issue**: ImagePullBackOff

```bash
# Check image name and registry credentials
kubectl describe pod <pod-name> -n quantumalpha
```

## Security Best Practices

1. **Never commit secrets**:
   - Use `.gitignore` for actual secret files
   - Only commit `.example` files
   - Use AWS Secrets Manager or Vault for production

2. **Rotate credentials regularly**:
   - Database passwords: every 90 days
   - API keys: every 180 days
   - TLS certificates: before expiry

3. **Enable audit logging**:

   ```bash
   # Check CloudTrail logs
   aws cloudtrail lookup-events --max-results 10

   # Check Kubernetes audit logs
   kubectl logs -n kube-system kube-apiserver-*
   ```

4. **Review security groups**:
   ```bash
   # List security groups
   aws ec2 describe-security-groups --filters "Name=vpc-id,Values=<vpc-id>"
   ```

## Cleanup / Destroy

### Kubernetes Cleanup

```bash
# Delete all resources
kubectl delete -k kubernetes/overlays/dev/
kubectl delete -k kubernetes/base/
```

### Terraform Destroy

```bash
cd terraform/environments/dev

# Plan destroy
terraform plan -destroy -out=destroy.tfplan

# Review and confirm
terraform show destroy.tfplan

# Execute destroy
terraform apply destroy.tfplan
```
