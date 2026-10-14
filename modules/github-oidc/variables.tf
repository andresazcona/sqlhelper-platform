variable "name" {
  description = "Name prefix, e.g. sqlhelper-prod."
  type        = string
}

variable "github_repository" {
  description = "owner/repo allowed to assume the role."
  type        = string
}

variable "github_environment" {
  description = "GitHub environment the workflow job must run in (dev, staging, prod)."
  type        = string
}

variable "ecr_repository_arn" {
  description = "Repository the workflow pushes to."
  type        = string
}

variable "ecs_service_arn" {
  description = "ECS service being deployed."
  type        = string
}

variable "execution_role_arn" {
  description = "Task execution role referenced by new task definitions."
  type        = string
}

variable "codedeploy_app_arn" {
  description = "CodeDeploy application ARN."
  type        = string
}

variable "codedeploy_deployment_group_arn" {
  description = "CodeDeploy deployment group ARN."
  type        = string
}

variable "frontend_bucket_arn" {
  description = "Bucket the built SPA is synced to."
  type        = string
}

variable "distribution_arn" {
  description = "CloudFront distribution to invalidate."
  type        = string
}
