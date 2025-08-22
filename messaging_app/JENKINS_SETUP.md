# Jenkins CI/CD Pipeline Setup Guide

## Prerequisites

1. Docker installed and running
2. GitHub repository with your messaging app code
3. Docker Hub account (for pushing images)

## 1. Running Jenkins in Docker

```bash
# Run Jenkins container
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

# Check if Jenkins is running
docker ps

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

## 2. Jenkins Initial Setup

1. Open http://localhost:8080 in your browser
2. Enter the initial admin password from the container
3. Install suggested plugins
4. Create admin user
5. Configure Jenkins URL (http://localhost:8080)

## 3. Install Required Jenkins Plugins

Go to **Manage Jenkins** > **Manage Plugins** > **Available** and install:

- **Git plugin** - For source code management
- **Pipeline** - For declarative pipeline support
- **ShiningPanda Plugin** - For Python support
- **HTML Publisher Plugin** - For test reports
- **Credentials Plugin** - For storing secrets
- **Docker Pipeline Plugin** - For Docker operations

## 4. Configure Jenkins Credentials

### GitHub Credentials
1. Go to **Manage Jenkins** > **Manage Credentials**
2. Click **System** > **Global credentials** > **Add Credentials**
3. Choose **SSH Username with private key**
4. ID: `github-ssh`
5. Username: Your GitHub username
6. Private Key: Your GitHub SSH private key

### Docker Hub Credentials
1. Go to **Manage Jenkins** > **Manage Credentials**
2. Click **System** > **Global credentials** > **Add Credentials**
3. Choose **Username with password**
4. ID: `docker-hub-credentials`
5. Username: Your Docker Hub username
6. Password: Your Docker Hub access token

## 5. Create Jenkins Pipeline Job

1. Click **New Item**
2. Enter job name: `messaging-app-pipeline`
3. Choose **Pipeline**
4. Click **OK**

### Pipeline Configuration
1. **General**: Check **GitHub project** and enter your repository URL
2. **Build Triggers**: Check **Poll SCM** and set schedule (e.g., `H/15 * * * *`)
3. **Pipeline**: Choose **Pipeline script from SCM**
4. **SCM**: Choose **Git**
5. **Repository URL**: Your GitHub repository URL
6. **Credentials**: Select your GitHub credentials
7. **Branch Specifier**: `*/main`
8. **Script Path**: `messaging_app/Jenkinsfile`

## 6. GitHub Actions Setup

### Repository Secrets
Go to your GitHub repository > **Settings** > **Secrets and variables** > **Actions** and add:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token

### Workflow Files
The following workflow files are already created:
- `.github/workflows/ci.yml` - Runs tests on every push/PR
- `.github/workflows/dep.yml` - Builds and pushes Docker images

## 7. Running the Pipeline

### Manual Trigger
1. Go to your Jenkins job
2. Click **Build Now**
3. Monitor the build progress in the console output

### Automatic Trigger
The pipeline will automatically run when:
- Code is pushed to the main branch
- Pull requests are created/updated
- Scheduled polling triggers

## 8. Pipeline Stages

1. **Checkout**: Pulls code from GitHub
2. **Setup Python**: Configures Python environment
3. **Install Dependencies**: Installs Python packages
4. **Code Quality Check**: Runs flake8 linting
5. **Run Tests**: Executes pytest with coverage
6. **Generate Test Report**: Creates HTML and XML reports
7. **Build Docker Image**: Creates Docker image
8. **Push Docker Image**: Pushes to Docker Hub

## 9. Test Reports and Coverage

- **Test Results**: Available in Jenkins build page
- **Coverage Report**: HTML report accessible via Jenkins
- **Artifacts**: Test results and coverage data stored as build artifacts

## 10. Troubleshooting

### Common Issues
1. **Docker not found**: Ensure Docker is installed and accessible
2. **Permission denied**: Check Docker group membership
3. **Git clone failed**: Verify SSH keys and repository access
4. **Python not found**: Install Python on Jenkins host or use Docker agent

### Logs
- Jenkins build logs: Available in job console output
- Docker logs: `docker logs jenkins`
- System logs: Check Jenkins system log

## 11. Security Considerations

1. Use Docker Hub access tokens instead of passwords
2. Restrict Jenkins network access
3. Regularly update Jenkins and plugins
4. Use secrets management for sensitive data
5. Implement proper user authentication and authorization

## 12. Monitoring and Maintenance

1. Monitor Jenkins resource usage
2. Clean up old builds and artifacts
3. Update Jenkins and plugins regularly
4. Monitor pipeline success rates
5. Set up notifications for build failures
