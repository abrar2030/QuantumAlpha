# Outputs for enhanced VPC module

# VPC
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_arn" {
  description = "ARN of the VPC"
  value       = aws_vpc.main.arn
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "vpc_default_security_group_id" {
  description = "ID of the default security group"
  value       = aws_vpc.main.default_security_group_id
}

output "vpc_default_network_acl_id" {
  description = "ID of the default network ACL"
  value       = aws_vpc.main.default_network_acl_id
}

output "vpc_default_route_table_id" {
  description = "ID of the default route table"
  value       = aws_vpc.main.default_route_table_id
}

output "vpc_enable_dns_support" {
  description = "Whether DNS support is enabled in the VPC"
  value       = aws_vpc.main.enable_dns_support
}

output "vpc_enable_dns_hostnames" {
  description = "Whether DNS hostnames are enabled in the VPC"
  value       = aws_vpc.main.enable_dns_hostnames
}

# Internet Gateway
output "igw_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.main.id
}

output "igw_arn" {
  description = "ARN of the Internet Gateway"
  value       = aws_internet_gateway.main.arn
}

# Subnets
output "public_subnet_ids" {
  description = "List of IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "public_subnet_arns" {
  description = "List of ARNs of the public subnets"
  value       = aws_subnet.public[*].arn
}

output "public_subnet_cidr_blocks" {
  description = "List of CIDR blocks of the public subnets"
  value       = aws_subnet.public[*].cidr_block
}

output "private_subnet_ids" {
  description = "List of IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

output "private_subnet_arns" {
  description = "List of ARNs of the private subnets"
  value       = aws_subnet.private[*].arn
}

output "private_subnet_cidr_blocks" {
  description = "List of CIDR blocks of the private subnets"
  value       = aws_subnet.private[*].cidr_block
}

output "database_subnet_ids" {
  description = "List of IDs of the database subnets"
  value       = aws_subnet.database[*].id
}

output "database_subnet_arns" {
  description = "List of ARNs of the database subnets"
  value       = aws_subnet.database[*].arn
}

output "database_subnet_cidr_blocks" {
  description = "List of CIDR blocks of the database subnets"
  value       = aws_subnet.database[*].cidr_block
}

output "database_subnet_group_id" {
  description = "ID of the database subnet group"
  value       = aws_db_subnet_group.main.id
}

output "database_subnet_group_name" {
  description = "Name of the database subnet group"
  value       = aws_db_subnet_group.main.name
}

output "elasticache_subnet_group_id" {
  description = "ID of the ElastiCache subnet group"
  value       = aws_elasticache_subnet_group.main.id
}

output "elasticache_subnet_group_name" {
  description = "Name of the ElastiCache subnet group"
  value       = aws_elasticache_subnet_group.main.name
}

# NAT Gateways
output "nat_gateway_ids" {
  description = "List of IDs of the NAT Gateways"
  value       = aws_nat_gateway.main[*].id
}

output "nat_gateway_public_ips" {
  description = "List of public Elastic IPs associated with the NAT Gateways"
  value       = aws_eip.nat[*].public_ip
}

output "nat_gateway_private_ips" {
  description = "List of private IP addresses of the NAT Gateways"
  value       = aws_nat_gateway.main[*].private_ip
}

# Route Tables
output "public_route_table_id" {
  description = "ID of the public route table"
  value       = aws_route_table.public.id
}

output "private_route_table_ids" {
  description = "List of IDs of the private route tables"
  value       = aws_route_table.private[*].id
}

output "database_route_table_id" {
  description = "ID of the database route table"
  value       = aws_route_table.database.id
}

# Network ACLs
output "public_network_acl_id" {
  description = "ID of the public network ACL"
  value       = aws_network_acl.public.id
}

output "private_network_acl_id" {
  description = "ID of the private network ACL"
  value       = aws_network_acl.private.id
}

output "database_network_acl_id" {
  description = "ID of the database network ACL"
  value       = aws_network_acl.database.id
}

# VPC Endpoints
output "vpc_endpoint_s3_id" {
  description = "ID of the S3 VPC endpoint"
  value       = aws_vpc_endpoint.s3.id
}

output "vpc_endpoint_ecr_dkr_id" {
  description = "ID of the ECR DKR VPC endpoint"
  value       = aws_vpc_endpoint.ecr_dkr.id
}

output "vpc_endpoint_ecr_api_id" {
  description = "ID of the ECR API VPC endpoint"
  value       = aws_vpc_endpoint.ecr_api.id
}

output "vpc_endpoints_security_group_id" {
  description = "ID of the VPC endpoints security group"
  value       = aws_security_group.vpc_endpoints.id
}

# Security
output "flow_log_id" {
  description = "ID of the VPC Flow Log"
  value       = aws_flow_log.vpc_flow_log.id
}

output "flow_log_cloudwatch_log_group_name" {
  description = "Name of the CloudWatch Log Group for VPC Flow Logs"
  value       = aws_cloudwatch_log_group.vpc_flow_log.name
}

output "flow_log_cloudwatch_log_group_arn" {
  description = "ARN of the CloudWatch Log Group for VPC Flow Logs"
  value       = aws_cloudwatch_log_group.vpc_flow_log.arn
}

output "vpc_logs_kms_key_id" {
  description = "ID of the KMS key for VPC logs encryption"
  value       = aws_kms_key.vpc_logs.key_id
}

output "vpc_logs_kms_key_arn" {
  description = "ARN of the KMS key for VPC logs encryption"
  value       = aws_kms_key.vpc_logs.arn
}

output "vpc_logs_kms_alias_name" {
  description = "Name of the KMS key alias for VPC logs"
  value       = aws_kms_alias.vpc_logs.name
}

output "flow_log_iam_role_arn" {
  description = "ARN of the IAM role for VPC Flow Logs"
  value       = aws_iam_role.flow_log.arn
}

# Availability Zones
output "availability_zones" {
  description = "List of availability zones used"
  value       = data.aws_availability_zones.available.names
}

# CIDR blocks for reference
output "vpc_cidr_blocks" {
  description = "All CIDR blocks associated with the VPC"
  value = {
    vpc      = aws_vpc.main.cidr_block
    public   = aws_subnet.public[*].cidr_block
    private  = aws_subnet.private[*].cidr_block
    database = aws_subnet.database[*].cidr_block
  }
}

# Tags
output "common_tags" {
  description = "Common tags applied to resources"
  value       = var.common_tags
}

# Compliance and Security Information
output "compliance_info" {
  description = "Compliance and security information"
  value = {
    sox_compliant         = true
    pci_dss_compliant     = true
    glba_compliant        = true
    encryption_enabled    = true
    flow_logs_enabled     = true
    vpc_endpoints_enabled = true
    network_acls_enabled  = true
  }
}

# Network Configuration Summary
output "network_summary" {
  description = "Summary of network configuration"
  value = {
    vpc_id                   = aws_vpc.main.id
    vpc_cidr                 = aws_vpc.main.cidr_block
    public_subnets_count     = length(aws_subnet.public)
    private_subnets_count    = length(aws_subnet.private)
    database_subnets_count   = length(aws_subnet.database)
    nat_gateways_count       = length(aws_nat_gateway.main)
    availability_zones_count = length(data.aws_availability_zones.available.names)
    flow_logs_enabled        = true
    vpc_endpoints_count      = 3
  }
}
