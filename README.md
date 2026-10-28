# Review System — CI/CD V1, V2, V3

Includes a Flask review app, tests, Docker image tags `v1`, `v2`, `v3`, a Jenkins pipeline, and three Kubernetes Deployment/Service manifests.

## Run locally (PowerShell)
```powershell
python -m pip install -r requirements.txt
python -m pytest -v
python app.py
```
Open `http://localhost:5000` and `http://localhost:5000/health`.

## Build images manually
```powershell
docker build --build-arg APP_VERSION=v1 -t mmokshitha/review-system:v1 .
docker build --build-arg APP_VERSION=v2 -t mmokshitha/review-system:v2 .
docker build --build-arg APP_VERSION=v3 -t mmokshitha/review-system:v3 .
```

## Push source to GitHub
Create an empty repository, then run from this folder:
```powershell
git init
git add .
git commit -m "Create Review System with tests and CI/CD files"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/review-system.git
git push -u origin main
```
Replace `YOUR_GITHUB_USERNAME`. If `origin` already exists, inspect `git remote -v` instead of adding it again.

## Jenkins setup
1. Create a Pipeline job and configure it to use `Jenkinsfile` from SCM.
2. Add a Jenkins credential of type **Username with password**:
   - ID: `dockerhub-credentials`
   - Username: `mmokshitha`
   - Password: a Docker Hub access token with permission to push images.
3. Make sure the Jenkins agent is Windows, Docker Desktop is running, and Git is configured.
4. If Python or Docker is installed elsewhere, update the two paths in `Jenkinsfile`.
5. Run the job and inspect Console Output.

## Kubernetes
Start Docker Desktop Kubernetes and confirm `kubectl get nodes` shows `Ready`. After the three images have been pushed:
```powershell
kubectl apply -f k8s/v1-deployment.yaml
kubectl apply -f k8s/v2-deployment.yaml
kubectl apply -f k8s/v3-deployment.yaml
kubectl get deployments
kubectl get pods
kubectl get services
```
Open:
- V1: `http://localhost:30081`
- V2: `http://localhost:30082`
- V3: `http://localhost:30083`

## Important
This starter uses in-memory reviews, so reviews reset when the application restarts. The three images are tagged separately and display their version, but they are built from the same app source. If your instructor expects different features in each version, add the required feature changes and commit them separately before building each version. Never commit Docker tokens or passwords.
