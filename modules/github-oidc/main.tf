terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

# One provider per account; each environment lives in its own account.
resource "aws_iam_openid_connect_provider" "github" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}

data "aws_iam_policy_document" "trust" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # Only jobs bound to this GitHub environment (and its protection rules) get in.
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repository}:environment:${var.github_environment}"]
    }
  }
}

resource "aws_iam_role" "deploy" {
  name                 = "${var.name}-github-deploy"
  assume_role_policy   = data.aws_iam_policy_document.trust.json
  max_session_duration = 3600
}

# Exactly what deploy.yml does, scoped to this environment's resources.
data "aws_iam_policy_document" "deploy" {
  statement {
    sid       = "EcrLogin"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"] # account-level call, no resource ARN exists
  }

  statement {
    sid = "EcrPush"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:BatchGetImage",
      "ecr:CompleteLayerUpload",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart",
    ]
    resources = [var.ecr_repository_arn]
  }

  statement {
    sid       = "TaskDefinitions"
    actions   = ["ecs:DescribeTaskDefinition", "ecs:RegisterTaskDefinition"]
    resources = ["*"] # these actions do not support resource-level permissions
  }

  statement {
    sid       = "EcsService"
    actions   = ["ecs:DescribeServices"]
    resources = [var.ecs_service_arn]
  }

  statement {
    sid       = "PassExecutionRole"
    actions   = ["iam:PassRole"]
    resources = [var.execution_role_arn]

    condition {
      test     = "StringEquals"
      variable = "iam:PassedToService"
      values   = ["ecs-tasks.amazonaws.com"]
    }
  }

  statement {
    sid       = "CodeDeployRevision"
    actions   = ["codedeploy:RegisterApplicationRevision"]
    resources = [var.codedeploy_app_arn]
  }

  statement {
    sid       = "CodeDeployDeployment"
    actions   = ["codedeploy:CreateDeployment", "codedeploy:GetDeployment", "codedeploy:GetDeploymentGroup"]
    resources = [var.codedeploy_deployment_group_arn]
  }

  statement {
    sid       = "CodeDeployConfig"
    actions   = ["codedeploy:GetDeploymentConfig"]
    resources = ["arn:aws:codedeploy:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:deploymentconfig:*"]
  }

  statement {
    sid       = "FrontendList"
    actions   = ["s3:ListBucket"]
    resources = [var.frontend_bucket_arn]
  }

  statement {
    sid       = "FrontendWrite"
    actions   = ["s3:PutObject", "s3:DeleteObject"]
    resources = ["${var.frontend_bucket_arn}/*"]
  }

  statement {
    sid       = "Invalidate"
    actions   = ["cloudfront:CreateInvalidation"]
    resources = [var.distribution_arn]
  }
}

resource "aws_iam_role_policy" "deploy" {
  name   = "deploy"
  role   = aws_iam_role.deploy.id
  policy = data.aws_iam_policy_document.deploy.json
}
