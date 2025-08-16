# Rolling Update Script

This directory contains the script to perform a rolling update of the Django messaging app deployment.

## Files

- `blue_deployment.yaml` - The updated deployment file with django:2.0 image
- `kubctl-0x03` - Shell script to perform rolling update and test for downtime
- `kubctl-0x03.bat` - Windows batch script to perform rolling update and test for downtime

## Rolling Update Process

The rolling update script performs the following operations:

1. **Starts background curl requests** - Continuously sends HTTP requests to the application to monitor for downtime
2. **Applies the updated deployment** - Updates the deployment to use django:2.0 image
3. **Monitors rollout status** - Tracks the progress of the rolling update
4. **Verifies update completion** - Checks that all pods are running the new version
5. **Analyzes downtime** - Reviews the curl responses to determine if any downtime occurred

## Usage

### Unix-like systems (Linux/macOS)
```bash
chmod +x kubctl-0x03
./kubctl-0x03
```

### Windows
```cmd
kubctl-0x03.bat
```

## What the Script Does

1. **Starts continuous monitoring** - Uses curl to send requests every 100ms to detect downtime
2. **Triggers rolling update** - Applies the updated deployment configuration
3. **Waits for completion** - Uses `kubectl rollout status` to wait for update completion
4. **Analyzes results** - Checks the HTTP response codes to determine if any requests failed
5. **Reports findings** - Shows statistics on successful and failed requests

## Expected Output

The script will show:
- Real-time rollout status updates
- Final pod status
- Downtime analysis with statistics
- Confirmation of successful update

## Notes

- The script assumes the application is accessible at http://localhost:8000
- The curl requests run in the background to detect any momentary downtime
- The script cleans up temporary files after execution
- Rolling updates in Kubernetes ensure zero-downtime deployments by gradually replacing old pods with new ones