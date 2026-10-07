# Task 1: Terraform S3 Demo

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

---

## Terraform Workflow Commands & Log

### 1. `terraform init`
Initializes working directory and downloads HashiCorp AWS Provider plugins.
```bash
terraform init
```

### 2. `terraform fmt`
Formats HCL configuration files into standard canonical format.
```bash
terraform fmt
```

### 3. `terraform validate`
Validates syntax and internal consistency of configuration files.
```bash
terraform validate
# Output: Success! The configuration is valid.
```

### 4. `terraform plan`
Creates an execution plan showing actions to reach desired infrastructure state.
```bash
terraform plan
# Output: Plan: 2 to add, 0 to change, 0 to destroy.
```

### 5. `terraform apply`
Executes planned changes to provision AWS S3 bucket and versioning config.
```bash
terraform apply -auto-approve
# Output: Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

### 6. `terraform show` & `terraform output`
Inspect state and output values.
```bash
terraform output
# Output:
# bucket_arn = "arn:aws:s3:::devops-hero-shifa-s3-bucket-2026"
# bucket_id = "devops-hero-shifa-s3-bucket-2026"
```

### 7. `terraform destroy`
Destroys managed infrastructure resources safely.
```bash
terraform destroy -auto-approve
# Output: Destroy complete! Resources: 2 destroyed.
```
