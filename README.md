# Simple End-to-End MLOps on Google Cloud

This project demonstrates a **production-ready MLOps pipeline** for deploying machine learning models in a **business environment** using **Google Cloud Platform (GCP)**. It provides a scalable, secure, and automated approach for building, versioning, and deploying ML services.

## Business Context

Modern enterprises need **reliable ML pipelines** to:
- Automate model deployment and updates.
- Ensure compliance and security in cloud environments.
- Reduce operational overhead with CI/CD.
- Enable rapid experimentation and delivery of ML-driven features.

This solution is designed for:
- **Data Science Teams**: Focus on model development, not infrastructure.
- **DevOps Teams**: Standardized deployment process.
- **Business Stakeholders**: Faster time-to-market for ML products.

## Key Capabilities
- **Containerized ML Application** for portability and reproducibility.
- **Artifact Registry** for secure image storage and versioning.
- **Automated CI/CD** using GitHub Actions.
- **Timestamped Image Naming** for traceability.
- **Cloud-Native Deployment** (Cloud Run optional).

## Architecture Overview

ML Code → Docker Image → Artifact Registry → (Optional) Cloud Run

- **Source Code**: ML logic and business rules.
- **Dockerization**: Ensures consistent runtime.
- **Artifact Registry**: Centralized image repository.
- **CI/CD Workflow**: Automates build and push.
- **Deployment**: Cloud Run or other GCP services.

## Prerequisites
- **Google Cloud Project** with:
  - Artifact Registry enabled.
  - IAM roles for service account:
    - `roles/artifactregistry.admin` (required for automated repo creation).
    - `roles/storage.objectAdmin`.
- **GitHub Secrets**:
  - `SMPL_E2E_MLOPS_GCP_CREDENTIALS` → Service account JSON key.
  - `SMPL_E2E_MLOPS_GCP_PROJECT_ID` → GCP Project ID.
  - `SMPL_E2E_MLOPS_GCP_REGION` → Artifact Registry region.

## Setup Steps

1. **Enable APIs**:

```shell
   gcloud services enable artifactregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com
```

2. Configure GitHub Secrets for CI/CD.


Repository creation is automated in GitHub Actions if permissions allow.

If permissions are restricted, pre-create the repository manually:

```shell

gcloud artifacts repositories create smpl-e2e-mlops-gcp \
  --repository-format=docker \
  --location=us-east1 \
  --project=YOUR_PROJECT_ID
```

## CI/CD Workflow Highlights

Builds Docker image from devops/dockerBuild/Dockerfile.
Names image as: simple-e2e-mlops-on-gcp-YYYY-MM-DD-HH-MM-SS

### Pushes image to Artifact Registry:

REGION-docker.pkg.dev/PROJECT_ID/smpl-e2e-mlops-gcp/simple-e2e-mlops-on-gcp-YYYY-MM-DD-HH-MM-SS

### Run Workflow
Trigger manually from GitHub Actions:
Actions → GCP Build Push Deploy → Run workflow

### Optional Deployment
Deploy to Cloud Run for serverless execution:
Shellgcloud run deploy smpl-e2e-mlops-gcp-service \  --image REGION-docker.pkg.dev/PROJECT_ID/smpl-e2e-mlops-gcp/simple-e2e-mlops-on-gcp-YYYY-MM-DD-HH-MM-SS \  --region REGION \  --platform managed \  --allow-unauthenticatedShow more lines

### Business Benefits

Scalability: Deploy across regions with GCP services.
Security: Artifact Registry with IAM controls.
Auditability: Timestamped image names for compliance.
Speed: Automated pipeline reduces manual steps.

### Tech Stack

- Google Cloud Platform 
- Artifact Registry 
- Docker 
- GitHub Actions 
- Python (ML code)

## GCP Service Account Permissions Required

To run this MLOps pipeline and associated GitHub Actions workflows, the service account used for CI/CD must have the following IAM roles:
Core Roles for Build & Deploy

```text
roles/artifactregistry.admin – Manage Artifact Registry repositories.
roles/artifactregistry.repoAdmin – Manage artifacts in repositories.
roles/cloudbuild.connectionAdmin – Required for Cloud Build integrations.
roles/clouddeploy.admin – Manage Cloud Deploy resources.
roles/container.admin – Full control over Kubernetes Engine resources.
roles/container.clusterAdmin – Create and manage Kubernetes clusters.
roles/storage.objectAdmin – Read/write access to Cloud Storage objects.
```

### ML & Data Roles

```text
roles/aiplatform.admin – Manage Vertex AI resources.
roles/bigquery.admin – Access and manage BigQuery datasets.
```

### Setup Roles (One-Time Project Initialization)

If you want the same service account to enable APIs and grant roles automatically, it also needs:

```text
roles/serviceusage.serviceUsageAdmin – Enable and manage Google Cloud APIs.
roles/resourcemanager.projectIamAdmin – Grant IAM roles to other accounts.
```

⚠️ Best Practice: Use a separate admin account for initial setup and keep the CI/CD service account limited to build/deploy roles for security.


 Invoke-WebRequest -Uri "http://localhost:5052/upload-parquet" -Method POST
