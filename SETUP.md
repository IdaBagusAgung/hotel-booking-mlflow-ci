# MLflow CI/CD Workflow - ADVANCE Level Setup Guide

## 📋 Overview
Workflow CI/CD lengkap untuk Kriteria 3 - ADVANCE Level (4/4 pts) dengan:
- ✅ MLflow Project dengan python_env.yaml
- ✅ Docker Build menggunakan `mlflow build-docker`
- ✅ Docker Hub Push
- ✅ Google Drive Upload untuk artifacts
- ✅ 15 Steps seperti gambar referensi

---

## 🔧 Prerequisites

### 1. GitHub Repository
```bash
# Initialize git jika belum
cd Workflow-CI
git init
git remote add origin <your-github-repo-url>
```

### 2. DagsHub Account
- URL: https://dagshub.com/gus_agung/hotel-booking-mlflow
- Token: `26046db2b4540bf02257eb5a4b03d1f7acfdd9d7`

### 3. Docker Hub Account
- Buat akun di https://hub.docker.com
- Catat username dan password

### 4. Google Drive API Setup
1. Buka https://console.cloud.google.com
2. Buat project baru atau pilih existing
3. Enable Google Drive API
4. Buat OAuth 2.0 credentials
5. Download credentials JSON
6. Authorize dan dapatkan access token

---

## 🔑 GitHub Secrets Configuration

Tambahkan secrets berikut di GitHub repo settings:

```
Settings → Secrets and variables → Actions → New repository secret
```

### Required Secrets:

1. **DAGSHUB_TOKEN**
   ```
   Value: 26046db2b4540bf02257eb5a4b03d1f7acfdd9d7
   ```

2. **MLFLOW_TRACKING_USERNAME**
   ```
   Value: gus_agung
   ```

3. **MLFLOW_TRACKING_PASSWORD**
   ```
   Value: 26046db2b4540bf02257eb5a4b03d1f7acfdd9d7
   ```

4. **DOCKER_USERNAME**
   ```
   Value: <your-docker-hub-username>
   ```

5. **DOCKER_PASSWORD**
   ```
   Value: <your-docker-hub-password>
   ```

6. **GDRIVE_CREDENTIALS** (Optional)
   ```json
   {
     "token": "your-access-token",
     "refresh_token": "your-refresh-token",
     "token_uri": "https://oauth2.googleapis.com/token",
     "client_id": "your-client-id",
     "client_secret": "your-client-secret",
     "scopes": ["https://www.googleapis.com/auth/drive.file"]
   }
   ```

---

## 📁 Project Structure

```
Workflow-CI/
├── .github/
│   └── workflows/
│       └── mlflow_ci.yml          # Main CI/CD workflow
├── MLProject/
│   ├── MLproject                  # MLflow project config
│   ├── python_env.yaml            # Python environment
│   ├── modelling_tuning.py        # Training script (ADVANCE)
│   └── hotel_bookings_preprocessed.csv  # Dataset (copy from Eksperimen)
├── SETUP.md                       # This file
└── README.md                      # Documentation
```

---

## 🚀 Setup Steps

### Step 1: Copy Dataset
```bash
# Copy preprocessed dataset ke MLProject folder
Copy-Item "../Eksperimen_SML_gus_agung/dataset/dataset_clean.csv" `
  -Destination "MLProject/hotel_bookings_preprocessed.csv"
```

Atau download dari:
```
https://drive.google.com/drive/folders/1yYZzVx9AN8R3xFUZrEMAvndNI3PQdrbs
```

### Step 2: Verify MLProject Structure
```bash
cd MLProject

# Check files exist
Get-ChildItem
# Should see:
# - MLproject
# - python_env.yaml
# - modelling_tuning.py
# - hotel_bookings_preprocessed.csv
```

### Step 3: Test MLflow Project Locally (Optional)
```bash
# Install dependencies
pip install mlflow dagshub scikit-learn pandas numpy matplotlib seaborn

# Set environment variables
$env:MLFLOW_TRACKING_URI="https://dagshub.com/gus_agung/hotel-booking-mlflow.mlflow"
$env:DAGSHUB_USER_TOKEN="26046db2b4540bf02257eb5a4b03d1f7acfdd9d7"

# Run MLflow project
mlflow run . --env-manager=local -P data_path="hotel_bookings_preprocessed"
```

### Step 4: Push to GitHub
```bash
cd ..  # Back to Workflow-CI root

# Add all files
git add .
git commit -m "feat: add MLflow CI/CD workflow - ADVANCE level

- MLflow Project with python_env.yaml
- GitHub Actions workflow with 15 steps
- Docker build using mlflow build-docker
- Docker Hub push integration
- Google Drive artifact upload
- DagsHub MLflow tracking

Kriteria 3 - ADVANCE Level (4/4 pts)"

