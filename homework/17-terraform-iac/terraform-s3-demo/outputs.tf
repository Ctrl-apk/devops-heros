output "bucket_id" {
  description = "The name of the bucket"
  value       = aws_s3_bucket.demo_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the bucket"
  value       = aws_s3_bucket.demo_bucket.arn
}

output "bucket_region" {
  description = "The AWS region where bucket resides"
  value       = aws_s3_bucket.demo_bucket.region
}
