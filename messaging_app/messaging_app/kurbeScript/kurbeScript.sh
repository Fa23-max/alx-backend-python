#!/bin/bash

# kurbeScript - Kubernetes cluster management script
# This script starts a Kubernetes cluster, verifies it's running, and retrieves available pods
# It also ensures minikube is installed

echo "[INFO] Starting kurbeScript - Kubernetes cluster management script"
echo

# Check if kubectl is installed
echo "[INFO] Checking if kubectl is installed..."
if command -v kubectl &> /dev/null; then
    echo "[INFO] kubectl is already installed"
    kubectl version --client
else
    echo "[WARN] kubectl is not installed. Installing kubectl..."
    # For Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    # For macOS
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
        sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    else
        echo "[ERROR] Unsupported OS type: $OSTYPE"
        exit 1
    fi
    
    if [ -f "kubectl" ]; then
        echo "[INFO] kubectl installed successfully"
        rm kubectl
    else
        echo "[ERROR] Failed to install kubectl"
        exit 1
    fi
fi

echo
# Check if minikube is installed
echo "[INFO] Checking if minikube is installed..."
if command -v minikube &> /dev/null; then
    echo "[INFO] minikube is already installed"
    minikube version
else
    echo "[WARN] minikube is not installed. Installing minikube..."
    # For Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
        sudo install minikube-linux-amd64 /usr/local/bin/minikube
    # For macOS
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
        sudo install minikube-darwin-amd64 /usr/local/bin/minikube
    else
        echo "[ERROR] Unsupported OS type: $OSTYPE"
        exit 1
    fi
    
    if [ -f "minikube-linux-amd64" ] || [ -f "minikube-darwin-amd64" ]; then
        echo "[INFO] minikube installed successfully"
        rm minikube-linux-amd64 minikube-darwin-amd64 2>/dev/null
    else
        echo "[ERROR] Failed to install minikube"
        exit 1
    fi
fi

echo
# Start Kubernetes cluster
echo "[INFO] Starting Kubernetes cluster with minikube..."
minikube start
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to start minikube cluster"
    exit 1
fi

echo
# Verify cluster is running
echo "[INFO] Verifying cluster is running..."
kubectl cluster-info
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to verify cluster info"
    exit 1
fi

echo
# Retrieve available pods
echo "[INFO] Retrieving available pods..."
kubectl get pods --all-namespaces
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to retrieve pods"
    exit 1
fi

echo
echo "[INFO] kurbeScript completed successfully!"
echo "[INFO] Kubernetes cluster is running and pods have been retrieved."