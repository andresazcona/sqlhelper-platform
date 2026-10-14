variable "domain_name" {
  description = "Public FQDN of the app. A Route 53 hosted zone with this name must exist in the account."
  type        = string
}

variable "github_repository" {
  description = "owner/repo whose deploy workflow may assume the deploy role."
  type        = string
}

variable "alarm_email" {
  description = "Email for alarm notifications. Empty disables the subscription."
  type        = string
  default     = ""
}
