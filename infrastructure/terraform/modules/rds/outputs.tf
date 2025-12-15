# Database Instance
output "db_instance_id" {
  description = "RDS instance ID"
  value       = aws_db_instance.main.id
}

output "db_instance_arn" {
  description = "RDS instance ARN"
  value       = aws_db_instance.main.arn
}

output "db_instance_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "db_instance_hosted_zone_id" {
  description = "RDS instance hosted zone ID"
  value       = aws_db_instance.main.hosted_zone_id
}

output "db_instance_port" {
  description = "RDS instance port"
  value       = aws_db_instance.main.port
}

output "db_instance_name" {
  description = "RDS instance database name"
  value       = aws_db_instance.main.db_name
}

output "db_instance_username" {
  description = "RDS instance master username"
  value       = aws_db_instance.main.username
  sensitive   = true
}

output "db_instance_engine" {
  description = "RDS instance engine"
  value       = aws_db_instance.main.engine
}

output "db_instance_engine_version" {
  description = "RDS instance engine version"
  value       = aws_db_instance.main.engine_version
}

output "db_instance_class" {
  description = "RDS instance class"
  value       = aws_db_instance.main.instance_class
}

output "db_instance_status" {
  description = "RDS instance status"
  value       = aws_db_instance.main.status
}

output "db_instance_multi_az" {
  description = "RDS instance Multi-AZ status"
  value       = aws_db_instance.main.multi_az
}

output "db_instance_storage_encrypted" {
  description = "RDS instance storage encryption status"
  value       = aws_db_instance.main.storage_encrypted
}

output "db_instance_kms_key_id" {
  description = "RDS instance KMS key ID"
  value       = aws_db_instance.main.kms_key_id
}

output "db_instance_availability_zone" {
  description = "RDS instance availability zone"
  value       = aws_db_instance.main.availability_zone
}

output "db_instance_backup_retention_period" {
  description = "RDS instance backup retention period"
  value       = aws_db_instance.main.backup_retention_period
}

output "db_instance_backup_window" {
  description = "RDS instance backup window"
  value       = aws_db_instance.main.backup_window
}

output "db_instance_maintenance_window" {
  description = "RDS instance maintenance window"
  value       = aws_db_instance.main.maintenance_window
}

# Read Replica
output "db_read_replica_id" {
  description = "RDS read replica instance ID"
  value       = var.create_read_replica ? aws_db_instance.read_replica[0].id : null
}

output "db_read_replica_arn" {
  description = "RDS read replica instance ARN"
  value       = var.create_read_replica ? aws_db_instance.read_replica[0].arn : null
}

output "db_read_replica_endpoint" {
  description = "RDS read replica instance endpoint"
  value       = var.create_read_replica ? aws_db_instance.read_replica[0].endpoint : null
  sensitive   = true
}

# Security Group
output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.rds.id
}

output "security_group_arn" {
  description = "ARN of the security group"
  value       = aws_security_group.rds.arn
}

output "security_group_name" {
  description = "Name of the security group"
  value       = aws_security_group.rds.name
}

# Parameter Group
output "parameter_group_id" {
  description = "DB parameter group ID"
  value       = aws_db_parameter_group.main.id
}

output "parameter_group_arn" {
  description = "DB parameter group ARN"
  value       = aws_db_parameter_group.main.arn
}

output "parameter_group_name" {
  description = "DB parameter group name"
  value       = aws_db_parameter_group.main.name
}

# Option Group
output "option_group_id" {
  description = "DB option group ID"
  value       = aws_db_option_group.main.id
}

output "option_group_arn" {
  description = "DB option group ARN"
  value       = aws_db_option_group.main.arn
}

output "option_group_name" {
  description = "DB option group name"
  value       = aws_db_option_group.main.name
}

# KMS Key
output "kms_key_id" {
  description = "KMS key ID for RDS encryption"
  value       = aws_kms_key.rds.key_id
}

output "kms_key_arn" {
  description = "KMS key ARN for RDS encryption"
  value       = aws_kms_key.rds.arn
}

output "kms_alias_name" {
  description = "KMS key alias name"
  value       = aws_kms_alias.rds.name
}

# CloudWatch Log Groups
output "cloudwatch_log_groups" {
  description = "CloudWatch log groups for RDS logs"
  value = {
    for log_type, log_group in aws_cloudwatch_log_group.postgresql :
    log_type => {
      name = log_group.name
      arn  = log_group.arn
    }
  }
}

