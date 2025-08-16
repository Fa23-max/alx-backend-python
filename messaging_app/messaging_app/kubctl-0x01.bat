@echo off
REM kubctl-0x01 - Script to scale Django app deployment and perform load testing

echo === Scaling Django app deployment to 3 replicas ===
kubectl scale deployment django-messaging-app --replicas=3

echo.
echo === Verifying that multiple pods are running ===
kubectl get pods

echo.
echo === Performing load testing with wrk ===
REM Check if wrk is installed
where wrk >nul 2>&1
if %errorlevel% == 0 (
    REM Get the service IP
    for /f "tokens=*" %%i in ('kubectl get service django-messaging-app-service -o jsonpath^="{.spec.clusterIP}"') do set SERVICE_IP=%%i
    echo Service IP: %SERVICE_IP%
    
    REM Perform load test
    echo Starting load test...
    wrk -t12 -c400 -d30s http://%SERVICE_IP%:8000/
) else (
    echo wrk could not be found, please install it manually:
    echo   Download from https://github.com/wg/wrk
)

echo.
echo === Monitoring Resource Usage ===
kubectl top nodes
kubectl top pods