# Push to GitHub
git push origin main
```

### Step 5: Configure GitHub Secrets
1. Buka repository di GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Add 5 required secrets (lihat section "GitHub Secrets Configuration")

### Step 6: Trigger Workflow

#### Option 1: Push Trigger
```bash
# Make any change in MLProject/
echo "# Test" >> MLProject/README.md
git add .
git commit -m "test: trigger CI workflow"
git push origin main
```

#### Option 2: Manual Dispatch
1. Buka GitHub repository
2. Go to **Actions** tab
3. Select "MLflow CI/CD - ADVANCE Level" workflow
4. Click **Run workflow**
5. Fill in experiment name (optional)
6. Click **Run workflow** button

---

## 📊 Workflow Steps Explanation

### Steps 1-5: Setup Environment
1. **Checkout repository** - Clone code
2. **Set up Python 3.12.7** - Install Python
3. **Check Env** - Verify environment
4. **Install dependencies** - Install MLflow, DagsHub, scikit-learn

### Steps 6-7: MLflow Training
5. **Run mlflow project** - Train models dengan MLflow Project
6. **Get latest MLflow run id** - Ambil run ID untuk artifacts

### Steps 8-9: Artifact Management
7. **Install Python dependencies** - Install Google Drive API
8. **Upload to Google Drive** - Upload artifacts ke Google Drive

### Steps 10-13: Docker Deployment
9. **Build Docker Model** - Build image menggunakan `mlflow build-docker`
10. **Log in to Docker Hub** - Authenticate dengan Docker Hub
11. **Tag Docker image** - Tag dengan latest dan commit SHA
12. **Push Docker image** - Push ke Docker Hub repository

### Steps 14-15: Cleanup
13. **Upload workflow artifacts** - Save artifacts ke GitHub
14. **Post actions** - Cleanup actions

---

## 🔍 Verify Workflow Success

### 1. Check GitHub Actions
- Buka **Actions** tab di GitHub
- Lihat workflow run status (harus semua hijau ✅)
- Download artifacts jika tersedia

### 2. Check DagsHub
- Buka https://dagshub.com/gus_agung/hotel-booking-mlflow
- Verify run terbaru ada di experiment
- Check metrics dan artifacts

### 3. Check Docker Hub
- Buka https://hub.docker.com/r/<username>/hotel-booking-model
- Verify image sudah ter-push
- Lihat tags: `latest` dan commit SHA

### 4. Check Google Drive (If configured)
- Buka https://drive.google.com/drive/folders/1yYZzVx9AN8R3xFUZrEMAvndNI3PQdrbs
- Verify artifacts ter-upload

---

## 🐛 Troubleshooting

### Issue 1: MLflow Project Run Failed
```bash
# Check dataset exists
ls MLProject/hotel_bookings_preprocessed.csv

# Check DagsHub credentials
echo $env:DAGSHUB_USER_TOKEN
```

### Issue 2: Docker Build Failed
```bash
# Check models generated
ls MLProject/models/

# Try manual docker build
cd MLProject
docker build -t test-image .
```

### Issue 3: Docker Hub Push Failed
```bash
# Verify Docker Hub credentials
docker login -u <username>

# Check image exists
docker images | grep hotel-booking-model
```

### Issue 4: Google Drive Upload Failed
```
# This is optional - workflow will continue without it
# Check GDRIVE_CREDENTIALS secret is properly formatted JSON
```

---

## 📈 Success Criteria (ADVANCE Level 4/4 pts)

✅ **MLflow Project Structure**
- MLproject file dengan entry points
- python_env.yaml (bukan conda.yaml)
- Training script dengan manual logging

✅ **Artifacts Uploaded**
- Models (.pkl files)
- Plots (PNG images)
- Metrics (logged to DagsHub)

✅ **Docker Integration**
- Build menggunakan `mlflow build-docker`
- Push ke Docker Hub
- Docker_Hub_Link.txt tersimpan

✅ **CI/CD Automation**
- GitHub Actions workflow lengkap
- Multiple triggers (push, PR, manual)
- 15 steps sesuai best practices

---

## 📚 References

- MLflow Projects: https://mlflow.org/docs/latest/projects.html
- MLflow Docker: https://mlflow.org/docs/latest/cli.html#mlflow-models-build-docker
- DagsHub: https://dagshub.com/docs/integration_guide/mlflow_tracking/
- GitHub Actions: https://docs.github.com/en/actions

---

## 🎯 Next Steps

Setelah Kriteria 3 selesai, lanjut ke **Kriteria 4: Monitoring & Logging**

- Setup Prometheus untuk monitoring
- Setup Grafana untuk visualization
- Implement alerting rules
- Create inference service

---

**Author**: gus_agung  
**Level**: ADVANCE (4/4 pts)  
**Date**: 2024
