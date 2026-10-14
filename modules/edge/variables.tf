variable "name" {
  description = "Name prefix, e.g. sqlhelper-prod."
  type        = string
}

variable "domain_name" {
  description = "App FQDN. A Route 53 public hosted zone with this exact name must exist in the account."
  type        = string
}

variable "alb_arn" {
  description = "Internal ALB exposed through the CloudFront VPC origin."
  type        = string
}

variable "alb_dns_name" {
  description = "DNS name of the internal ALB."
  type        = string
}

variable "price_class" {
  description = "CloudFront price class."
  type        = string
  default     = "PriceClass_100"
}
