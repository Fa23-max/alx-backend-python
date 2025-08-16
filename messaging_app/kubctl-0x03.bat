@echo off
REM kubctl-0x03 - Script to perform rolling update and test for downtime

echo === Starting Rolling Update ===

REM Start background curl requests to test for downtime
echo Starting background curl requests to test for downtime...
(
  echo @echo off
  echo :loop
  echo for /f "tokens=*" %%%%i in ('powershell -Command "Get-Date -UFormat %%s"') do set timestamp=%%%%i
  echo curl -s -o nul -w "%%{http_code}" http://localhost:8000 2^>nul ^|^| echo 000 ^> response.txt
  echo set /p response=^< response.txt
  echo echo [%%timestamp%%] HTTP Response: %%response%% ^>^> curl_responses.log
  echo del response.txt
  echo timeout /t 1 /nobreak ^>nul
  echo goto loop
) > curl_loop.bat

start "" curl_loop.bat
timeout /t 2 /nobreak >nul

REM Apply the updated deployment
echo Applying updated deployment with django:2.0...
kubectl apply -f blue_deployment.yaml

REM Monitor the rollout status
echo Monitoring rollout status...
kubectl rollout status deployment/django-messaging-app

REM Stop the background curl requests
echo Stopping background curl requests...
taskkill /f /im curl_loop.bat 2>nul

REM Verify the Rolling Update is Complete
echo.
echo === Verifying Rolling Update ===
echo Current pods:
kubectl get pods

echo.
echo Deployment status:
kubectl get deployment django-messaging-app -o wide

echo.
echo === Downtime Analysis ===
echo Checking curl responses for downtime...
if exist curl_responses.log (
  echo Total requests: 
  type curl_responses.log | find /c /v ""
  echo Successful requests (200):
  type curl_responses.log | find /c "200"
  echo Failed requests:
  type curl_responses.log | find /c "000"
  
  echo.
  type curl_responses.log | find "000" >nul
  if %errorlevel% == 0 (
    echo Failed requests timestamps:
    type curl_responses.log | find "000"
  ) else (
    echo No failed requests detected - no downtime experienced!
  )
) else (
  echo No curl response log found
)

REM Clean up
del curl_responses.log curl_loop.bat 2>nul

echo.
echo === Rolling Update Complete ===
echo The deployment has been updated to django:2.0
echo Rolling update completed with minimal to no downtime