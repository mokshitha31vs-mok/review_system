# College Assignment Screenshot Checklist & Submission Guide

This directory is reserved for capturing and storing demonstration screenshots required for college laboratory evaluations, project vivas, and assignment submissions.

---

## 📸 Required Screenshot Checklist

| No. | Step / Milestone | Component | What to Capture in the Screenshot |
|---|---|---|---|
| **01** | Local Flask Execution | Terminal & Browser | Terminal running `python app.py` and browser showing `http://127.0.0.1:5000` with the review submission form. |
| **02** | Local Endpoint Testing | Browser | Browser or curl displaying `http://127.0.0.1:5000/health` returning `{"status":"healthy","version":"v1"}`. |
| **03** | Automated Pytest Suite | Terminal | PowerShell terminal displaying `pytest -v` with all 9 unit and integration tests passing (`9 passed`). |
| **04** | Git & GitHub History | GitHub UI / Git CLI | GitHub repository showing commits on `main` and branch list (`main`, `v1`, `v2`, `v3`). |
| **05** | Docker Image Builds | Terminal | Output of `docker images mmokshitha/review-system` showing tags `v1`, `v2`, and `v3`. |
| **06** | Local Docker Containers | Browser & Terminal | 3 active containers running on host ports 5001, 5002, 5003 displaying distinct UI versions in browser tabs. |
| **07** | Jenkins Pipeline Configuration | Jenkins UI | Pipeline project configuration in Jenkins showing SCM linking to GitHub and Script Path `Jenkinsfile`. |
| **08** | Jenkins Pipeline Execution | Jenkins UI | Pipeline Stage View showing green stages (`Checkout`, `Check Tools`, `Install Dependencies`, `Run Tests`, `Build V1 Image`, `Build V2 Image`, `Build V3 Image`, `Login and Push to Docker Hub`, `Validate Kubernetes Manifests`) with `SUCCESS`. |
| **09** | Docker Hub Repository | Docker Hub UI | Public repository `mmokshitha/review-system` displaying pushed tags `v1`, `v2`, and `v3` with recent timestamps. |
| **10** | Kubernetes Cluster Status | Terminal | Output of `kubectl get deployments,pods,services` showing running pods and active services for v1, v2, and v3. |
| **11** | V1 Live Access | Browser | Browser tab displaying `http://localhost:18081` (Review System V1 with blue theme and basic submission). |
| **12** | V2 Live Access | Browser | Browser tab displaying `http://localhost:18082` (Review System V2 with emerald theme, stats cards, and star rating filter). |
| **13** | V3 Live Access | Browser | Browser tab displaying `http://localhost:18083` (Review System V3 with purple theme, sorting dropdown, and rating breakdown histogram). |
| **14** | Kubernetes /health Probes | Browser | Browser tabs or curl testing `http://localhost:18081/health`, `http://localhost:18082/health`, and `http://localhost:18083/health` showing respective versions. |

---

## 💡 Best Practices for Viva / Evaluation
- **Full Screen Context**: Include the taskbar, URL bar, or terminal prompt to prove live execution on your machine.
- **Side-by-Side Comparison**: Capture a single screenshot with three browser windows side-by-side displaying V1 (Blue), V2 (Green), and V3 (Purple) to demonstrate version progression.
- **File Naming Format**: Name screenshot files systematically:
  - `01_flask_local_home.png`
  - `02_flask_health_endpoint.png`
  - `03_pytest_automated_tests.png`
  - `04_git_branches_github.png`
  - `05_docker_local_images.png`
  - `06_jenkins_pipeline_success.png`
  - `07_dockerhub_tags_v1_v2_v3.png`
  - `08_k8s_deployments_pods_services.png`
  - `09_k8s_v1_localhost_18081.png`
  - `10_k8s_v2_localhost_18082.png`
  - `11_k8s_v3_localhost_18083.png`
