# ElastiCache Module Outputs

output "endpoint" {
  description = "The address of the Redis primary endpoint"
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
}

output "reader_endpoint" {
  description = "The address of the Redis reader endpoint"
  value       = aws_elasticache_replication_group.redis.reader_endpoint_address
}

output "port" {
  description = "The port number on which the Redis accepts connections"
  value       = 6379
}

output "replication_group_id" {
  description = "The ID of the ElastiCache Replication Group"
  value       = aws_elasticache_replication_group.redis.id
}

output "replication_group_arn" {
  description = "The ARN of the ElastiCache Replication Group"
  value       = aws_elasticache_replication_group.redis.arn
}

output "security_group_id" {
  description = "The ID of the security group created for Redis"
  value       = aws_security_group.redis.id
}

output "parameter_group_id" {
  description = "The ElastiCache parameter group name"
  value       = aws_elasticache_parameter_group.redis.id
}

output "subnet_group_name" {
  description = "The name of the subnet group"
  value       = aws_elasticache_subnet_group.main.name
}
