# 🍅 TomatoGuard — Deteksi Penyakit Tomat

Aplikasi web untuk mendeteksi penyakit pada daun tomat secara otomatis menggunakan Deep Learning (MobileNetV2).

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## ✨ Fitur

- 🔍 Deteksi 10 jenis penyakit daun tomat
- 📊 Confidence score & top-K prediksi
- 💊 Informasi penanganan per penyakit
- ⚡ Mode TFLite untuk deployment ringan
- 🎨 UI modern & responsif

## 🚀 Cara Menjalankan Lokal

### 1. Clone repository

```bash
git clone https://github.com/USERNAME/tomatoguard.git
cd tomatoguard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Jalankan aplikasi

```bash
streamlit run app.py
```

## 📦 Deployment ke Streamlit Cloud

### Langkah 1: Konversi model (jika belum ada file `.tflite`)

Jalankan di Google Colab atau environment dengan TensorFlow:

```bash
pip install tensorflow
python convert_to_tflite.py
```

Ini akan menghasilkan `model/tomato_disease_classifier.tflite`.

### Langkah 2: Push ke GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/tomatoguard.git
git push -u origin main
```

### Langkah 3: Deploy di Streamlit Cloud

1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan akun GitHub
3. Pilih repository, branch `main`, dan file `app.py`
4. Klik **Deploy!**

## 📁 Struktur Project

```
streamlit_app/
├── .gitignore
├── .streamlit/
│   └── config.toml          # Konfigurasi tema Streamlit
├── app.py                    # Aplikasi utama
├── convert_to_tflite.py      # Script konversi model
├── requirements.txt          # Dependencies
├── README.md
└── model/
    ├── class_names.json                          # Nama kelas
    ├── tomato_disease_classifier.tflite          # Model TFLite (untuk deploy)
    └── tomato_disease_classifier_final_fixed.h5  # Model asli (untuk dev)
```

## 🧠 Model

| Property | Value |
|----------|-------|
| Arsitektur | MobileNetV2 |
| Transfer Learning | ImageNet |
| Input Size | 224 × 224 px |
| Dataset | PlantifyDR (Kaggle) |
| Jumlah Kelas | 10 |

### Kelas yang Didukung

1. Bacterial Spot
2. Early Blight
3. Healthy
4. Late Blight
5. Leaf Mold
6. Mosaic Virus
7. Septoria Leaf Spot
8. Spider Mites
9. Target Spot
10. Yellow Leaf Curl Virus

## 📄 Lisensi

MIT License
