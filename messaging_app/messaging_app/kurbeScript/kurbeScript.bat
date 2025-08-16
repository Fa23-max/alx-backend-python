@echo off
REM kurbeScript - Kubernetes cluster management script
REM This script starts a Kubernetes cluster, verifies it's running, and retrieves available pods
REM It also ensures minikube is installed

echo [INFO] Starting kurbeScript - Kubernetes cluster management script
echo.

REM Check if kubectl is installed
echo [INFO] Checking if kubectl is installed...
where kubectl >nul 2>&1
if %errorlevel% == 0 (
    echo [INFO] kubectl is already installed
    kubectl version --client
) else (
    echo [WARN] kubectl is not installed. Installing kubectl...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri https://dl.k8s.io/release/v1.28.0/bin/windows/amd64/kubectl.exe -OutFile kubectl.exe}"
    if exist kubectl.exe (
        echo [INFO] kubectl downloaded successfully
        move kubectl.exe C:\Windows\System32\
        echo [INFO] kubectl installed to C:\Windows\System32\
    ) else (
        echo [ERROR] Failed to download kubectl
        exit /b 1
    )
)

echo.
REM Check if minikube is installed
echo [INFO] Checking if minikube is installed...
where minikube >nul 2>&1
if %errorlevel% == 0 (
    echo [INFO] minikube is already installed
    minikube version
) else (
    echo [WARN] minikube is not installed. Installing minikube...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe -OutFile minikube.exe}"
    if exist minikube.exe (
        echo [INFO] minikube downloaded successfully
        move minikube.exe C:\Windows\System32\minikube.exe
        echo [INFO] minikube installed to C:\Windows\System32\
    ) else (
        echo [ERROR] Failed to download minikube
        exit /b 1
    )
)

echo.
REM Start Kubernetes cluster
echo [INFO] Starting Kubernetes cluster with minikube...
minikube start --driver=docker
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start minikube cluster
    exit /b 1
)

echo.
REM Verify cluster is running
echo [INFO] Verifying cluster is running...
kubectl cluster-info
if %errorlevel% neq 0 (
    echo [ERROR] Failed to verify cluster info
    exit /b 1
)

echo.
REM Retrieve available pods
echo [INFO] Retrieving available pods...
kubectl get pods --all-namespaces
if %errorlevel% neq 0 (
    echo [ERROR] Failed to retrieve pods
    exit /b 1
)

echo.
echo [INFO] kurbeScript completed successfully!
echo [INFO] Kubernetes cluster is running and pods have been retrieved.