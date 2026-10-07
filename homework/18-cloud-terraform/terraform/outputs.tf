output "vpc_id" {
  value = aws_vpc.main.id
}

output "subnet_id" {
  value = aws_subnet.public.id
}

output "ec2_public_ip" {
  value = aws_instance.web_server.public_ip
}

output "s3_bucket_arn" {
  value = aws_s3_bucket.app_storage.arn
}
