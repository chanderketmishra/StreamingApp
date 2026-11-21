# StreamingApp — DevOps Graded Project

A MERN-based streaming application organised as a frontend and four backend microservices, with MongoDB as the shared database.

## Project architecture

| Component | Container port | Responsibility |
|---|---:|---|
| Frontend | 80 | React web application |
| Auth service | 3001 | Authentication and user access |
| Streaming service | 3002 | Streaming APIs and catalogue |
| Admin service | 3003 | Administration and asset management |
| Chat service | 3004 | Real-time chat APIs |
| MongoDB | 27017 | Application database |

The Docker Compose configuration builds the five application images and starts MongoDB with the application services.

## Repository layout

- `frontend/` — React application and frontend Dockerfile
- `backend/authService/` — authentication microservice
- `backend/streamingService/` — streaming microservice
- `backend/adminService/` — admin microservice
- `backend/chatService/` — chat microservice
- `docker-compose.yml` — local multi-container configuration
- `helm/streamingapp/` — Helm chart for Kubernetes packaging
- `Jenkinsfile` — Jenkins pipeline to build and push application images to Amazon ECR

## Run locally with Docker Compose

Prerequisites: Docker Engine and Docker Compose.

1. Clone this repository.
2. Create a local `.env` file if you need to override the defaults. Do not commit credentials or production secrets.
3. Build and start the stack:

```bash
docker compose up --build -d
```

4. Open the frontend at `http://localhost:3000`.
5. Check container status and logs:

```bash
docker compose ps
docker compose logs -f
```

Stop the stack:

```bash
docker compose down
```

To remove the local MongoDB volume as well (this deletes local database data):

```bash
docker compose down -v
```

## Environment and secrets

The Compose file supports environment overrides for MongoDB, JWT, AWS S3/CDN and frontend API endpoints. Set the required values in a local, untracked `.env` file or in the deployment platform's secret manager.

**Security:** replace all development defaults such as `JWT_SECRET=changeme` before any shared or production deployment. Never commit AWS access keys, real JWT secrets, database passwords, or populated `.env` files. Prefer an IAM role for AWS workloads instead of long-lived access keys.

The frontend API URLs are build-time values. Set the `REACT_APP_*` variables to addresses reachable by the users' browsers before building the frontend image; `localhost` is only suitable for local development.

## Docker images and Amazon ECR

The project has five application images: `frontend`, `auth`, `streaming`, `admin`, and `chat`. The Jenkins pipeline in the repository builds and pushes these images to the ECR registry configured in the pipeline.

Before running the pipeline, configure the Jenkins agent with Docker CLI/daemon access and AWS CLI, and create a Jenkins username/password credential containing an AWS access key ID and secret access key. Use credential ID `aws-credentials`. The IAM identity must have permission to authenticate to ECR and push to the five repositories in the configured AWS account and region.

Update the registry and region constants in the Jenkinsfile if your AWS account or region differs. Do not put AWS keys in the Jenkinsfile.

## Jenkins CI pipeline

The root-level `Jenkinsfile` provides a declarative pipeline that checks out the configured branch, authenticates to ECR using Jenkins credentials, builds all five Docker images, and pushes them with the `latest` tag.

Configure a Pipeline job to use this repository and the `submission-ready` branch (or merge the file into `main` first). For automatic builds after commits, configure a GitHub webhook to the Jenkins endpoint or enable SCM polling in the Jenkins job. A Jenkinsfile alone does not configure the GitHub webhook.

## Kubernetes and Helm

The Helm chart is in `helm/streamingapp`. Validate and render it locally:

```bash
helm lint helm/streamingapp
helm template streamingapp helm/streamingapp
```

These commands validate chart structure and render Kubernetes manifests locally. They do **not** create a Kubernetes cluster or deploy the application.

**Deployment status:** the chart has been packaged and locally validated. An Amazon EKS cluster and an actual Kubernetes rollout have not been created as part of this repository submission. Before deploying, configure secure Kubernetes Secrets, ECR image-pull permissions, a suitable storage class for MongoDB, reachable frontend API URLs, and an appropriate ingress/load-balancer setup. Do not use the development JWT default in a cluster.

## AWS monitoring

The project work includes CloudWatch EC2 CPU monitoring and centralized Docker application log collection in the `/streamingapp/docker` log group (AWS region `ap-south-1`). The Docker Compose logging driver is configured for the same log group and service-specific streams. Ensure the EC2 instance role has the required CloudWatch Logs permissions and that the log group exists before starting containers with the `awslogs` driver.

## Health checks and validation

The following service health endpoints were used during project verification:

| Component | Endpoint |
|---|---|
| Frontend | `http://localhost:3000` |
| Auth | `http://localhost:3001/health` |
| Streaming | `http://localhost:3002/api/health` |
| Admin | `http://localhost:3003/api/health` |
| Chat | `http://localhost:3004/api/health` |

Use the actual host/port values configured in your environment. A successful local health check confirms the service responds locally; it does not by itself demonstrate Kubernetes deployment or autoscaling.

## Current project scope and limitations

- Dockerfiles and Docker Compose configuration are included for the frontend and four backend services.
- Jenkins pipeline source is included for building and pushing the five application images to ECR; Jenkins credentials, agent prerequisites, job configuration, and webhook/polling must be configured in the Jenkins environment.
- Helm chart packaging and local lint/render validation are included.
- CloudWatch monitoring/logging configuration is documented.
- EKS cluster creation, Helm deployment to a live cluster, and Kubernetes autoscaling/load testing are not claimed as completed.

## Submission evidence

Keep screenshots of successful Docker builds and health checks, Jenkins build output, ECR repositories/images, CloudWatch alarm/log streams, and Helm lint/template output alongside the final project report. Do not include credentials or secret values in screenshots.
