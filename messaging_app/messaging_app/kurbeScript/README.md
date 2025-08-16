# kurbeScript

A collection of scripts to manage a Kubernetes cluster using minikube.

## Overview

This project contains scripts that:
1. Ensures minikube and kubectl are installed
2. Starts a Kubernetes cluster on your machine
3. Verifies that the cluster is running using `kubectl cluster-info`
4. Retrieves the available pods

## Scripts

### kurbeScript.bat
A Windows batch script for managing Kubernetes clusters with minikube.

### kurbeScript.sh
A shell script for managing Kubernetes clusters with minikube on Unix-like systems (Linux/macOS).

## Usage

### Windows
```cmd
kurbeScript.bat
```

### Linux/macOS
```bash
chmod +x kurbeScript.sh
./kurbeScript.sh
```

## What the Script Does

1. **Checks for kubectl installation** - If not found, downloads and installs it
2. **Checks for minikube installation** - If not found, downloads and installs it
3. **Starts a Kubernetes cluster** using `minikube start`
4. **Verifies the cluster is running** using `kubectl cluster-info`
5. **Retrieves available pods** using `kubectl get pods --all-namespaces`

## Prerequisites

- Windows, Linux, or macOS operating system
- Internet connection (for downloading minikube and kubectl if not installed)
- Docker (required for minikube)

## Notes

- The script will attempt to install minikube and kubectl if they are not found
- On Windows, the script installs the binaries to `C:\Windows\System32\`
- On Linux/macOS, the script installs the binaries to `/usr/local/bin/`
- The script uses Docker as the default driver for minikube