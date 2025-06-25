# Variables for enhanced VPC module with financial-grade security

variable "project_name" {
  description = "Name of the project"
  type        = string
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must contain only lowercase letters, numbers, and hyphens."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid IPv4 CIDR block."
  }
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
  validation {
    condition     = length(var.public_subnet_cidrs) >= 2
    error_message = "At least 2 public subnets are required for high availability."
  }
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
  validation {
    condition     = length(var.private_subnet_cidrs) >= 2
    error_message = "At least 2 private subnets are required for high availability."
  }
}

variable "database_subnet_cidrs" {
  description = "CIDR blocks for database subnets"
  type        = list(string)
  default     = ["10.0.100.0/24", "10.0.200.0/24"]
  validation {
    condition     = length(var.database_subnet_cidrs) >= 2
    error_message = "At least 2 database subnets are required for high availability."
  }
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "enable_vpn_gateway" {
  description = "Enable VPN Gateway"
  type        = bool
  default     = false
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in VPC"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "Enable DNS support in VPC"
  type        = bool
  default     = true
}

variable "enable_flow_logs" {
  description = "Enable VPC Flow Logs for security monitoring"
  type        = bool
  default     = true
}

variable "flow_log_destination_type" {
  description = "Type of destination for VPC Flow Logs (cloud-watch-logs, s3)"
  type        = string
  default     = "cloud-watch-logs"
  validation {
    condition     = contains(["cloud-watch-logs", "s3"], var.flow_log_destination_type)
    error_message = "Flow log destination type must be either 'cloud-watch-logs' or 's3'."
  }
}

variable "log_retention_days" {
  description = "Number of days to retain VPC Flow Logs"
  type        = number
  default     = 2555  # 7 years for SOX compliance
  validation {
    condition     = var.log_retention_days >= 365
    error_message = "Log retention must be at least 365 days for compliance."
  }
}

variable "enable_network_acls" {
  description = "Enable custom Network ACLs for additional security"
  type        = bool
  default     = true
}

variable "enable_vpc_endpoints" {
  description = "Enable VPC Endpoints for AWS services"
  type        = bool
  default     = true
}

variable "vpc_endpoints" {
  description = "List of VPC endpoints to create"
  type        = list(string)
  default     = ["s3", "ecr.dkr", "ecr.api", "logs", "monitoring"]
}

variable "enable_dhcp_options" {
  description = "Enable custom DHCP options"
  type        = bool
  default     = true
}

variable "dhcp_options_domain_name" {
  description = "Domain name for DHCP options"
  type        = string
  default     = ""
}

variable "dhcp_options_domain_name_servers" {
  description = "Domain name servers for DHCP options"
  type        = list(string)
  default     = ["AmazonProvidedDNS"]
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default = {
    Terraform   = "true"
    Project     = "quantumalpha"
    Owner       = "platform-team"
    CostCenter  = "engineering"
    Compliance  = "sox,pci-dss,glba"
  }
}

variable "security_tags" {
  description = "Security-specific tags for compliance"
  type        = map(string)
  default = {
    "compliance.sox"       = "true"
    "compliance.pci-dss"   = "true"
    "compliance.glba"      = "true"
    "security.level"       = "high"
    "backup.required"      = "true"
    "monitoring.required"  = "true"
    "encryption.required"  = "true"
    "audit.required"       = "true"
  }
}

variable "enable_encryption" {
  description = "Enable encryption for all applicable resources"
  type        = bool
  default     = true
}

variable "kms_key_deletion_window" {
  description = "Number of days before KMS key deletion"
  type        = number
  default     = 7
  validation {
    condition     = var.kms_key_deletion_window >= 7 && var.kms_key_deletion_window <= 30
    error_message = "KMS key deletion window must be between 7 and 30 days."
  }
}

variable "enable_key_rotation" {
  description = "Enable automatic KMS key rotation"
  type        = bool
  default     = true
}

variable "allowed_cidr_blocks" {
  description = "List of CIDR blocks allowed to access resources"
  type        = list(string)
  default     = []
}

variable "allowed_security_groups" {
  description = "List of security group IDs allowed to access resources"
  type        = list(string)
  default     = []
}

variable "enable_transit_gateway" {
  description = "Enable Transit Gateway for multi-VPC connectivity"
  type        = bool
  default     = false
}

variable "transit_gateway_id" {
  description = "ID of existing Transit Gateway to attach to"
  type        = string
  default     = ""
}

variable "enable_private_dns" {
  description = "Enable private DNS for VPC endpoints"
  type        = bool
  default     = true
}

variable "enable_security_groups" {
  description = "Enable default security groups"
  type        = bool
  default     = true
}

variable "default_security_group_ingress" {
  description = "List of ingress rules for default security group"
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = []
}

variable "default_security_group_egress" {
  description = "List of egress rules for default security group"
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
      description = "All outbound traffic"
    }
  ]
}

variable "enable_ipv6" {
  description = "Enable IPv6 support"
  type        = bool
  default     = false
}

variable "assign_ipv6_address_on_creation" {
  description = "Assign IPv6 address on subnet creation"
  type        = bool
  default     = false
}

variable "map_public_ip_on_launch" {
  description = "Map public IP on instance launch in public subnets"
  type        = bool
  default     = false  # Security: Disabled by default
}

variable "enable_nat_instance" {
  description = "Use NAT instance instead of NAT Gateway (cost optimization)"
  type        = bool
  default     = false
}

variable "nat_instance_type" {
  description = "Instance type for NAT instance"
  type        = string
  default     = "t3.micro"
}

variable "enable_bastion_host" {
  description = "Enable bastion host for secure access"
  type        = bool
  default     = false
}

variable "bastion_instance_type" {
  description = "Instance type for bastion host"
  type        = string
  default     = "t3.micro"
}

variable "bastion_key_name" {
  description = "Key pair name for bastion host"
  type        = string
  default     = ""
}

variable "enable_cloudtrail" {
  description = "Enable CloudTrail for API logging"
  type        = bool
  default     = true
}

variable "cloudtrail_s3_bucket_name" {
  description = "S3 bucket name for CloudTrail logs"
  type        = string
  default     = ""
}

variable "enable_config" {
  description = "Enable AWS Config for compliance monitoring"
  type        = bool
  default     = true
}

variable "config_s3_bucket_name" {
  description = "S3 bucket name for AWS Config"
  type        = string
  default     = ""
}

variable "enable_guardduty" {
  description = "Enable GuardDuty for threat detection"
  type        = bool
  default     = true
}

variable "enable_security_hub" {
  description = "Enable Security Hub for security posture management"
  type        = bool
  default     = true
}

variable "compliance_standards" {
  description = "List of compliance standards to enable"
  type        = list(string)
  default     = ["aws-foundational-security-standard", "pci-dss", "cis-aws-foundations-benchmark"]
}

variable "enable_inspector" {
  description = "Enable Inspector for vulnerability assessment"
  type        = bool
  default     = true
}

variable "enable_macie" {
  description = "Enable Macie for data security and privacy"
  type        = bool
  default     = true
}

variable "enable_secrets_manager" {
  description = "Enable Secrets Manager for secure credential storage"
  type        = bool
  default     = true
}

variable "secrets_manager_kms_key_id" {
  description = "KMS key ID for Secrets Manager encryption"
  type        = string
  default     = ""
}

variable "enable_parameter_store" {
  description = "Enable Systems Manager Parameter Store"
  type        = bool
  default     = true
}

variable "parameter_store_kms_key_id" {
  description = "KMS key ID for Parameter Store encryption"
  type        = string
  default     = ""
}

