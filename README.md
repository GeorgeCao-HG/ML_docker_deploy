# ML Docker Demo - Machine Learning Model Docker Deployment Guide

This project demonstrates how to package machine learning models into Docker containers and serve them via REST API. It's a complete end-to-end example covering model training, dependency management, Docker building, and deployment debugging best practices.

## 📁 Project Structure

```
ml-docker-demo/
├── train_model.py          # Model training script
├── capture_requirements.py # Smart dependency capture tool
├── app.py                  # Flask API service
├── Dockerfile              # Docker configuration
├── requirements.txt        # Auto-generated dependency list
├── model.joblib            # Saved model file
└── README.MD               # Project documentation
```

## 🚀 Quick Start

### Step 1: Environment Setup

Create and activate Conda environment:
```bash
# Create virtual environment
conda create -n ml-deploy python=3.9
conda activate ml-deploy

# Or use Python venv
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

Install required dependencies:
```bash
pip install flask==2.3.2 scikit-learn==1.3.0 numpy==1.23.5 joblib==1.3.2
```

### Step 2: Train Model and Generate Dependencies

```bash
# 1. Train the model
python train_model.py

# 2. Auto-capture exact dependency versions
python capture_requirements.py
```

This generates `requirements.txt` with pinned versions:
```
scikit-learn==1.6.1
numpy==1.23.5
flask==2.3.2
joblib==1.3.2
```

### Step 3: Docker Build and Run

```bash
# Build Docker image
docker build -t ml-model-api .

# Run container
docker run -p 5000:5000 ml-model-api

# One-command build and run
docker build -t ml-model-api . && docker run -p 5000:5000 ml-model-api
```

## 🧪 API Testing

### Using curl (Recommended)

**Windows PowerShell/CMD:**
```cmd
curl -v -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"features\": [5.1, 3.5, 1.4, 0.2]}"
```

**Linux/macOS/Git Bash:**
```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

**Expected Output:**
```json
{"prediction": 0}
```

### Using Python

Create test script `test_api.py`:
```python
import requests

response = requests.post(
    "http://localhost:5000/predict",
    json={"features": [5.1, 3.5, 1.4, 0.2]}
)
print(response.json())
```

Run test:
```bash
python test_api.py
```

## 🔧 Advanced Docker Operations

### Container Management Commands

```bash
# View running containers
docker ps

# View container logs
docker logs <container_id>

# Stop container
docker stop <container_id>

# Stop all related containers
docker stop $(docker ps -q --filter ancestor=ml-model-api)

# Verify dependencies inside container
docker run -it ml-model-api pip list

# Check container file structure
docker run -it ml-model-api ls -l /app
```

### Container Debugging Techniques

#### Method 1: Enter Running Container
```bash
# Get container ID
docker ps

# Enter container shell
docker exec -it <container_id> /bin/sh

# Install curl inside container for internal testing
apk add curl  # Alpine image
# OR
apt-get update && apt-get install -y curl  # Debian image

# Test API from inside container
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

#### Method 2: Start Interactive Container
```bash
# Start container in interactive mode
docker run -it --entrypoint /bin/sh ml-model-api

# Debug inside container
ls -la /app
cat requirements.txt
python app.py
```

## 🛠️ Dependency Management Best Practices

### Benefits of Auto Dependency Capture

Using `capture_requirements.py` instead of `pip freeze`:
- ✅ **Exact Version Matching**: Ensures production environment matches training environment exactly
- ✅ **Avoid Version Conflicts**: Only includes dependencies actually needed by the model
- ✅ **Reproducible Builds**: Eliminates "works on my machine" problems

### Manual requirements.txt Generation (Backup Method)

**Windows:**
```cmd
pip freeze | findstr "flask scikit-learn numpy joblib" > requirements.txt
```

**Linux/macOS:**
```bash
pip freeze | grep -E "flask|scikit-learn|numpy|joblib" > requirements.txt
```

Verify generated file:
```cmd
type requirements.txt  # Windows
cat requirements.txt   # Linux/macOS
```

## 🐛 Troubleshooting Guide

### Common Issues and Solutions

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| `curl` command hangs | Container not started or port mapping error | `docker ps` to check container status, verify port mapping |
| Port conflict error | Port 5000 already in use | Change host port: `-p 5001:5000` |
| Container startup failure | Dependency installation error or missing files | Check `docker logs <container_id>` |
| API returns 500 error | Model file missing or corrupted | Retrain model, check `model.joblib` |

### Debugging Workflow

1. **Check Container Status**
   ```bash
   docker ps -a
   ```

2. **View Container Logs**
   ```bash
   docker logs <container_id>
   ```

3. **Verify Container Internals**
   ```bash
   docker exec -it <container_id> /bin/sh
   ls -la /app
   python -c "import joblib; print('Model loaded:', joblib.load('model.joblib'))"
   ```

4. **Test API Response**
   - First test inside container
   - Then test from host
   - Compare results to locate issue

## 📚 Technical Notes

### Docker Layer Build Optimization

Dockerfile follows best practices:
```dockerfile
FROM python:3.9-slim      # Use lightweight base image
WORKDIR /app              # Set working directory
COPY requirements.txt .   # Copy dependency file first
RUN pip install --no-cache-dir -r requirements.txt  # Install deps (cached layer)
COPY . .                  # Copy application code
EXPOSE 5000              # Declare port
CMD ["python", "app.py"]  # Startup command
```

### Flask Application Configuration

Key configuration notes:
- `host="0.0.0.0"`: Allow external access (required for Docker containers)
- `port=5000`: Must match Dockerfile's EXPOSE directive
- Production environments should use WSGI servers like Gunicorn

## 🔄 Development Workflow

```bash
# 1. Development and training
python train_model.py

# 2. Generate exact dependencies
python capture_requirements.py

# 3. Local testing
python app.py

# 4. Docker deployment
docker build -t ml-model-api .
docker run -p 5000:5000 ml-model-api

# 5. Validation testing
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

## 📈 Extension Recommendations

- 🔐 **Security**: Add API authentication and input validation
- 📊 **Monitoring**: Integrate logging and performance monitoring
- 🚀 **Scalability**: Use Kubernetes for container orchestration
- 🧪 **Testing**: Add unit tests and integration tests
- 📦 **CI/CD**: Configure automated build and deployment pipelines

## 🎯 Key Learning Points

### Docker Container Debugging Strategy

This is primarily a diagnostic tool. The debugging workflow follows this logic:
- If external test fails but internal test succeeds → Problem is with port mapping or firewall
- If internal test also fails → Problem is with application code itself (crashed or wrong port)
- Always check container logs first: `docker logs <container_id>`

### Production Deployment Considerations

1. **Environment Consistency**: Use `capture_requirements.py` to ensure exact version matching
2. **Container Health Checks**: Implement health endpoints for monitoring
3. **Resource Limits**: Set memory and CPU limits in production
4. **Security**: Never expose debug endpoints in production

---

*This project serves as a comprehensive learning example for dockerizing machine learning models, covering the complete pipeline from model training to production deployment.*
