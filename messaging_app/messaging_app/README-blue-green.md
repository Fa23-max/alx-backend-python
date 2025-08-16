# Blue-Green Deployment Strategy

This directory contains the configuration files for implementing a blue-green deployment strategy for the Django messaging app.

## Files

- `blue_deployment.yaml` - The blue (current) version of the Django app deployment
- `green_deployment.yaml` - The green (new) version of the Django app deployment
- `kubeservice.yaml` - Kubernetes services to manage traffic routing
- `kubctl-0x02` - Shell script to deploy both versions and check for errors
- `kubctl-0x02.bat` - Windows batch script to deploy both versions and check for errors

## Blue-Green Deployment Strategy

Blue-green deployment is a release strategy that reduces downtime and risk by running two identical production environments called Blue and Green.

- **Blue** - The current production environment
- **Green** - The new version of the application

The strategy allows you to:
1. Deploy the new version to the green environment
2. Test the green environment
3. Switch traffic from blue to green with zero downtime
4. Roll back quickly if issues are found

## How It Works

1. Both blue and green deployments are deployed simultaneously
2. The main service initially points to the blue deployment
3. After testing the green deployment, you can switch traffic by updating the service selector
4. If issues are found, you can quickly switch back to the blue deployment

## Switching Traffic

To switch traffic from blue to green:

1. Edit `kubeservice.yaml`
2. Change the selector from `app: django-messaging-app-blue` to `app: django-messaging-app-green`
3. Apply the changes:
   ```bash
   kubectl apply -f kubeservice.yaml
   ```

## Usage

### Unix-like systems (Linux/macOS)
```bash
chmod +x kubctl-0x02
./kubctl-0x02
```

### Windows
```cmd
kubctl-0x02.bat
```

## What the Script Does

1. **Deploys both versions** - Applies the blue and green deployment configurations
2. **Deploys services** - Creates the necessary Kubernetes services
3. **Checks deployment status** - Verifies that deployments are running
4. **Checks pod status** - Verifies that pods are running
5. **Checks service status** - Verifies that services are available
6. **Checks for errors** - Retrieves logs from both deployments to check for errors

## Notes

- The blue deployment uses the original `django-messaging-app` labels
- The green deployment uses `django-messaging-app-green` labels
- Both deployments use the same Docker image but can be modified to use different versions
- The main service acts as a load balancer that can switch between blue and green deployments