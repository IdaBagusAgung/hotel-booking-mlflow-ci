# 🚀 Langkah Eksekusi Workflow CI/CD - ADVANCE Level (4 pts)

## 📋 Daftar Isi
1. [Persiapan Awal](#1-persiapan-awal)
2. [Setup GitHub Repository](#2-setup-github-repository)
3. [Setup GitHub Secrets](#3-setup-github-secrets)
4. [Setup Google Drive](#4-setup-google-drive)
5. [Eksekusi Workflow](#5-eksekusi-workflow)
6. [Verifikasi Hasil](#6-verifikasi-hasil)
7. [Testing Manual (Opsional)](#7-testing-manual-opsional)

---

## 1. Persiapan Awal

### ✅ Checklist Persiapan
- [ ] File `modelling.py` siap dan teruji
- [ ] File `modelling_tuning.py` siap dan teruji
- [ ] Dataset preprocessing sudah ada di folder `hotel_bookings_preprocessed/`
- [ ] Akun DagsHub aktif dan token tersedia
- [ ] Akun Docker Hub aktif dan credentials tersedia
- [ ] Google Drive folder sudah disiapkan

### 📁 Struktur yang Diperlukan
```
Workflow-CI/
├── .env                           # ✅ Sudah ada
├── .github/
│   └── workflows/
│       └── mlflow_ci.yml         # ✅ Sudah ada
├── MLProject/
│   ├── modelling.py              # ✅ Sudah ada
│   ├── modelling_tuning.py       # ✅ Sudah ada
│   ├── conda.yaml                # ✅ Sudah ada
│   ├── python_env.yaml           # ✅ Sudah ada
│   ├── MLproject                 # ✅ Sudah ada
│   ├── Docker_Hub_Link.txt       # 🔄 Akan dibuat otomatis
│   └── hotel_bookings_preprocessed/
│       ├── X_train.csv           # ✅ Sudah ada
│       ├── X_test.csv            # ✅ Sudah ada
│       ├── y_train.csv           # ✅ Sudah ada
│       └── y_test.csv            # ✅ Sudah ada
└── README.md                     # ✅ Sudah ada
```

---

## 2. Setup GitHub Repository

### 2.1. Buat Repository Baru di GitHub

1. **Buka GitHub**: https://github.com/new
2. **Buat repository baru**:
   ```
   Repository name: hotel-booking-mlflow-ci
   Description: MLflow CI/CD Pipeline for Hotel Booking Cancellation Prediction
   Visibility: Public atau Private (pilih sesuai kebutuhan)
   ✅ Add README file: TIDAK perlu (sudah ada)
   ```

3. **Klik "Create repository"**

### 2.2. Push Code ke GitHub

Buka PowerShell di folder `Workflow-CI/` dan jalankan:

```powershell
# Inisialisasi Git (jika belum)
git init

# Tambahkan remote repository
git remote add origin https://github.com/gus_agung/hotel-booking-mlflow-ci.git

# Buat .gitignore
@"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# MLflow
mlruns/
mlartifacts/
outputs/
artifacts/
plots/
models/*.pkl

# Environment
.env

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"@ | Out-File -FilePath .gitignore -Encoding utf8

# Add semua file
git add .

# Commit
git commit -m "Initial commit: MLflow CI/CD Pipeline - ADVANCE Level"

# Push ke GitHub
git branch -M main
git push -u origin main
```

---

## 3. Setup GitHub Secrets

### 3.1. Buka Settings > Secrets and Variables > Actions

Pada repository GitHub Anda, buka:
```
Settings → Secrets and variables → Actions → New repository secret
```

### 3.2. Tambahkan Secret Berikut

| Secret Name | Value | Keterangan |
|------------|-------|------------|
| `DAGSHUB_TOKEN` | `26046db2b4540bf02257eb5a4b03d1f7acfdd9d7` | Token DagsHub untuk akses MLflow |
| `MLFLOW_TRACKING_USERNAME` | `gus_agung` | Username DagsHub |
| `MLFLOW_TRACKING_PASSWORD` | `26046db2b4540bf02257eb5a4b03d1f7acfdd9d7` | Token DagsHub (sama dengan DAGSHUB_TOKEN) |
| `DOCKER_USERNAME` | `gusagung` | Username Docker Hub |
| `DOCKER_PASSWORD` | `<your_docker_password>` | ⚠️ Password Docker Hub Anda |
| `GDRIVE_CREDENTIALS` | `<credentials_json>` | ⚠️ Google Drive OAuth credentials (opsional) |

#### ⚠️ Catatan Penting:
- **`DOCKER_PASSWORD`**: Gunakan password Docker Hub Anda atau buat Docker Access Token:
  1. Login ke https://hub.docker.com/
  2. Account Settings → Security → New Access Token
  3. Copy token dan gunakan sebagai `DOCKER_PASSWORD`

- **`GDRIVE_CREDENTIALS`** (Opsional): Jika ingin upload ke Google Drive, lihat [Setup Google Drive](#4-setup-google-drive)

---

## 4. Setup Google Drive

### 4.1. Buat OAuth 2.0 Credentials (Opsional - untuk Auto Upload)

Jika Anda ingin **automated upload** ke Google Drive:

1. **Buka Google Cloud Console**: https://console.cloud.google.com/
2. **Buat Project Baru**: "hotel-booking-ci"
3. **Enable Google Drive API**:
   - APIs & Services → Library
   - Cari "Google Drive API" → Enable

4. **Buat OAuth 2.0 Credentials**:
   - APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID
   - Application type: Desktop app
   - Name: "hotel-booking-ci-app"
   - Download JSON credentials

5. **Generate Refresh Token**:
   ```powershell
   # Install library
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

   # Buat script generate_token.py
   @"
   from google_auth_oauthlib.flow import InstalledAppFlow
   import json
   
   SCOPES = ['https://www.googleapis.com/auth/drive.file']
   
   flow = InstalledAppFlow.from_client_secrets_file(
       'credentials.json', SCOPES)
   creds = flow.run_local_server(port=0)
   
   # Save credentials
   creds_data = {
       'token': creds.token,
       'refresh_token': creds.refresh_token,
       'token_uri': creds.token_uri,
       'client_id': creds.client_id,
       'client_secret': creds.client_secret,
       'scopes': creds.scopes
   }
   
   print(json.dumps(creds_data))
   "@ | Out-File -FilePath generate_token.py -Encoding utf8

   # Jalankan
   python generate_token.py
   ```

6. **Copy JSON output** dan simpan sebagai `GDRIVE_CREDENTIALS` secret di GitHub

### 4.2. Manual Upload (Alternatif - Lebih Mudah)

Jika tidak ingin setup OAuth, Anda bisa:
1. Download artifacts dari GitHub Actions
2. Upload manual ke Google Drive folder: https://drive.google.com/drive/u/0/folders/1yYZzVx9AN8R3xFUZrEMAvndNI3PQdrbs

---

## 5. Eksekusi Workflow

### 5.1. Trigger via Push (Otomatis)

Workflow akan **otomatis berjalan** ketika:
```powershell
# Setiap push ke branch main atau develop
git add .
git commit -m "Update model atau konfigurasi"
git push origin main
```

### 5.2. Trigger Manual (workflow_dispatch)

1. **Buka GitHub Repository**
2. **Actions tab**
3. **Pilih workflow "MLflow CI/CD - ADVANCE Level"**
4. **Klik "Run workflow"**
5. **Isi parameter**:
   - Branch: `main`
   - Experiment name: `hotel_booking_ci_advance` (atau custom)
6. **Klik "Run workflow"**

### 5.3. Monitor Eksekusi

Workflow akan menjalankan langkah-langkah berikut:

| Step | Deskripsi | Durasi Estimasi |
|------|-----------|-----------------|
| 1. Checkout | Clone repository | ~10 detik |
| 2. Setup Python | Install Python 3.12.7 | ~20 detik |
| 3. Check Env | Verifikasi environment | ~5 detik |
| 4. Install Dependencies | Install MLflow, scikit-learn, dll | ~1-2 menit |
| 5. Run MLflow Project | Training model dengan MLflow | ~3-5 menit |
| 6. Get Run ID | Ambil latest run ID dari MLflow | ~10 detik |
| 7. Install GDrive Deps | Install Google Drive libraries | ~30 detik |
| 8. Upload to Google Drive | Upload artifacts ke GDrive | ~30 detik - 1 menit |
| 9. Build Docker Model | Build Docker image dengan mlflow | ~2-3 menit |
| 10. Login Docker Hub | Authenticate ke Docker Hub | ~10 detik |
| 11. Tag Docker Image | Tag image dengan SHA | ~5 detik |
| 12. Push to Docker Hub | Push image ke registry | ~1-2 menit |
| 13. Upload Artifacts | Upload ke GitHub Actions artifacts | ~30 detik |

**Total Estimasi**: ~10-15 menit

---

## 6. Verifikasi Hasil

### 6.1. Verifikasi di DagsHub (MLflow Tracking)

1. **Buka DagsHub**: https://dagshub.com/gus_agung/hotel-booking-mlflow
2. **Navigate ke "Experiments"**
3. **Cari experiment**: `hotel_booking_ci_advance`
4. **Verifikasi**:
   - ✅ Run baru dengan timestamp terbaru
   - ✅ Metrics: accuracy, precision, recall, f1_score, roc_auc
   - ✅ Parameters: model_type, n_estimators, max_depth, dll
   - ✅ Model artifacts tersimpan
   - ✅ Classification report tersimpan

**Screenshot**: Ambil screenshot halaman experiment untuk submission

### 6.2. Verifikasi di Docker Hub

1. **Buka Docker Hub**: https://hub.docker.com/repository/docker/gusagung/hotel-booking-model/general
2. **Verifikasi**:
   - ✅ Image baru dengan tag `latest`
   - ✅ Image dengan tag SHA commit (e.g., `abc123def`)
   - ✅ Size image reasonable (~500MB - 1GB)
   - ✅ Last pushed timestamp terbaru

**Screenshot**: Ambil screenshot halaman Docker Hub untuk submission

### 6.3. Verifikasi di Google Drive

1. **Buka Google Drive**: https://drive.google.com/drive/u/0/folders/1yYZzVx9AN8R3xFUZrEMAvndNI3PQdrbs
2. **Verifikasi file yang di-upload**:
   - ✅ `run_info.txt` - informasi run ID dan timestamp
   - ✅ Model artifacts (jika ada)
   - ✅ Plots (jika ada)

**Screenshot**: Ambil screenshot Google Drive folder untuk submission

### 6.4. Verifikasi di GitHub Actions

1. **Buka GitHub Repository → Actions**
2. **Verifikasi**:
   - ✅ Workflow run sukses (green checkmark)
   - ✅ Semua steps passed
   - ✅ Artifacts tersedia untuk download
   - ✅ Logs lengkap dan tidak ada error

**Screenshot**: Ambil screenshot workflow run untuk submission

### 6.5. Download dan Verifikasi Artifacts

```powershell
# Download artifacts dari GitHub Actions
# (bisa via UI atau GitHub CLI)

# Extract dan cek isi
cd mlflow-ci-artifacts-<sha>/
ls -R

# Verifikasi file:
# - models/          # Model files
# - artifacts/       # Training artifacts
# - plots/           # Visualizations
# - Docker_Hub_Link.txt  # Link ke Docker Hub
```

---

## 7. Testing Manual (Opsional)

### 7.1. Test MLflow Project Locally

```powershell
# Navigate ke folder MLProject
cd MLProject

# Set environment variables
$env:MLFLOW_TRACKING_URI = "https://dagshub.com/gus_agung/hotel-booking-mlflow.mlflow"
$env:DAGSHUB_TOKEN = "26046db2b4540bf02257eb5a4b03d1f7acfdd9d7"

# Run MLflow project
mlflow run . `
  --experiment-name "hotel_booking_test_local" `
  --env-manager=local `
  -P data_path="hotel_bookings_preprocessed" `
  -P experiment_name="hotel_booking_test_local"
```

### 7.2. Test Docker Image Locally

```powershell
# Pull Docker image dari Docker Hub
docker pull gusagung/hotel-booking-model:latest

# Jalankan container
docker run -p 8080:8080 gusagung/hotel-booking-model:latest

# Test inference (di terminal lain)
Invoke-WebRequest -Uri http://localhost:8080/invocations `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"data": [[...]]}'
```

### 7.3. Test Google Drive Upload Manually

```powershell
# Buat script test_gdrive.py
@"
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json

# Load credentials
creds = Credentials.from_authorized_user_file('gdrive_creds.json')
service = build('drive', 'v3', credentials=creds)

# Create test file
with open('test_artifact.txt', 'w') as f:
    f.write('Test artifact from local machine')

# Upload
file_metadata = {
    'name': 'test_artifact.txt',
    'parents': ['1yYZzVx9AN8R3xFUZrEMAvndNI3PQdrbs']
}
media = MediaFileUpload('test_artifact.txt', resumable=True)
file = service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id,name,webViewLink'
).execute()

print(f'Uploaded: {file.get(\"webViewLink\")}')
"@ | Out-File -FilePath test_gdrive.py -Encoding utf8

python test_gdrive.py
```

---

## 📊 Checklist Lengkap untuk Kriteria ADVANCE (4 pts)

### ✅ Mandatory Requirements

- [ ] **Folder MLProject** sudah dibuat dengan struktur lengkap
- [ ] **File MLproject** (MLflow project config) ada dan valid
- [ ] **Workflow CI** (`.github/workflows/mlflow_ci.yml`) berjalan sukses
- [ ] **Model training** otomatis saat trigger (push/manual)
- [ ] **Artifacts tersimpan** di repository atau Google Drive
- [ ] **Docker image** berhasil di-build menggunakan `mlflow build-docker`
- [ ] **Docker image** berhasil di-push ke Docker Hub
- [ ] **Docker Hub link** tersimpan di `Docker_Hub_Link.txt`

### 📸 Screenshot yang Diperlukan untuk Submission

1. **GitHub Actions**:
   - Workflow run sukses (semua steps green)
   - Artifacts yang di-upload

2. **DagsHub/MLflow**:
   - Experiment dengan run terbaru
   - Metrics dan parameters
   - Model artifacts

3. **Docker Hub**:
   - Repository dengan image terbaru
   - Tags (latest dan SHA)

4. **Google Drive**:
   - Folder dengan artifacts yang di-upload

5. **File `Docker_Hub_Link.txt`**:
   - Isi file dengan link Docker Hub

---

## 🎯 Kriteria Penilaian

| Kriteria | Status | Poin |
|----------|--------|------|
| Reject: Tidak ada folder MLProject & workflow CI | ❌ | 0 pts |
| Basic: Folder MLProject + workflow CI berjalan | ✅ | 2 pts |
| Skilled: + Artifacts tersimpan di repo/Google Drive | ✅ | 3 pts |
| **Advance: + Docker image dengan mlflow build-docker** | ✅ | **4 pts** |

**Target Anda**: **ADVANCE (4 pts)** ✅

---

## 🚨 Troubleshooting

### Issue 1: GitHub Actions Fail pada Step "Run MLflow Project"

**Penyebab**: Missing secrets atau environment variables

**Solusi**:
```yaml
# Pastikan secrets sudah diset:
- DAGSHUB_TOKEN
- MLFLOW_TRACKING_USERNAME
- MLFLOW_TRACKING_PASSWORD
```

### Issue 2: Docker Build Gagal

**Penyebab**: Model tidak ditemukan atau MLflow registry issue

**Solusi**:
```powershell
# Cek model ada di mlflow registry
mlflow models list

# Atau build manual
cd MLProject
mlflow models build-docker -m "models:/hotel_booking_cancellation_predictor/latest" -n gusagung/hotel-booking-model
```

### Issue 3: Push Docker Image Gagal

**Penyebab**: Docker Hub credentials salah

**Solusi**:
```powershell
# Test login manual
docker login -u gusagung

# Atau buat access token baru di Docker Hub
# Settings → Security → New Access Token
```

### Issue 4: Google Drive Upload Gagal

**Penyebab**: Credentials tidak valid atau expired

**Solusi**:
```yaml
# Opsi 1: Skip Google Drive upload (tidak mandatory)
# Workflow akan continue jika upload gagal

# Opsi 2: Upload manual dari artifacts yang di-download
```

---

## 📞 Support

Jika ada masalah:
1. Cek GitHub Actions logs untuk detail error
2. Cek DagsHub MLflow tracking untuk run details
3. Review dokumentasi MLflow: https://mlflow.org/docs/latest/projects.html
4. Review dokumentasi GitHub Actions: https://docs.github.com/en/actions

---

## 🎉 Selamat!

Jika semua langkah di atas berhasil, Anda telah mencapai **ADVANCE Level (4 pts)** untuk Kriteria 3! 🏆

**Next Steps**:
- Compile semua screenshot untuk submission
- Buat dokumentasi lengkap di README.md
- Siapkan presentasi/demo untuk review

---

**Last Updated**: November 17, 2025
**Author**: gus_agung
**Version**: 1.0 - ADVANCE Level
