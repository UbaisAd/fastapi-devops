# FastAPI DevOps Project

A Python REST API deployed on AWS EC2 using Docker, Docker Compose, Nginx, HTTPS, and GitHub Actions for continuous integration and deployment.

## Live Application

- **Application:** https://devops-fastapi.duckdns.org/
- **Health Check:** https://devops-fastapi.duckdns.org/health
- **API Information:** https://devops-fastapi.duckdns.org/api/info
- **Demo Endpoint:** https://devops-fastapi.duckdns.org/api/demo
- **API Documentation:** https://devops-fastapi.duckdns.org/docs

The application is available while the EC2 instance and its associated services are running.

## Technologies Used

- Python 3.12
- FastAPI
- Docker and Docker Compose
- Nginx reverse proxy
- Let's Encrypt for HTTPS
- DuckDNS for domain configuration
- AWS EC2 running Ubuntu 24.04
- GitHub Actions for CI/CD
- GitHub Container Registry (GHCR)
- GitHub Actions self-hosted runner

## Architecture

### 1. CI/CD and Deployment Flow

```text
+----------------------+
|      Developer       |
|  Code Changes        |
+----------+-----------+
           |
           | git push
           v
+----------------------+
|   GitHub Repository  |
|   main branch        |
+----------+-----------+
           |
           v
+----------------------+
|   GitHub Actions     |
|                      |
|  1. Validate Code    |
|  2. Build Image      |
|  3. Run Checks       |
+----------+-----------+
           |
           | Push image on successful
           | main branch workflow
           v
+----------------------+
| GitHub Container     |
| Registry (GHCR)      |
|                      |
| fastapi-devops:latest|
+----------+-----------+
           |
           | Pull image and deploy
           v
+------------------------------------------------+
|              AWS EC2 Instance                  |
|                Ubuntu Linux                    |
|                                                |
|  +------------------------------------------+  |
|  |             Docker Compose               |  |
|  |                                          |  |
|  |  +------------------------------------+  |  |
|  |  |       Nginx Container              |  |  |
|  |  |                                    |  |  |
|  |  |  - HTTP: Port 80                   |  |  |
|  |  |  - HTTPS: Port 443                 |  |  |
|  |  |  - HTTP to HTTPS redirect          |  |  |
|  |  |  - Reverse proxy                   |  |  |
|  |  +------------------+-----------------+  |  |
|  |                     |                    |  |
|  |                     | Internal Docker    |  |
|  |                     | Network             |  |
|  |                     v                    |  |
|  |  +------------------------------------+  |  |
|  |  |       FastAPI Container            |  |  |
|  |  |                                    |  |  |
|  |  |  Python REST API                   |  |  |
|  |  |          |                         |  |  |
|  |  |          v                         |  |  |
|  |  |  Uvicorn ASGI Server               |  |  |
|  |  |  Internal Port: 8000               |  |  |
|  |  |  Health Check: /health             |  |  |
|  |  +------------------------------------+  |  |
|  |                                          |  |
|  +------------------------------------------+  |
|                                                |
|  AWS Security Group:                           |
|  - Allow inbound TCP 80                        |
|  - Allow inbound TCP 443                       |
|  - No public SSH access                        |
|  - Port 8000 is not publicly exposed           |
|                                                |
|  AWS Systems Manager Session Manager           |
|  Used for administrative access                |
+------------------------------------------------+
```

### 2. Application Request Flow

1. The client sends an HTTP or HTTPS request to `devops-fastapi.duckdns.org`.
2. The AWS security group allows incoming traffic on ports 80 and 443.
3. Nginx receives the request. HTTP requests are redirected to HTTPS.
4. Nginx forwards HTTPS requests to the FastAPI service through the internal Docker network.
5. Uvicorn receives the request on port 8000 and runs the FastAPI application.
6. FastAPI processes the request and returns a JSON response.
7. Uvicorn sends the response back through Nginx to the client.

### 3. CI/CD Deployment Flow

1. The developer pushes code changes to the GitHub repository.
2. GitHub Actions runs the configured validation and build steps.
3. For a successful push to the `main` branch, the workflow publishes the Docker image to GHCR.
4. The self-hosted GitHub Actions runner on EC2 pulls the updated repository and image.
5. Docker Compose recreates the API container using the updated image while keeping the Nginx service configured.
6. The application health check and public API endpoints can be verified after deployment.

### 4. Container Responsibilities

