provider "aws" {
  region              = "us-east-1"
  allowed_account_ids = ["111111111111"] # placeholder: the dev account

  default_tags {
    tags = {
      Project     = "sqlhelper"
      Environment = local.env
      ManagedBy   = "terraform"
    }
  }
}

locals {
  env  = "dev"
  name = "sqlhelper-${local.env}"
}

module "network" {
  source = "../../modules/network"

  name                = local.name
  cidr_block          = "10.10.0.0/16"
  single_az_endpoints = true
}

module "ecr" {
  source = "../../modules/ecr"

  name = "sqlhelper-api"
}

module "api" {
  source = "../../modules/api"

  name              = local.name
  vpc_id            = module.network.vpc_id
  vpc_cidr          = module.network.vpc_cidr
  subnet_ids        = module.network.private_subnet_ids
  s3_prefix_list_id = module.network.s3_prefix_list_id
  repository_url    = module.ecr.repository_url
  app_origin        = "https://${var.domain_name}"

  cpu       = 256
  memory    = 512
  min_count = 1 # cheapest: one task, no autoscaling
  max_count = 1

  deployment_config_name = "CodeDeployDefault.ECSAllAtOnce"
  rollback_alarm_names   = module.monitoring.rollback_alarm_names
  log_retention_days     = 14
  deletion_protection    = false
}

module "edge" {
  source = "../../modules/edge"

  name         = local.name
  domain_name  = var.domain_name
  alb_arn      = module.api.alb_arn
  alb_dns_name = module.api.alb_dns_name
  price_class  = "PriceClass_100"
}

module "monitoring" {
  source = "../../modules/monitoring"

  name            = local.name
  alb_arn_suffix  = module.api.alb_arn_suffix
  cluster_name    = module.api.cluster_name
  service_name    = module.api.service_name
  distribution_id = module.edge.distribution_id
  alarm_email     = var.alarm_email
}

module "github_oidc" {
  source = "../../modules/github-oidc"

  name                            = local.name
  github_repository               = var.github_repository
  github_environment              = local.env
  ecr_repository_arn              = module.ecr.repository_arn
  ecs_service_arn                 = module.api.service_arn
  execution_role_arn              = module.api.execution_role_arn
  codedeploy_app_arn              = module.api.codedeploy_app_arn
  codedeploy_deployment_group_arn = module.api.codedeploy_deployment_group_arn
  frontend_bucket_arn             = module.edge.frontend_bucket_arn
  distribution_arn                = module.edge.distribution_arn
}
