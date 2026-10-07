# AWS S3 (Simple Storage Service) Research

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

---

## 1. What is S3?
Amazon S3 is an object storage service offering industry-leading scalability, data availability, security, and performance.

## 2. Key Concepts

- **Buckets:** Top-level containers for storing objects. Bucket names must be globally unique across AWS.
- **Objects:** Files and metadata stored within buckets.
- **Storage Classes:** 
  - *S3 Standard*: Frequent access.
  - *S3 Intelligent-Tiering*: Auto-cost optimization.
  - *S3 Glacier*: Long-term archival.
- **Versioning:** Keeps multiple variants of an object in the same bucket to protect against accidental deletion.
- **Lifecycle Policies:** Automated rules to transition objects across storage classes or expire old objects.
- **Encryption:** SSE-S3 (AES-256), SSE-KMS, or client-side encryption.
- **Bucket Policies:** JSON access control policies attached directly to buckets.
