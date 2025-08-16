@echo off
REM kubctl-0x02 - Script to deploy blue-green deployment and check for errors

echo === Deploying Blue-Green Deployment Strategy ===

echo Deploying blue version...
kubectl apply -f blue_deployment.yaml

echo Deploying green version...
kubectl apply -f green_deployment.yaml

echo Deploying services...
kubectl apply -f kubeservice.yaml

echo.
echo === Checking deployment status ===
kubectl get deployments

echo.
echo === Checking pod status ===
kubectl get pods

echo.
echo === Checking service status ===
kubectl get services

echo.
echo === Checking for errors in blue deployment ===
for /f "tokens=*" %%i in ('kubectl get pods -l app^=django-messaging-app -o jsonpath^="{.items[0].metadata.name}"') do set BLUE_POD=%%i
if defined BLUE_POD (
  echo Logs for blue deployment pod (%BLUE_POD%):
  kubectl logs %BLUE_POD%
) else (
  echo No blue deployment pods found
)

echo.
echo === Checking for errors in green deployment ===
for /f "tokens=*" %%i in ('kubectl get pods -l app^=django-messaging-app-green -o jsonpath^="{.items[0].metadata.name}"') do set GREEN_POD=%%i
if defined GREEN_POD (
  echo Logs for green deployment pod (%GREEN_POD%):
  kubectl logs %GREEN_POD%
) else (
  echo No green deployment pods found
)

echo.
echo === Blue-Green Deployment Complete ===
echo To switch traffic from blue to green, update the selector in kubeservice.yaml
echo Change 'app: django-messaging-app-blue' to 'app: django-messaging-app-green'