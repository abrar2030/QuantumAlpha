variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs"
  type        = list(string)
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
}

variable "allocated_storage" {
  description = "Allocated storage for RDS instance in GB"
  type        = number
}

variable "engine_version" {
  description = "PostgreSQL engine version"
  type        = string
}

variable "database_name" {
  description = "Name of the database"
  type        = string
}

variable "master_username" {
  description = "Master username for RDS instance"
  type        = string
}

variable "master_password" {
  description = "Master password for RDS instance"
  type        = string
  sensitive   = true
}
