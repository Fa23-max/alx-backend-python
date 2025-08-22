# Messaging App CI/CD Pipeline

This repository contains a Django messaging application with comprehensive CI/CD pipeline setup using Jenkins and GitHub Actions.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- GitHub account
- Docker Hub account

### 1. Start Jenkins
```bash
# Option 1: Using docker-compose (recommended)
docker-compose -f docker-compose.jenkins.yml up -d

# Option 2: Using docker run
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

### 2. Access Jenkins
- Open http://localhost:8080
- Get initial password: `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`
- Follow setup wizard

## 📋 Pipeline Overview

### Jenkins Pipeline Stages
1. **Checkout** - Pull code from GitHub
2. **Setup Python** - Configure Python environment
3. **Install Dependencies** - Install Python packages
4. **Code Quality Check** - Run flake8 linting
5. **Run Tests** - Execute pytest with coverage
6. **Generate Test Report** - Create HTML/XML reports
7. **Build Docker Image** - Create Docker image
8. **Push Docker Image** - Push to Docker Hub

### GitHub Actions Workflows
- **CI Workflow** (`.github/workflows/ci.yml`) - Runs tests on every push/PR
- **Deployment Workflow** (`.github/workflows/dep.yml`) - Builds and pushes Docker images

## 🔧 Configuration

### Jenkins Setup
1. Install required plugins:
   - Git plugin
   - Pipeline
   - ShiningPanda Plugin
   - HTML Publisher Plugin
   - Credentials Plugin
   - Docker Pipeline Plugin

2. Configure credentials:
   - GitHub SSH key: `github-ssh`
   - Docker Hub: `docker-hub-credentials`

3. Create pipeline job:
   - Name: `messaging-app-pipeline`
   - SCM: Git with your repository
   - Script path: `messaging_app/Jenkinsfile`

### GitHub Actions Setup
1. Add repository secrets:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`

2. Update image names in workflow files

## 🧪 Testing

### Running Tests Locally
```bash
# Install test dependencies
pip install -r test-requirements.txt

# Run tests
cd messaging_app
python -m pytest chats/tests/ -v --cov=chats

# Run linting
flake8 . --max-line-length=120 --exclude=*/migrations/*,*/__pycache__/*
```

### Test Configuration
- **pytest.ini**: Main test configuration
- **Coverage**: HTML and XML reports
- **Linting**: flake8 with custom rules
- **Database**: MySQL for integration tests

## 🐳 Docker

### Building Images
```bash
# Build locally
docker build -t messaging-app:latest -f messaging_app/Dockerfile messaging_app/

# Run locally
docker run -p 8000:8000 messaging-app:latest
```

### Docker Compose
```bash
# Development
docker-compose up -d

# Jenkins
docker-compose -f docker-compose.jenkins.yml up -d
```

## 📊 Monitoring

### Jenkins
- Build history and logs
- Test results and coverage reports
- Pipeline stage status
- Build artifacts

### GitHub Actions
- Workflow run status
- Test results
- Coverage reports
- Docker image builds

## 🔒 Security

### Best Practices
- Use Docker Hub access tokens
- Implement proper authentication
- Regular security updates
- Secrets management
- Network isolation

### Credentials
- Store sensitive data in Jenkins credentials
- Use GitHub secrets for Actions
- Rotate access tokens regularly

## 🚨 Troubleshooting

### Common Issues
1. **Docker not found**: Ensure Docker is running and accessible
2. **Permission denied**: Check Docker group membership
3. **Git clone failed**: Verify SSH keys and repository access
4. **Python not found**: Install Python or use Docker agent

### Debug Commands
```bash
# Check Jenkins logs
docker logs jenkins

# Check Jenkins status
docker ps

# Access Jenkins shell
docker exec -it jenkins bash

# Check pipeline status
curl http://localhost:8080/api/json
```

## 📚 Additional Resources

### Documentation
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [pytest Documentation](https://docs.pytest.org/)

### Plugins
- [Jenkins Plugins](https://plugins.jenkins.io/)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review Jenkins and GitHub Actions logs
3. Create an issue in the repository
4. Contact the development team

---

**Note**: Remember to update the Docker image names and credentials in the configuration files before using them in production.
