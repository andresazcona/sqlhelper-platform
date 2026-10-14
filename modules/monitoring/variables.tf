variable "name" {
  description = "Name prefix, e.g. sqlhelper-prod."
  type        = string
}

variable "alb_arn_suffix" {
  description = "ARN suffix of the API load balancer (CloudWatch dimension)."
  type        = string
}

variable "cluster_name" {
  description = "ECS cluster name."
  type        = string
}

variable "service_name" {
  description = "ECS service name."
  type        = string
}

variable "distribution_id" {
  description = "CloudFront distribution ID."
  type        = string
}

variable "alarm_email" {
  description = "Email subscribed to the alarm topic. Empty disables the subscription."
  type        = string
  default     = ""
}