| Component | Responsibility |
|---|---|
| Nginx container | HTTPS termination, HTTP-to-HTTPS redirect, and reverse proxy |
| FastAPI container | REST API endpoints and application logic |
| Uvicorn | ASGI server that runs the FastAPI application |
| Docker Compose | Manages the two containers and their network |
| GHCR | Stores published Docker images |
| GitHub Actions | Automates validation, image publishing, and deployment |
| AWS EC2 | Hosts the Docker-based deployment |

**Security note:** The application port 8000 is not published directly to the public network. Nginx reaches the FastAPI service over the internal Docker network.

## Features

- REST API built with FastAPI
- Containerized application using Docker
- Service management with Docker Compose
- Nginx reverse proxy
- HTTPS with Let's Encrypt
- Automatic HTTP-to-HTTPS redirection
- Automated image publishing to GHCR
- GitHub Actions CI/CD pipeline
- Application health-check endpoint
- Non-root application user inside the Docker container
- Container health check and restart policy
- Internal-only FastAPI port

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns application information |
| GET | `/health` | Returns the application health status |
| GET | `/api/info` | Returns application and runtime information |
| GET | `/api/demo` | Returns a demonstration response |
| GET | `/docs` | Opens the interactive Swagger API documentation |

## Project Structure

```text
fastapi-devops/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── app/
│   └── main.py
├── nginx/
│   └── default.conf
├── Dockerfile
├── compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

The repository contains the application source code, Docker configuration, Nginx configuration, CI/CD workflow, and project documentation. Production TLS certificates and private keys are maintained on the server and should not be committed to Git.

## Running Locally

### Prerequisites

Install the following tools before running the application:

- Python 3.12 or a compatible version
- Docker
- Docker Compose
- Git

### Clone the repository

```bash
git clone https://github.com/UbaisAd/fastapi-devops.git
cd fastapi-devops
```

### Build the Docker image

```bash
docker build -t fastapi-devops:local .
```

### Run the API container

```bash
docker run -d --name fastapi-local -p 8000:8000 fastapi-devops:local
```

Verify the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"healthy"}
```

Open `http://localhost:8000/docs` to access the API documentation.

Stop and remove the local container when finished:

```bash
docker rm -f fastapi-local
```

The production Docker Compose configuration includes Nginx and mounts TLS certificates from the server. For local testing, the API-only Docker commands above avoid the need to configure production certificates.

## Docker Image Publishing

The application image is published to GitHub Container Registry.

Image reference:

`ghcr.io/ubaisad/fastapi-devops:latest`

The GitHub Actions workflow builds and publishes the image when changes are pushed to the `main` branch. The repository's workflow permissions must allow package publishing.

To pull the public image manually:

```bash
docker pull ghcr.io/ubaisad/fastapi-devops:latest
```

The `latest` tag refers to the most recently published image. For production rollback, use a known-good image digest or versioned tag rather than relying on `latest`.

## CI/CD Workflow

The GitHub Actions workflow automates application validation, image publishing, and deployment.

1. A developer pushes changes to the `main` branch.
2. GitHub Actions checks out the repository and installs the Python dependencies.
3. The workflow validates that the FastAPI application can be imported and builds the Docker image.
4. On pushes to `main`, the workflow authenticates to GHCR using the GitHub-provided token and publishes the image.
5. After the CI job succeeds, the deployment job runs on the self-hosted runner on EC2.
6. The runner pulls the latest repository changes and the published API image.
7. Docker Compose updates the application services.
8. The workflow checks the service status.

Pull requests run the CI validation and image build without publishing or deploying the image. Deployment occurs only for pushes to `main` after the required CI job succeeds.

## Deployment on AWS EC2

The application runs on an Ubuntu EC2 instance. The self-hosted GitHub Actions runner performs the deployment, while Docker Compose manages the API and Nginx services.

Connect to the instance using AWS Systems Manager Session Manager or another approved administration method.

Navigate to the project directory:

```bash
cd /home/ubuntu/fastapi-devops
```

Check the service status:

```bash
sudo docker compose ps
```

Pull the latest API image:

```bash
sudo docker compose pull api
```

Apply the deployment:

```bash
sudo docker compose up -d
```

Check the services again:

```bash
sudo docker compose ps
```

These commands are also useful for manual recovery. Under normal operation, GitHub Actions performs the deployment automatically.

## Verification

Verify the public endpoints using a browser or `curl`.

