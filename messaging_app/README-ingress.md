# Ingress Configuration

This directory contains the Ingress resource configuration for the Django messaging app.

## Files

- `ingress.yaml` - The Ingress resource definition
- `commands.txt` - The command used to apply the Ingress configuration

## Ingress Configuration

The Ingress resource is configured to route traffic to the Django messaging app service with the following paths:

- `/` - Root path routes to the Django app service
- `/api/` - API endpoints route to the Django app service
- `/admin/` - Django admin interface routes to the Django app service
- `/static/` - Static files route to the Django app service

The Ingress is configured with the host `messaging-app.local`.

## Applying the Configuration

To apply the Ingress configuration, use the command specified in `commands.txt`:

```bash
kubectl apply -f ingress.yaml
```

## Prerequisites

- A running Kubernetes cluster
- The Django messaging app deployed with the service named `django-messaging-app-service`
- An Ingress controller installed in the cluster (e.g., NGINX Ingress Controller)

## Testing

To test the Ingress, you can add an entry to your hosts file:

```
127.0.0.1 messaging-app.local
```

Then access the application at:
- http://messaging-app.local/
- http://messaging-app.local/api/
- http://messaging-app.local/admin/