variable "name" {
  description = "Name prefix, e.g. sqlhelper-prod. Also the ECS cluster name."
  type        = string
}

variable "vpc_id" {
  description = "VPC of the service."
  type        = string
}

variable "vpc_cidr" {
  description = "Task egress to interface endpoints is limited to this CIDR."
  type        = string
}

variable "subnet_ids" {
  description = "Private subnets (two AZs) for the ALB and the tasks."
  type        = list(string)
}

variable "s3_prefix_list_id" {
  description = "S3 gateway endpoint prefix list, needed to pull ECR image layers."
  type        = string
}

variable "repository_url" {
  description = "ECR repository URL of the API image."
  type        = string
}

variable "app_origin" {
  description = "Public origin of the app (https://domain), passed to the API as CORS_ORIGIN."
  type        = string
}

variable "cpu" {
  description = "Fargate task CPU units."
  type        = number
}

variable "memory" {
  description = "Fargate task memory in MiB."
  type        = number
}

variable "min_count" {
  description = "Minimum (and initial) number of tasks."
  type        = number
}

variable "max_count" {
  description = "Maximum number of tasks. Equal to min_count disables autoscaling."
  type        = number
}

variable "deployment_config_name" {
  description = "CodeDeploy ECS config, e.g. CodeDeployDefault.ECSAllAtOnce or CodeDeployDefault.ECSCanary10Percent5Minutes."
  type        = string
}

variable "rollback_alarm_names" {
  description = "CloudWatch alarms that stop and roll back a deployment."
  type        = list(string)
}

variable "log_retention_days" {
  description = "Retention of the API log group."
  type        = number
}

variable "deletion_protection" {
  description = "ALB deletion protection."
  type        = bool
  default     = false
}
