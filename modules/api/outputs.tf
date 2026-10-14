output "alb_arn" {
  value = aws_lb.api.arn
}

output "alb_dns_name" {
  value = aws_lb.api.dns_name
}

output "alb_arn_suffix" {
  value = aws_lb.api.arn_suffix
}

output "cluster_name" {
  value = aws_ecs_cluster.this.name
}

output "service_name" {
  value = aws_ecs_service.api.name
}

output "service_arn" {
  value = aws_ecs_service.api.id
}

output "execution_role_arn" {
  value = aws_iam_role.execution.arn
}

output "codedeploy_app_arn" {
  value = aws_codedeploy_app.api.arn
}

output "codedeploy_deployment_group_arn" {
  value = aws_codedeploy_deployment_group.api.arn
}
