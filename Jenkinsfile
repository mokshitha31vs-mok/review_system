pipeline {
    agent any

    environment {
        IMAGE_NAME = 'mmokshitha/review-system'
        PYTHON_EXE = 'C:\\Users\\MOKSHITHA\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        DOCKER_EXE = 'C:\\Users\\MOKSHITHA\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Tools') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    if (!(Test-Path $env:PYTHON_EXE)) {
                        throw "Python executable not found at: $env:PYTHON_EXE"
                    }
                    if (!(Test-Path $env:DOCKER_EXE)) {
                        throw "Docker executable not found at: $env:DOCKER_EXE"
                    }

                    Write-Host "=== Tool Versions ==="
                    & $env:PYTHON_EXE --version
                    & $env:DOCKER_EXE --version
                    kubectl version --client

                    Write-Host "Checking Docker daemon connectivity..."
                    & $env:DOCKER_EXE info --format "{{.ServerVersion}}"
                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker daemon is not running or accessible."
                    }
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"
                    Write-Host "Installing project requirements..."
                    & $env:PYTHON_EXE -m pip install --quiet -r requirements.txt
                    if ($LASTEXITCODE -ne 0) {
                        throw "Failed to install Python dependencies from requirements.txt."
                    }
                '''
            }
        }

        stage('Run Tests') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"
                    Write-Host "Executing automated pytest test suite..."
                    & $env:PYTHON_EXE -m pytest -v
                    if ($LASTEXITCODE -ne 0) {
                        throw "Pytest automated tests failed."
                    }
                '''
            }
        }

        stage('Build V1 Image') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"
                    Write-Host "Building Docker image: $env:IMAGE_NAME:v1"
                    & $env:DOCKER_EXE build --build-arg "APP_VERSION=v1" -t "$env:IMAGE_NAME`:v1" .
                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker build failed for version v1."
                    }
                '''
            }
        }

        stage('Build V2 Image') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"
                    Write-Host "Building Docker image: $env:IMAGE_NAME:v2"
                    & $env:DOCKER_EXE build --build-arg "APP_VERSION=v2" -t "$env:IMAGE_NAME`:v2" .
                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker build failed for version v2."
                    }
                '''
            }
        }

        stage('Build V3 Image') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"
                    Write-Host "Building Docker image: $env:IMAGE_NAME:v3"
                    & $env:DOCKER_EXE build --build-arg "APP_VERSION=v3" -t "$env:IMAGE_NAME`:v3" .
                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker build failed for version v3."
                    }
                '''
            }
        }

        stage('Login and Push to Docker Hub') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'dockerhub-token',
                        variable: 'DH_TOKEN'
                    )
                ]) {
                    powershell '''
                        $ErrorActionPreference = "Stop"

                        if ([string]::IsNullOrWhiteSpace($env:DH_TOKEN)) {
                            throw "Docker Hub token is missing or empty in Jenkins credentials (dockerhub-token)."
                        }

                        Write-Host "Authenticating with Docker Hub using token credential..."
                        $cleanToken = $env:DH_TOKEN.Trim()
                        $cleanToken | & $env:DOCKER_EXE login --username "mmokshitha" --password-stdin

                        if ($LASTEXITCODE -ne 0) {
                            throw "Docker Hub login failed. Verify that dockerhub-token credential contains a valid Read/Write Docker Hub Personal Access Token for username mmokshitha."
                        }

                        foreach ($ver in @("v1", "v2", "v3")) {
                            Write-Host "Pushing $env:IMAGE_NAME`:$ver to Docker Hub..."
                            & $env:DOCKER_EXE push "$env:IMAGE_NAME`:$ver"
                            if ($LASTEXITCODE -ne 0) {
                                throw "Docker push failed for tag: $ver"
                            }
                        }

                        Write-Host "Successfully pushed all three image tags to Docker Hub."
                        & $env:DOCKER_EXE logout
                    '''
                }
            }
        }

        stage('Validate Kubernetes Manifests') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"
                    Write-Host "Validating Kubernetes deployment and service YAML manifests..."
                    kubectl apply --dry-run=client -f k8s/
                    if ($LASTEXITCODE -ne 0) {
                        throw "Kubernetes manifest validation failed. Inspect YAML syntax and schemas in k8s/ directory."
                    }
                    Write-Host "All Kubernetes manifests in k8s/ are valid and ready for deployment."
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS: CI/CD pipeline completed all stages successfully! Tests passed, V1/V2/V3 images built and pushed, and Kubernetes manifests validated."
        }
        failure {
            echo "FAILED: Review Console Output for the first failing stage."
        }
    }
}