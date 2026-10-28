# Review System CI/CD Project

An end-to-end, production-grade DevOps CI/CD pipeline and web application built from absolute scratch. This project demonstrates modern cloud-native engineering principles: a responsive Python Flask microservice, automated unit & integration testing via pytest, multi-version container packaging with Docker, automated continuous integration & deployment pipelines in Jenkins, and resilient orchestration on Kubernetes.

---

## 📑 Table of Contents
1. [Project Overview & Objectives](#project-overview--objectives)
2. [Key Features Across Versions (V1, V2, V3)](#key-features-across-versions-v1-v2-v3)
3. [Technology Stack](#technology-stack)
4. [Complete Project Structure](#complete-project-structure)
5. [Local Development & Python Setup](#local-development--python-setup)
6. [Automated Testing with Pytest](#automated-testing-with-pytest)
7. [Git & GitHub Branching Strategy](#git--github-branching-strategy)
8. [Docker Containerization](#docker-containerization)
9. [Docker Hub Configuration & Authentication](#docker-hub-configuration--authentication)
10. [Jenkins CI/CD Pipeline](#jenkins-cicd-pipeline)
11. [Kubernetes Orchestration & Probes](#kubernetes-orchestration--probes)
12. [Port-Forwarding & Localhost Access](#port-forwarding--localhost-access)
13. [Troubleshooting & Common Errors](#troubleshooting--common-errors)
14. [Design Decisions & Known Limitations](#design-decisions--known-limitations)
15. [Viva & Project Review Presentation Guide](#viva--project-review-presentation-guide)

---

## 🎯 Project Overview & Objectives

### Introduction
The **Review System** is a customer feedback management system designed to showcase how software evolves through progressive feature rollouts and automated delivery pipelines. Rather than presenting static code, this repository implements three distinct, functional application versions (`v1`, `v2`, `v3`) managed under Git, containerized into independent Docker images, and deployed to Kubernetes using Jenkins automation.

### Academic & Technical Objectives
- **Modern Web Application Architecture:** Build a modular Flask application adhering to Model-View-Template separation (Python backend, Jinja2 templates, modern responsive CSS).
- **Test-Driven Reliability:** Guarantee zero-defect delivery by executing an automated test suite before every image build.
- **Immutable Containerization:** Package each release into reproducible, minimal Docker container images based on `python:3.11-slim`.
- **Automated CI/CD:** Orchestrate linting, testing, multi-version image construction, secure Docker Hub publishing, and Kubernetes manifest validation inside Jenkins.
- **Zero-Downtime Microservices:** Deploy each version onto a Kubernetes cluster with dedicated services, readiness/liveness health probes, and independent host port forwards.

---

## 🌟 Key Features Across Versions (V1, V2, V3)

Each version is visibly distinguishable in browser presentation and functionally distinct:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        REVIEW SYSTEM VERSIONS                          │
├─────────────────┬──────────────────────────┬───────────────────────────┤
│   Version 1.0   │       Version 2.0        │        Version 3.0        │
│  (Classic Blue) │     (Modern Emerald)     │      (Royal Purple)       │
├─────────────────┼──────────────────────────┼───────────────────────────┤
│ • Feedback Form │ • All V1 capabilities    │ • All V1 & V2 capabilities│
│ • Input Checks  │ • Dynamic Star Filter    │ • Multi-Criteria Sorting  │
│ • Live Reviews  │ • Total Reviews Counter  │ • Rating Histogram Bar    │
│ • /health API   │ • Average Score (/5.0)   │ • Positive Sentiment %    │
│ • Version Badge │ • 5-Star Volume Tracker  │ • Enhanced Theme Styling  │
└─────────────────┴──────────────────────────┴───────────────────────────┘
```

- **Version 1 (`v1`):**
  - Classic Blue corporate UI theme.
  - Reviewer name, 1–5 star rating dropdown, and review comment fields.
  - Strict input validation (rejects empty fields, ratings outside 1–5, comments > 500 chars).
  - Live customer reviews feed with timestamps and avatar badges.
  - Operational health endpoint at `/health`.

- **Version 2 (`v2`):**
  - Vibrant Emerald Green UI theme.
  - **Dynamic Rating Filter:** Instant client-side / query-based filtering (Show All, 5★, 4★, 3★, 2★, 1★).
  - **Analytics Cards:** Total review count, mathematical average rating (e.g. `4.7 / 5.0`), and 5-star count.

- **Version 3 (`v3`):**
  - Royal Violet / Indigo modern UI theme.
  - **Multi-Criteria Sorting:** Sort reviews dynamically by *Newest First*, *Oldest First*, *Highest Rated*, or *Lowest Rated*.
  - **Visual Distribution Bar:** Graphical percentage histogram breakdown for each star level (5★ down to 1★).
  - **Sentiment Metric:** Real-time positive sentiment calculation (percentage of 4★ and 5★ ratings).

---

## 🛠 Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Backend Language** | Python | 3.11+ | Core application runtime |
| **Web Framework** | Flask | 3.1.3 | Routing, request validation, Jinja2 template rendering |
| **Test Framework** | Pytest | 8.4.2 | Automated unit and integration endpoint tests |
| **Container Engine** | Docker Desktop | 29.8+ | Multi-stage image building, container virtualization |
| **Image Registry** | Docker Hub | Cloud | Public registry storing `mmokshitha/review-system` tags |
| **CI/CD Automation** | Jenkins | 2.500+ | Declarative pipeline orchestrating builds and pushes |
| **Container Orchestration**| Kubernetes (kind/Docker) | v1.36.1 | Declarative deployments, pods, and service networking |
| **Version Control** | Git & GitHub | 2.55+ | SCM repository, commit tracking, and branching |

---

## 📂 Complete Project Structure

```text
review-system-from-scratch/
│
├── app.py                     # Main Flask web application and REST API
├── requirements.txt           # Python application dependencies (Flask, pytest)
├── test_app.py                # Automated pytest unit and integration test suite
├── Dockerfile                 # Optimized multi-version Docker container recipe
├── .dockerignore              # Files excluded from Docker build context
├── .gitignore                 # Files excluded from Git version control
├── Jenkinsfile                # 9-stage declarative CI/CD pipeline definition
├── README.md                  # Comprehensive project documentation (this file)
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Base HTML layout with version theming and navigation
│   ├── index.html             # Main dashboard (form, statistics, reviews, filters)
│   └── reviews.html           # Dedicated full-page review registry
│
├── static/                    # Frontend stylesheet assets
│   └── style.css              # Responsive modern stylesheet with dynamic CSS variables
│
├── k8s/                       # Kubernetes deployment and service manifests
│   ├── v1-deployment.yaml     # Kubernetes Deployment manifest for Version 1
│   ├── v1-service.yaml        # Kubernetes NodePort Service manifest for Version 1
│   ├── v2-deployment.yaml     # Kubernetes Deployment manifest for Version 2
│   ├── v2-service.yaml        # Kubernetes NodePort Service manifest for Version 2
│   ├── v3-deployment.yaml     # Kubernetes Deployment manifest for Version 3
│   └── v3-service.yaml        # Kubernetes NodePort Service manifest for Version 3
│
└── screenshots/               # College assignment demonstration assets
    └── README.md              # Screenshot catalog and submission instructions
```

---

## 💻 Local Development & Python Setup

### Prerequisites
Ensure Python 3.11+ is installed. On Windows, verify using PowerShell:
```powershell
python --version
```

### Installation
1. Clone or navigate to the project root:
   ```powershell
   cd C:\Users\MOKSHITHA\Downloads\review-system-from-scratch
   ```

2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Run the application locally:
   ```powershell
   # Default runs Version 1:
   python app.py

   # To test Version 2 locally:
   $env:APP_VERSION="v2"; python app.py

   # To test Version 3 locally:
   $env:APP_VERSION="v3"; python app.py
   ```

4. Open your browser and navigate to:
   - Web Interface: [http://127.0.0.1:5000](http://127.0.0.1:5000)
   - Health Probe: [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health)

---

## 🧪 Automated Testing with Pytest

All endpoints and validation rules are covered by automated tests in `test_app.py`. The tests utilize Flask's native test client, guaranteeing fast, isolated, and repeatable test execution without launching an external server.

### Execute Tests
Run pytest in verbose mode:
```powershell
python -m pytest -v
```

### Test Suite Coverage
```text
test_app.py::test_home_page_returns_200                     PASSED
test_app.py::test_health_endpoint_is_healthy                PASSED
test_app.py::test_health_endpoint_includes_version          PASSED
test_app.py::test_submit_valid_review_redirects_and_saves   PASSED
test_app.py::test_invalid_review_missing_name_rejected      PASSED
test_app.py::test_invalid_review_missing_comment_rejected   PASSED
test_app.py::test_invalid_review_out_of_range_rating_rejected PASSED
test_app.py::test_reviews_page_returns_200                 PASSED
test_app.py::test_statistics_calculation_accuracy           PASSED
```

---

## 🌿 Git & GitHub Branching Strategy

The repository follows a clean Git workflow where `main` acts as the primary trunk, supported by dedicated release branches for each feature milestone:

- `main`: Production-ready trunk with the complete multi-version application, Dockerfile, Jenkinsfile, and Kubernetes manifests.
- `v1`: Branch representing the initial Release 1.0 codebase.
- `v2`: Branch introducing rating filtering and aggregate statistics.
- `v3`: Branch introducing sorting algorithms and visual sentiment distribution.

### Git Commands
```powershell
# Stage all tracked and untracked project files
git add .

# Commit with a descriptive message
git commit -m "feat: complete review system with templates, v1-v3 versions, docker, and k8s"

# Push main to GitHub
git push origin main

# Create and push release branches
git branch -M v1
git push -u origin v1

git branch -M v2
git push -u origin v2

git branch -M v3
git push -u origin v3

# Return to main
git checkout main
```

---

## 🐳 Docker Containerization

The project uses a single, optimized `Dockerfile` leveraging Docker build arguments (`--build-arg APP_VERSION=...`) to build version-tagged images from the same codebase without code duplication.

### Build All Images
```powershell
docker build --build-arg APP_VERSION=v1 -t mmokshitha/review-system:v1 .
docker build --build-arg APP_VERSION=v2 -t mmokshitha/review-system:v2 .
docker build --build-arg APP_VERSION=v3 -t mmokshitha/review-system:v3 .
```

### Run and Verify Containers Concurrently
```powershell
# Run v1 on host port 5001
docker run -d --name review-v1 -p 5001:5000 mmokshitha/review-system:v1

# Run v2 on host port 5002
docker run -d --name review-v2 -p 5002:5000 mmokshitha/review-system:v2

# Run v3 on host port 5003
docker run -d --name review-v3 -p 5003:5000 mmokshitha/review-system:v3
```

### Verify Endpoints
```powershell
curl.exe http://127.0.0.1:5001/health  # {"status":"healthy","version":"v1"}
curl.exe http://127.0.0.1:5002/health  # {"status":"healthy","version":"v2"}
curl.exe http://127.0.0.1:5003/health  # {"status":"healthy","version":"v3"}
```

---

## 🔐 Docker Hub Configuration & Authentication

### Security Best Practice
In modern DevOps, never hard-code plaintext credentials or regular account passwords. Always generate a **Personal Access Token (PAT)**:
1. Log in to [Docker Hub](https://hub.docker.com/).
2. Navigate to **Account Settings** &rarr; **Security** &rarr; **Personal access tokens**.
3. Generate a token with **Read & Write** permissions named `jenkins-ci-token`.
4. Copy the generated token string (`dckr_pat_...`).

### Jenkins Credential Setup
1. In Jenkins dashboard, go to: **Manage Jenkins** &rarr; **Credentials** &rarr; **System** &rarr; **Global credentials (unrestricted)**.
2. Click **+ Add Credentials**.
3. Select **Kind**: `Secret text`.
4. Set **ID**: `dockerhub-token`.
5. In **Secret**, paste your Docker Hub Personal Access Token.
6. Set **Description**: `Docker Hub PAT for mmokshitha`.
7. Click **Create**.

---

## ⚙️ Jenkins CI/CD Pipeline

The `Jenkinsfile` defines a 9-stage Declarative Pipeline designed specifically for a Windows agent:

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐
│ 1. Checkout  │ ──> │2. Check Tools│ ──> │3.Install Dependencies│
└──────────────┘     └──────────────┘     └──────────────────────┘
                                                     │
                                                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐
│ 6. Build V2  │ <── │ 5. Build V1  │ <── │     4. Run Tests     │
└──────────────┘     └──────────────┘     └──────────────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ 7. Build V3  │ ──> │ 8. Push to DockerHub │ ──> │ 9. Validate K8s YAML │
└──────────────┘     └──────────────────────┘     └──────────────────────┘
```

### Pipeline Stages
1. **Checkout:** Clones the latest commit from `https://github.com/mokshitha31vs-mok/review_system.git`.
2. **Check Tools:** Confirms Python 3.11, Docker Desktop daemon, and kubectl are operational.
3. **Install Dependencies:** Executes `pip install -r requirements.txt`.
4. **Run Tests:** Executes `pytest -v`. Halts immediately if any test fails.
5. **Build V1 Image:** Builds `mmokshitha/review-system:v1`.
6. **Build V2 Image:** Builds `mmokshitha/review-system:v2`.
7. **Build V3 Image:** Builds `mmokshitha/review-system:v3`.
8. **Login and Push to Docker Hub:** Decrypts `dockerhub-token`, executes secure stdin authentication, pushes all 3 tags, and logs out.
9. **Validate Kubernetes Manifests:** Runs `kubectl apply --dry-run=client -f k8s/` to catch YAML or schema errors before cluster deployment.

---

## ☸️ Kubernetes Orchestration & Probes

The project includes 6 independent Kubernetes manifests in `k8s/`:

| File | Resource | Details |
|---|---|---|
| `v1-deployment.yaml` | Deployment | Replicas: 1, Image: `mmokshitha/review-system:v1`, Readiness/Liveness Probes on `/health` |
| `v1-service.yaml` | Service (NodePort) | Port: 5000, TargetPort: 5000, NodePort: 31081, Selector: `app: review-system-v1` |
| `v2-deployment.yaml` | Deployment | Replicas: 1, Image: `mmokshitha/review-system:v2`, Readiness/Liveness Probes on `/health` |
| `v2-service.yaml` | Service (NodePort) | Port: 5000, TargetPort: 5000, NodePort: 31082, Selector: `app: review-system-v2` |
| `v3-deployment.yaml` | Deployment | Replicas: 1, Image: `mmokshitha/review-system:v3`, Readiness/Liveness Probes on `/health` |
| `v3-service.yaml` | Service (NodePort) | Port: 5000, TargetPort: 5000, NodePort: 31083, Selector: `app: review-system-v3` |

### Deploy to Cluster
```powershell
kubectl apply -f k8s/
```

### Verify Deployment Status
```powershell
kubectl get deployments
kubectl get pods
kubectl get services
```

---

## 🌐 Port-Forwarding & Localhost Access

To demonstrate and test all three running versions simultaneously on Windows:

### Port-Forwarding Commands
Run each command in its own dedicated PowerShell terminal window:

```powershell
# Terminal 1 — Version 1
kubectl port-forward service/review-system-v1-service 18081:5000

# Terminal 2 — Version 2
kubectl port-forward service/review-system-v2-service 18082:5000

# Terminal 3 — Version 3
kubectl port-forward service/review-system-v3-service 18083:5000
```

### URLs to Access and Demonstrate
- **Version 1 (Classic Blue):**
  - Application: [http://localhost:18081](http://localhost:18081)
  - Health: [http://localhost:18081/health](http://localhost:18081/health)
- **Version 2 (Modern Emerald):**
  - Application: [http://localhost:18082](http://localhost:18082)
  - Health: [http://localhost:18082/health](http://localhost:18082/health)
- **Version 3 (Royal Purple):**
  - Application: [http://localhost:18083](http://localhost:18083)
  - Health: [http://localhost:18083/health](http://localhost:18083/health)

---

## 🛠 Troubleshooting & Common Errors

| Error Symptom | Root Cause | Solution |
|---|---|---|
| `unauthorized: incorrect username or password` | Expired or incorrect Docker Hub token in Jenkins. | Generate a fresh Personal Access Token with Read/Write permission on Docker Hub and update the `dockerhub-token` credential in Jenkins. |
| `TemplateNotFound: base.html` | Missing templates folder in Docker image. | Ensure `COPY templates/ ./templates/` and `COPY static/ ./static/` are present in `Dockerfile`. |
| `ImagePullBackOff` | Image not found on Docker Hub or network timeout. | Verify image is built locally and set `imagePullPolicy: IfNotPresent` in Kubernetes deployments. |
| `port already allocated` | Port conflict on host machine. | Check active ports with `netstat -ano \| findstr <port>` and terminate conflicting process or select alternate port. |
| `Docker daemon is not running` | Docker Desktop service is stopped. | Start Docker Desktop from the Start menu and wait until the whale icon shows "Engine running". |

---

## ⚖️ Design Decisions & Known Limitations

1. **In-Memory Storage:**
   - *Rationale:* For a college laboratory project, in-memory Python data structures (`list` of `dict`) avoid the operational complexity, network latency, and credential overhead of an external relational database (PostgreSQL/MySQL).
   - *Limitation:* State is transient; if a container restarts or pod is rescheduled, submitted reviews revert to sample seed data. In an enterprise system, this would be replaced with PostgreSQL or MongoDB.
2. **Synchronous WSGI:**
   - *Rationale:* Running `python app.py` outputs clear synchronous logs to stdout, simplifying container debugging for beginners.
   - *Limitation:* Handles single-threaded requests; production deployments should wrap the Flask app with Gunicorn (`gunicorn -w 4 -b 0.0.0.0:5000 app:app`).

---

## 🎓 Viva & Project Review Presentation Guide

When presenting this project to your professor or examiner, explain the lifecycle in 5 key stages:
1. **Source Code & Architecture:** Explain how Flask serves HTML via Jinja2 templates and CSS from static assets, separated by concerns.
2. **Testing:** Highlight that `pytest` validates both positive (valid review) and negative (missing name/comment, bad rating) cases before any build occurs.
3. **Containerization:** Show that Docker images are parameterized using `ARG APP_VERSION`, keeping builds deterministic and lightweight.
4. **CI/CD Pipeline:** Demonstrate Jenkins automated stages—from code checkout to testing, image building, Docker Hub push, and Kubernetes validation.
5. **Orchestration:** Show the running Kubernetes pods with live readiness probes, and open all three version ports (`18081`, `18082`, `18083`) side-by-side in browser tabs to demonstrate continuous version delivery.
