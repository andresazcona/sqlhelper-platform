output "url" {
  value = module.edge.url
}

output "github_environment_variables" {
  description = "Copy into the GitHub environment of the same name; deploy.yml reads them."
  value = {
    AWS_ROLE_ARN               = module.github_oidc.role_arn
    FRONTEND_BUCKET            = module.edge.frontend_bucket_name
    CLOUDFRONT_DISTRIBUTION_ID = module.edge.distribution_id
  }
}
