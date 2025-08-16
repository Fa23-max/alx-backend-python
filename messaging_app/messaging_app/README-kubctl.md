# kubctl-0x01

A script to scale the Django messaging app deployment and perform load testing.

## Overview

This script performs the following operations:
1. Scales the Django app deployment to 3 replicas using `kubectl scale`
2. Verifies that multiple pods are running using `kubectl get pods`
3. Performs load testing on the app using wrk
4. Monitors resource usage using `kubectl top`

## Scripts

### kubctl-0x01
A shell script for Unix-like systems (Linux/macOS).

### kubctl-0x01.bat
A Windows batch script.

## Prerequisites

- A running Kubernetes cluster
- kubectl installed and configured
- The Django messaging app deployed
- wrk installed for load testing (optional)

## Usage

### Unix-like systems (Linux/macOS)
```bash
chmod +x kubctl-0x01
./kubctl-0x01
```

### Windows
```cmd
kubctl-0x01.bat
```

## What the Script Does

1. **Scales the deployment** - Increases the number of replicas to 3
2. **Verifies pods** - Shows the status of all pods
3. **Load testing** - Uses wrk to perform load testing on the app
4. **Resource monitoring** - Shows resource usage of nodes and pods

## Notes

- The script assumes the deployment is named "django-messaging-app"
- The script assumes the service is named "django-messaging-app-service"
- wrk needs to be installed separately for load testing functionality
- The load test parameters can be adjusted in the script as needed