# AWS IAM (Identity and Access Management) Research

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

---

## 1. What is IAM?
AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS resources. You use IAM to control who is authenticated (signed in) and authorized (has permissions) to use resources.

## 2. Key Concepts

- **IAM Users:** An identity created in AWS that represents a person or application interacting with AWS (e.g., `shifa-dev`).
- **IAM Groups:** A collection of IAM users. Groups let you specify permissions for multiple users at once (e.g., `developers-group`).
- **IAM Roles:** An identity with specific permissions that can be assumed by anyone who needs it (or by AWS services like EC2 or Lambda).
- **Policies:** JSON documents defining explicit permissions (Allow or Deny actions on specific resources).
- **Permissions:** Fine-grained access rights granted via policies attached to users, groups, or roles.

## 3. Principle of Least Privilege
Always grant users **only** the permissions required to perform their specific duties, and no more.

## 4. IAM Best Practices
- Lock down AWS Account Root User (enable MFA, don't use for daily tasks).
- Prefer IAM Roles over static Access Keys (`AWS_ACCESS_KEY_ID`).
- Use IAM Groups to assign permissions rather than individual user attachments.
- Regularly rotate security credentials.
