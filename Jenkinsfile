pipeline {
    agent any
    environment {
        IMAGE_NAME = 'mmokshitha/review-system'
        PYTHON_EXE = 'C:\\Users\\MOKSHITHA\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        DOCKER_EXE = 'C:\\Users\\MOKSHITHA\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Check Tools') {
            steps {
                powershell '''
                    if (!(Test-Path $env:PYTHON_EXE)) { throw "Python executable not found: $env:PYTHON_EXE" }
                    if (!(Test-Path $env:DOCKER_EXE)) { throw "Docker executable not found: $env:DOCKER_EXE" }
                    & $env:PYTHON_EXE --version
                    & $env:DOCKER_EXE --version
                    & $env:DOCKER_EXE info
                    if ($LASTEXITCODE -ne 0) { throw "Docker daemon is not available." }
                '''
            }
        }
        stage('Install Dependencies') {
            steps {
                powershell '''
                    & $env:PYTHON_EXE -m pip install -r requirements.txt
                    if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }
                '''
            }
        }
        stage('Run Tests') {
            steps {
                powershell '''
                    & $env:PYTHON_EXE -m pytest -v
                    if ($LASTEXITCODE -ne 0) { throw "Automated tests failed." }
                '''
            }
        }
        stage('Build Docker Images v1 v2 v3') {
            steps {
                powershell '''
                    foreach ($version in @("v1", "v2", "v3")) {
                        & $env:DOCKER_EXE build --build-arg "APP_VERSION=$version" -t "$env:IMAGE_NAME`:$version" .
                        if ($LASTEXITCODE -ne 0) { throw "Docker build failed for $version." }
                    }
                '''
            }
        }
        stage('Login and Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
                    powershell '''
                        $ErrorActionPreference = "Stop"
                        $username = $env:DH_USER.Trim()
                        $token = $env:DH_TOKEN.Trim()
                        $token | & $env:DOCKER_EXE login --username $username --password-stdin
                        if ($LASTEXITCODE -ne 0) { throw "Docker Hub login failed. Check Jenkins credential dockerhub-credentials." }
                        foreach ($version in @("v1", "v2", "v3")) {
                            & $env:DOCKER_EXE push "$env:IMAGE_NAME`:$version"
                            if ($LASTEXITCODE -ne 0) { throw "Docker push failed for $version." }
                        }
                    '''
                }
            }
        }
    }
    post {
        success { echo 'SUCCESS: tests passed and Docker images v1, v2, and v3 were pushed.' }
        failure { echo 'FAILED: inspect the first red stage in Console Output.' }
    }
}
