output "role_arn" {
  description = "Set as the AWS_ROLE_ARN variable of the matching GitHub environment."
  value       = aws_iam_role.deploy.arn
}