```bash
curl -fsS https://devops-fastapi.duckdns.org/
curl -fsS https://devops-fastapi.duckdns.org/health
curl -fsS https://devops-fastapi.duckdns.org/api/info
curl -fsS https://devops-fastapi.duckdns.org/api/demo
```

A successful health check returns:

```json
{"status":"healthy"}
```

Check the HTTPS certificate in the browser or inspect it with:

```bash
curl -Iv https://devops-fastapi.duckdns.org/
```

The API should be reachable through Nginx over HTTPS. The FastAPI container listens on port 8000 inside the Docker network and is not directly exposed to the public internet.

## Logs and Troubleshooting

### Check container status

```bash
sudo docker compose ps
```

### View API logs

```bash
sudo docker compose logs --tail=100 api
```

### View Nginx logs

```bash
sudo docker compose logs --tail=100 nginx
```

### Follow logs in real time

```bash
sudo docker compose logs -f
```

### Common issues

**The API is unhealthy**

Check the API container logs and health status. Confirm that the application starts successfully and that the `/health` endpoint responds correctly inside the container.

**The website returns a 502 Bad Gateway**

Check that the API container is running and that Nginx can reach the API service through the Docker network. Review the Nginx and API logs.

**HTTPS is not working**

Check DNS resolution, certificate validity, Nginx configuration, and the EC2 security group. Confirm that inbound ports 80 and 443 are allowed.

**The GitHub Actions workflow fails**

Review the failed job's logs. Check the CI output, GHCR permissions, runner availability, and Docker Compose errors before rerunning the workflow.

**The deployment cannot pull the image**

Verify the image name and tag, registry visibility, network connectivity, and registry authentication if required.

Keep port 8000 private. Public application traffic should enter through Nginx on ports 80 and 443.

## Rollback and Recovery

If a new deployment fails, inspect the GitHub Actions logs and the running containers before making further changes.

A reliable rollback requires a previously working image digest or versioned tag. The mutable `latest` tag alone does not identify a specific historical version.

1. Identify the last known-good image digest or versioned tag from GHCR.
2. Update the API image reference in `compose.yml` to that known-good version.
3. Pull the selected image and recreate the API service.
4. Check the container health and test the public endpoints.
5. After resolving the issue, restore the normal deployment configuration.

For example, after setting the API service to the intended known-good image:

```bash
sudo docker compose pull api
sudo docker compose up -d
sudo docker compose ps
```

Verify the health endpoint before considering the rollback complete. Record the known-good image reference and the reason for the rollback so that the recovery can be repeated if necessary.

## Security Considerations

- HTTPS is configured through Nginx and Let's Encrypt.
- The FastAPI service is accessible internally through the Docker network.
- The application runs as a non-root user inside the container.
- Docker health checks help identify an unhealthy application container.
- Container restart policies help services recover after certain failures.
- Production TLS certificates and private keys are excluded from version control.
- The EC2 security group should expose only the required inbound ports, such as 80 and 443.
- Administrative access should use an approved secure method, such as AWS Systems Manager Session Manager.
- GitHub Actions permissions and AWS IAM permissions should follow the principle of least privilege.
- Secrets and access tokens must not be committed to the repository or printed in workflow logs.

## AWS Cleanup

When evaluation is complete and the application is no longer needed, remove or stop the AWS resources that are no longer required.

1. Capture the required screenshots and save the submission evidence.
2. Stop or terminate the EC2 instance when it is safe to take the application offline.
3. Review related EBS volumes, snapshots, Elastic IP addresses, and other billable resources.
4. Delete only resources that are no longer required and are safe to remove.
5. Review AWS billing to check for remaining charges.

Stopping or terminating an instance does not necessarily remove every billable resource. Check the AWS console before considering cleanup complete.

Keep the GitHub repository and container image available if they are required for evaluation.

## What I Learned

Through this project, I practiced:

- Building and containerizing a Python REST API
- Managing application services with Docker Compose
- Configuring Nginx as a reverse proxy
- Setting up HTTPS with Let's Encrypt
- Deploying an application on AWS EC2
- Publishing container images to GHCR
- Automating validation and deployment with GitHub Actions
- Using a self-hosted runner for deployment
- Verifying application health and reviewing container logs
- Documenting deployment, troubleshooting, and recovery procedures

## Author

**Ubais Ahamed**

- GitHub: https://github.com/UbaisAd
- Repository: https://github.com/UbaisAd/fastapi-devops

---

This project demonstrates an end-to-end deployment workflow for a containerized REST API using cloud infrastructure, container tooling, HTTPS, and automated CI/CD.
