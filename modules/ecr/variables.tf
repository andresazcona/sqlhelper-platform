variable "name" {
  description = "Repository name."
  type        = string
}

variable "keep_images" {
  description = "Images retained by the lifecycle policy (rollback window)."
  type        = number
  default     = 30
}