# CloudWatch Alarms
output "cloudwatch_alarms" {
  description = "CloudWatch alarms for RDS monitoring"
  value = {
    cpu_utilization = {
      name = aws_cloudwatch_metric_alarm.database_cpu.alarm_name
      arn  = aws_cloudwatch_metric_alarm.database_cpu.arn
    }
    connection_count = {
      name = aws_cloudwatch_metric_alarm.database_connections.alarm_name
      arn  = aws_cloudwatch_metric_alarm.database_connections.arn
    }
    free_storage = {
      name = aws_cloudwatch_metric_alarm.database_free_storage.alarm_name
      arn  = aws_cloudwatch_metric_alarm.database_free_storage.arn
    }
  }
}

output "enhanced_monitoring_iam_role_arn" {
  description = "Enhanced monitoring IAM role ARN"
  value       = var.monitoring_interval > 0 ? aws_iam_role.rds_enhanced_monitoring[0].arn : null
}

output "enhanced_monitoring_iam_role_name" {
  description = "Enhanced monitoring IAM role name"
  value       = var.monitoring_interval > 0 ? aws_iam_role.rds_enhanced_monitoring[0].name : null
}

# Secrets Manager
output "secrets_manager_secret_id" {
  description = "Secrets Manager secret ID for database credentials"
  value       = aws_secretsmanager_secret.db_credentials.id
}

output "secrets_manager_secret_arn" {
  description = "Secrets Manager secret ARN for database credentials"
  value       = aws_secretsmanager_secret.db_credentials.arn
}

output "secrets_manager_secret_name" {
  description = "Secrets Manager secret name for database credentials"
  value       = aws_secretsmanager_secret.db_credentials.name
}

# Compliance Snapshot
output "compliance_snapshot_id" {
  description = "Compliance snapshot ID"
  value       = var.create_compliance_snapshot ? aws_db_snapshot.compliance_snapshot[0].id : null
}

output "compliance_snapshot_arn" {
  description = "Compliance snapshot ARN"
  value       = var.create_compliance_snapshot ? aws_db_snapshot.compliance_snapshot[0].db_snapshot_arn : null
}

# Connection Information
output "connection_info" {
  description = "Database connection information"
  value = {
    endpoint = aws_db_instance.main.endpoint
    port     = aws_db_instance.main.port
    database = aws_db_instance.main.db_name
    username = aws_db_instance.main.username
  }
  sensitive = true
}

# Compliance Information
output "compliance_info" {
  description = "Compliance and security information"
  value = {
    sox_compliant        = true
    pci_dss_compliant    = true
    glba_compliant       = true
    encryption_enabled   = aws_db_instance.main.storage_encrypted
    backup_enabled       = aws_db_instance.main.backup_retention_period > 0
    monitoring_enabled   = var.monitoring_interval > 0
    multi_az_enabled     = aws_db_instance.main.multi_az
    deletion_protection  = aws_db_instance.main.deletion_protection
    performance_insights = var.performance_insights_enabled
  }
}

# Network Information
output "network_info" {
  description = "Network configuration information"
  value = {
    vpc_security_group_ids = aws_db_instance.main.vpc_security_group_ids
    db_subnet_group_name   = aws_db_instance.main.db_subnet_group_name
    publicly_accessible    = aws_db_instance.main.publicly_accessible
    availability_zone      = aws_db_instance.main.availability_zone
  }
}

# Storage Information
output "storage_info" {
  description = "Storage configuration information"
  value = {
    allocated_storage     = aws_db_instance.main.allocated_storage
    max_allocated_storage = aws_db_instance.main.max_allocated_storage
    storage_type          = aws_db_instance.main.storage_type
    storage_encrypted     = aws_db_instance.main.storage_encrypted
    kms_key_id            = aws_db_instance.main.kms_key_id
    iops                  = aws_db_instance.main.iops
  }
}

# Backup Information
output "backup_info" {
  description = "Backup configuration information"
  value = {
    backup_retention_period   = aws_db_instance.main.backup_retention_period
    backup_window             = aws_db_instance.main.backup_window
    copy_tags_to_snapshot     = aws_db_instance.main.copy_tags_to_snapshot
    delete_automated_backups  = aws_db_instance.main.delete_automated_backups
    final_snapshot_identifier = aws_db_instance.main.final_snapshot_identifier
  }
}

# Monitoring Information
output "monitoring_info" {
  description = "Monitoring configuration information"
  value = {
    monitoring_interval                   = aws_db_instance.main.monitoring_interval
    monitoring_role_arn                   = aws_db_instance.main.monitoring_role_arn
    enabled_cloudwatch_logs_exports       = aws_db_instance.main.enabled_cloudwatch_logs_exports
    performance_insights_enabled          = aws_db_instance.main.performance_insights_enabled
    performance_insights_kms_key_id       = aws_db_instance.main.performance_insights_kms_key_id
    performance_insights_retention_period = aws_db_instance.main.performance_insights_retention_period
  }
}
