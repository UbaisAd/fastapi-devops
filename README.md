# FastAPI DevOps Project — CI/CD Deployment on AWS EC2

A containerized Python REST API deployed on AWS EC2 using Docker Compose, Nginx, HTTPS, and GitHub Actions for automated CI/CD.

## 🚀 Live Application

- **Application:** https://devops-fastapi.duckdns.org/
- **Health Check:** https://devops-fastapi.duckdns.org/health
- **API Documentation:** https://devops-fastapi.duckdns.org/docs
- **Demo Endpoint:** https://devops-fastapi.duckdns.org/api/demo

> **Note:** The live URL is available while the AWS EC2 instance is running and correctly configured. Availability is not guaranteed.

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI
- **Containerization:** Docker
- **Container Orchestration:** Docker Compose
- **Reverse Proxy:** Nginx
- **HTTPS:** Let's Encrypt
- **DNS:** DuckDNS
- **Cloud Hosting:** AWS EC2 (Ubuntu 24.04)
- **CI/CD:** GitHub Actions
- **Deployment Runner:** Self-hosted GitHub Actions runner

## 🏗️ Architecture

```text
Developer
    |
    | Git push to main
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    | CI: Build and validate
    v
Self-hosted Runner on AWS EC2
    |
    | Pull latest code
    | Docker Compose build and deploy
    v
Nginx (Ports 80 and 443)
    |
    | HTTPS / Reverse Proxy
    v
FastAPI Application (Port 8000)
```

Nginx handles incoming HTTP and HTTPS requests and forwards API traffic to the FastAPI application. Let's Encrypt provides the TLS certificate.

## ✨ Features

- REST API built with FastAPI
- Dockerized application for consistent deployment
- Docker Compose service management
- Nginx reverse proxy
- HTTPS encryption with Let's Encrypt
- HTTP-to-HTTPS redirection
- Automated CI/CD using GitHub Actions
- Application health-check endpoint
- Automated container rebuild and deployment after successful CI

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application information |
| GET | `/health` | Health status |
| GET | `/api/info` | API and runtime information |
| GET | `/api/demo` | Demonstration response |
| GET | `/docs` | Interactive Swagger API documentation |

## 📂 Project Structure

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

Runtime certificate files and other deployment secrets should not be committed to the repository.

## ⚙️ Run Locally

### Prerequisites

- Python 3.12 or compatible version
- Docker
- Docker Compose
- Git

### 1. Clone the repository

```bash
git clone https://github.com/UbaisAd/fastapi-devops.git
cd fastapi-devops
```

### 2. Start the application

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

**Note:** The production Compose configuration uses Nginx with HTTPS certificates mounted from the EC2 host. For a fresh local setup, configure the required certificates or use a separate development configuration before starting the complete stack.

### 3. Stop the application

```bash
docker compose down
```

## 🔄 CI/CD Workflow

The GitHub Actions workflow automates the deployment process:

1. A developer pushes changes to the `main` branch.
2. GitHub Actions runs the CI build and validation job.
3. After CI succeeds, the deployment job runs on the self-hosted EC2 runner.
4. The runner pulls the latest code from GitHub.
5. Docker Compose builds the updated image and recreates the required containers.
6. The deployment job checks the running containers.

This reduces manual deployment steps and keeps the deployed application synchronized with the repository.

## 🔐 Security Considerations

- HTTPS is configured through Nginx and Let's Encrypt.
- The FastAPI service is exposed internally to the Compose network rather than directly publishing port 8000 on the host.
- Certificate private keys should remain outside version control.
- The EC2 security group should allow only the required inbound ports.
- GitHub Actions runner access and AWS permissions should follow the principle of least privilege.

## 📚 What I Learned

- Building and containerizing a FastAPI application
- Managing services using Docker Compose
- Configuring Nginx as a reverse proxy
- Enabling HTTPS using Let's Encrypt
- Deploying applications to AWS EC2
- Automating builds and deployments using GitHub Actions
- Using a self-hosted runner for deployment
- Verifying application health and container status

## 👨‍💻 Author

**Ubais Ahamed**

- GitHub: https://github.com/UbaisAd

---

*This project demonstrates a basic end-to-end DevOps deployment workflow for a containerized REST API.*
