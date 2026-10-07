variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Name of the AWS S3 bucket"
  type        = string
  default     = "devops-hero-shifa-s3-demo"
}

variable "environment" {
  description = "Deployment environment tag"
  type        = string
  default     = "dev"
}
