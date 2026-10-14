output "vpc_id" {
  value = aws_vpc.this.id
}

output "vpc_cidr" {
  value = aws_vpc.this.cidr_block
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "s3_prefix_list_id" {
  description = "Prefix list of the S3 gateway endpoint, for task egress rules (ECR layers live in S3)."
  value       = aws_vpc_endpoint.s3.prefix_list_id
}
