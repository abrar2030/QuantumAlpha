provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "../../modules/vpc"

  project_name         = "quantumalpha"
  environment          = var.environment
  vpc_cidr             = var.vpc_cidr
  public_subnet_cidrs  = var.public_subnets
  private_subnet_cidrs = var.private_subnets
  common_tags          = var.common_tags
}

module "eks" {
  source = "../../modules/eks"

  environment         = var.environment
  cluster_name        = "quantumalpha-${var.environment}"
  cluster_version     = var.eks_cluster_version
  vpc_id              = module.vpc.vpc_id
  private_subnet_ids  = module.vpc.private_subnet_ids
  node_instance_types = var.eks_node_instance_types
  node_desired_size   = var.eks_node_desired_size
  node_min_size       = var.eks_node_min_size
  node_max_size       = var.eks_node_max_size
}

module "rds" {
  source = "../../modules/rds"

  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  instance_class     = var.rds_instance_class
  allocated_storage  = var.rds_allocated_storage
  engine_version     = var.rds_engine_version
  database_name      = "quantumalpha"
  master_username    = var.rds_master_username
  master_password    = var.rds_master_password
}

module "elasticache" {
  source = "../../modules/elasticache"

  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  node_type          = var.elasticache_node_type
  engine_version     = var.elasticache_engine_version
  num_cache_nodes    = var.elasticache_num_cache_nodes
}

# MSK module commented out - create modules/msk if needed
# module "msk" {
#   source = "../modules/msk"
#
#   environment         = var.environment
#   vpc_id              = module.vpc.vpc_id
#   private_subnet_ids  = module.vpc.private_subnet_ids
#   kafka_version       = var.msk_kafka_version
#   broker_instance_type = var.msk_broker_instance_type
#   broker_count        = var.msk_broker_count
#   ebs_volume_size     = var.msk_ebs_volume_size
# }

# Output the EKS cluster endpoint and certificate authority data
output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "eks_cluster_certificate_authority_data" {
  value     = module.eks.cluster_certificate_authority_data
  sensitive = true
}

# Output the RDS endpoint
output "rds_endpoint" {
  value = module.rds.endpoint
}

# Output the ElastiCache endpoint
output "elasticache_endpoint" {
  value = module.elasticache.endpoint
}

# Output the MSK bootstrap brokers
# output "msk_bootstrap_brokers" {
#   value = module.msk.bootstrap_brokers
# }
