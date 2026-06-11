# Art Store Website Demo

A containerized e-commerce demo for an online art store, built as a DevOps-focused full-stack project. The application includes a FastAPI backend, PostgreSQL database, two static Nginx frontends, Docker Compose for local orchestration, Kubernetes manifests for cluster deployment, GitHub Actions CI/CD, and an Argo CD application for GitOps delivery.

## Project Highlights

- Multi-service application with backend, database, seller UI, and user UI
- REST API built with FastAPI, SQLAlchemy, Pydantic, and PostgreSQL
- Static frontend containers served by Nginx
- Dockerized services for repeatable local and container runtime environments
- Kubernetes manifests with Deployments, Services, resource requests, limits, and persistent storage
- GitHub Actions pipeline for linting, testing, image builds, GHCR publishing, and manifest tag updates
- Argo CD Application manifest for automated GitOps sync into Kubernetes

## Architecture

```mermaid
flowchart LR
    Dev[Developer] --> GitHub[GitHub Repository]
    GitHub --> Actions[GitHub Actions CI/CD]
    Actions --> Tests[Lint and Backend Tests]
    Actions --> Images[Build Docker Images]
    Images --> GHCR[GitHub Container Registry]
    Actions --> Manifests[Update Kubernetes Image Tags]
    Manifests --> GitHub

    GitHub --> ArgoCD[Argo CD]
    ArgoCD --> K8s[Kubernetes Cluster]

    subgraph K8s[Kubernetes Namespace: ecommerce-1]
        SellerUI[Seller Frontend<br/>Nginx]
        UserUI[User Frontend<br/>Nginx]
        API[FastAPI Backend<br/>Uvicorn]
        DB[(PostgreSQL 16<br/>PVC Storage)]

        SellerUI --> API
        UserUI --> API
        API --> DB
    end
```

## How It Works

The repository is organized as a small production-style platform rather than a single standalone app.

1. A seller or user opens one of the frontend applications.
2. The static frontend is served from an Nginx container.
3. The frontend calls the FastAPI backend for product and category data.
4. FastAPI routes pass requests through service and repository layers.
5. SQLAlchemy persists and reads data from PostgreSQL.
6. In Kubernetes, each service runs as an independent workload with its own Deployment and Service.
7. Argo CD watches the `k8s/` directory and keeps the cluster synchronized with the Git repository.

## Repository Structure

