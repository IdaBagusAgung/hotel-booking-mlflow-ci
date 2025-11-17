# ⚡ Quick Start Guide - Workflow CI/CD

**Tujuan**: Mencapai **ADVANCE Level (4 pts)** untuk Kriteria 3  
**Waktu**: ~20-30 menit  
**Prerequisites**: GitHub account, Docker Hub account, DagsHub account

---

## 🚀 3 Langkah Utama

### 1️⃣ Setup GitHub Repository (5 menit)

```powershell
# A. Buat repository baru
# Buka browser: https://github.com/new
# - Repository name: hotel-booking-mlflow-ci
# - Visibility: Public
# - Klik "Create repository"

# B. Push code
cd "c:\Users\proda\OneDrive\Documents\Gus Agung\ACARA\ACARA AFTER LULUS\Mentor DBS 2026\SUBMISSION\FOLDER_SUBMISSION\Workflow-CI"

git init
git remote add origin https://github.com/gus_agung/hotel-booking-mlflow-ci.git
git add .
git commit -m "Initial commit: MLflow CI/CD - ADVANCE Level"
git branch -M main
git push -u origin main
```

### 2️⃣ Setup GitHub Secrets (5 menit)

```
# Buka di browser:
https://github.com/gus_agung/hotel-booking-mlflow-ci/settings/secrets/actions

# Klik "New repository secret" untuk setiap secret:

1. DAGSHUB_TOKEN
   Value: 26046db2b4540bf02257eb5a4b03d1f7acfdd9d7

2. MLFLOW_TRACKING_USERNAME
   Value: gus_agung

3. MLFLOW_TRACKING_PASSWORD
   Value: 26046db2b4540bf02257eb5a4b03d1f7acfdd9d7

4. DOCKER_USERNAME
   Value: gusagung

5. DOCKER_PASSWORD
   ⚠️ Dapatkan dari Docker Hub:
   - Login ke https://hub.docker.com/
   - Account Settings → Security → New Access Token
   - Name: "GitHub Actions CI/CD"
   - Copy token → Paste sebagai secret value
```

### 3️⃣ Jalankan Workflow (15-20 menit)

```
# Buka di browser:
https://github.com/gus_agung/hotel-booking-mlflow-ci/actions

# 1. Klik workflow "MLflow CI/CD - ADVANCE Level"
# 2. Klik "Run workflow" (tombol hijau)
# 3. Branch: main
# 4. Experiment name: hotel_booking_ci_advance
# 5. Klik "Run workflow"

# 6. Monitor progress (refresh halaman)
# 7. Tunggu ~10-15 menit sampai semua steps selesai ✅
```

---

## ✅ Verifikasi Hasil

### Cek 1: GitHub Actions ✅
```
URL: https://github.com/gus_agung/hotel-booking-mlflow-ci/actions
Expected: Workflow run sukses (green checkmark)
Screenshot: Yes, ambil untuk submission
```

### Cek 2: DagsHub/MLflow ✅
```
URL: https://dagshub.com/gus_agung/hotel-booking-mlflow
Expected: Experiment baru "hotel_booking_ci_advance"
Screenshot: Yes, ambil untuk submission
```

### Cek 3: Docker Hub ✅
```
URL: https://hub.docker.com/r/gusagung/hotel-booking-model
Expected: Image baru dengan tag "latest"
Screenshot: Yes, ambil untuk submission
```

### Cek 4: Google Drive ✅
```
URL: https://drive.google.com/drive/folders/1yYZzVx9AN8R3xFUZrEMAvndNI3PQdrbs
Expected: Artifacts uploaded (atau upload manual)
Screenshot: Yes, ambil untuk submission
```

---

## 🎯 Kriteria ADVANCE (4 pts) - Checklist

- [x] Folder MLProject dengan struktur lengkap
- [x] Workflow CI menggunakan GitHub Actions
- [x] Model training otomatis saat trigger
- [x] Artifacts tersimpan di repository/Google Drive
- [x] Docker image dibuat dengan `mlflow build-docker`
- [x] Docker image di-push ke Docker Hub
- [x] File `Docker_Hub_Link.txt` tersimpan

**Result**: ✅ **ADVANCE (4 pts)**

---

## 📸 Screenshot yang Diperlukan

1. **GitHub Actions**: Workflow run success
2. **DagsHub**: Experiment dengan metrics
3. **Docker Hub**: Repository dengan image
4. **Google Drive**: Folder dengan artifacts
5. **File**: Docker_Hub_Link.txt content

---

## 🆘 Jika Ada Masalah

### Problem 1: Workflow fail di step "Install dependencies"
```powershell
# Solution: Biasanya network issue, retry workflow
```

### Problem 2: "Docker push denied"
```powershell
# Solution: Check DOCKER_PASSWORD secret
# Buat access token baru di Docker Hub
```

### Problem 3: "MLflow tracking authentication failed"
```powershell
# Solution: Check DAGSHUB_TOKEN valid
# Generate token baru di https://dagshub.com/user/settings/tokens
```

---

## 📚 Dokumentasi Lengkap

Untuk detail lebih lengkap, lihat:
- `LANGKAH_EKSEKUSI.md` - Step-by-step lengkap
- `STATUS_DAN_KEKURANGAN.md` - Status dan troubleshooting
- `EXECUTION_GUIDE.md` - Workflow execution guide
- `README.md` - Project overview

---

**Ready? Let's Go!** 🚀

**Time to ADVANCE (4 pts)**: ~20-30 menit dari sekarang!
