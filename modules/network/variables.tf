variable "name" {
  description = "Name prefix for every resource, e.g. sqlhelper-prod."
  type        = string
}

variable "cidr_block" {
  description = "VPC CIDR. Two /20 private subnets are carved from it."
  type        = string
}

variable "single_az_endpoints" {
  description = "Place interface endpoints in one AZ only (halves their cost, non-prod)."
  type        = bool
  default     = false
}