```text
.
|-- backend/
|   |-- app/
|   |   |-- api/             # API router and route handlers
|   |   |-- core/            # Database configuration
|   |   |-- models/          # SQLAlchemy models
|   |   |-- repository/      # Database access layer
|   |   |-- schemas/         # Pydantic request/response schemas
|   |   `-- services/        # Business logic layer
|   |-- Dockerfile
|   `-- requirements.txt
|-- seller-frontend/
|   |-- Dockerfile
|   `-- index.html
|-- user-frontend/
|   |-- Dockerfile
|   `-- index.html
|-- k8s/
|   |-- application.yaml
|   |-- backend_deployment.yaml
|   |-- db_deployment.yaml
|   |-- seller_frontend_deployment.yaml
|   `-- user_frontend_deployment.yaml
|-- .github/workflows/
|   `-- python-app.yml
|-- docker-compose.yml
`-- README.md
```

## Technology Stack

| Layer | Technology |
| --- | --- |
| Backend API | Python 3.11, FastAPI, Uvicorn |
| ORM and Validation | SQLAlchemy, Pydantic |
| Database | PostgreSQL 16 |
| Frontend Hosting | Static HTML served by Nginx |
| Containerization | Docker, Docker Compose |
| Orchestration | Kubernetes |
| CI/CD | GitHub Actions |
| Registry | GitHub Container Registry |
| GitOps | Argo CD |

## Backend Design

The backend follows a layered FastAPI structure:

- `main.py` creates the FastAPI app, registers routers, enables CORS, and initializes database tables.
- `api/routes/` exposes HTTP endpoints for products and categories.
- `services/` contains the application logic layer.
- `repository/` performs SQLAlchemy session operations.
- `models/` defines database tables.
- `schemas/` defines Pydantic request and response contracts.
- `core/database.py` loads `DATABASE_URL`, creates the SQLAlchemy engine, and provides database sessions.

At startup, the application calls `Base.metadata.create_all(bind=engine)` so the demo database schema is created automatically when the backend starts.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Backend health-style welcome response |
| `POST` | `/products/` | Create a product |
| `GET` | `/products/` | List products |
| `GET` | `/products/{product_id}` | Get product details |
| `PUT` | `/products/{product_id}` | Update a product |
| `DELETE` | `/products/{product_id}` | Delete a product |
| `POST` | `/categories/` | Create a category |
| `GET` | `/categories/` | List categories |
| `GET` | `/categories/{category_id}` | Get category details |

## Data Model

```mermaid
erDiagram
    CATEGORIES ||--o{ PRODUCTS : contains
    CATEGORIES {
        int id
        string name
    }
    PRODUCTS {
        int id
        string title
        string description
        float price
        string image_url
        int stock
        int category_id
    }
```

## Local Development

### Prerequisites

- Python 3.11
- Docker and Docker Compose
- PostgreSQL, if running the backend outside Docker

### Run With Docker Compose

Build the three application images first:

```bash
docker build -t art-shop-backend ./backend
docker build -t art-store-seller-ui ./seller-frontend
docker build -t art-store-user-ui ./user-frontend
```

Start the full stack:

```bash
docker compose up -d
```

Services are exposed locally as:

| Service | URL |
| --- | --- |
| Backend API | `http://localhost:8000` |
| Seller Frontend | `http://localhost:3000` |
| User Frontend | `http://localhost:3001` |

Stop the stack:

```bash
docker compose down
```

### Run Backend Locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:password@localhost:5432/art_store
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

For Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL="postgresql://postgres:password@localhost:5432/art_store"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Containerization

Each application component has a dedicated container image:

- `backend/Dockerfile` packages the FastAPI application with Python 3.11 slim and runs it with Uvicorn.
- `seller-frontend/Dockerfile` packages the seller UI into an Nginx container.
- `user-frontend/Dockerfile` packages the user UI into an Nginx container.
- `docker-compose.yml` wires the backend, PostgreSQL, seller UI, and user UI together for local orchestration.

## Kubernetes Deployment

The `k8s/` directory contains the deployment layer:

| Manifest | Purpose |
| --- | --- |
| `db_deployment.yaml` | Creates namespace, PostgreSQL Deployment, PVC, and ClusterIP Service |
| `backend_deployment.yaml` | Deploys the FastAPI backend with two replicas and a ClusterIP Service |
| `seller_frontend_deployment.yaml` | Deploys seller UI with a NodePort Service |
| `user_frontend_deployment.yaml` | Deploys user UI with a NodePort Service |
| `application.yaml` | Argo CD Application for automated GitOps sync |

Apply the Kubernetes manifests manually:

```bash
kubectl apply -f k8s/
```

Check workloads:

```bash
kubectl get all -n ecommerce-1
```

Frontend NodePorts:

| Frontend | NodePort |
| --- | --- |
| Seller UI | `30001` |
| User UI | `30002` |

## CI/CD Pipeline

GitHub Actions is configured in `.github/workflows/python-app.yml`.

```mermaid
flowchart LR
    Push[Push or PR to main] --> Test[Install, Lint, Test]
    Test --> Coverage[Upload Coverage Artifact]
    Test --> Build[Build Docker Images]
    Build --> PushImages[Push Images to GHCR]
    PushImages --> Update[Update K8s Image Tags]
    Update --> Commit[Commit Updated Manifests]
    Commit --> Argo[Argo CD Syncs Cluster]
```

Pipeline stages:

- Runs on pushes and pull requests to `main`
- Starts a PostgreSQL 16 service container for backend validation
- Installs backend dependencies
- Runs Ruff checks
- Runs Pytest with coverage output
- Builds backend, seller frontend, and user frontend images
- Pushes images to GitHub Container Registry
- Updates Kubernetes manifests with the generated image tag
- Commits updated manifests back to the repository

## GitOps Flow

The Argo CD Application watches the repository path `k8s/` and deploys to the `ecommerce-1` namespace.

The sync policy is automated:

- `selfHeal: true` restores the cluster if live resources drift from Git
- `prune: true` removes resources that are deleted from Git
- `CreateNamespace=true` allows Argo CD to create the target namespace when needed

This makes Git the source of truth for the deployed environment.


For production-style environments, move database credentials into Kubernetes Secrets or an external secret manager.

## DevOps Practices Demonstrated

- Infrastructure-as-code style Kubernetes manifests
- GitOps deployment with Argo CD
- CI validation before image publishing
- Container image build and registry push automation
- Immutable image tagging using commit-derived tags
- Kubernetes resource requests and limits
- Persistent database storage with a PVC
- Separate services for frontend, backend, and database responsibilities


## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.
