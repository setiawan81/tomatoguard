"""
╔══════════════════════════════════════════════════════════════╗
║  TomatoGuard — Konversi Model .h5 → .tflite                ║
║                                                              ║
║  Jalankan script ini di environment yang memiliki TensorFlow ║
║  (misalnya Google Colab, atau Conda dengan Python 3.10-3.12) ║
║                                                              ║
║  Cara pakai:                                                 ║
║    python convert_to_tflite.py                               ║
║                                                              ║
║  Atau di Google Colab:                                       ║
║    1. Upload file .h5 ke Colab                               ║
║    2. Jalankan cell:                                         ║
║       !pip install tensorflow                                ║
║       !python convert_to_tflite.py                           ║
║    3. Download file .tflite yang dihasilkan                  ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys

try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__} terdeteksi")
except ImportError:
    print("❌ TensorFlow tidak terinstall!")
    print("   Install dulu: pip install tensorflow")
    sys.exit(1)

# ─── Konfigurasi ──────────────────────────────────────────────────────────────
H5_PATH = "model/tomato_disease_classifier_final_fixed.h5"
TFLITE_PATH = "model/tomato_disease_classifier.tflite"

# ─── Cek file input ───────────────────────────────────────────────────────────
if not os.path.exists(H5_PATH):
    print(f"❌ File model tidak ditemukan: {H5_PATH}")
    print("   Pastikan script dijalankan dari root folder project.")
    sys.exit(1)

print(f"📂 Loading model dari: {H5_PATH}")
h5_size = os.path.getsize(H5_PATH) / (1024 * 1024)
print(f"   Ukuran file .h5: {h5_size:.1f} MB")

# ─── Load model ───────────────────────────────────────────────────────────────
model = tf.keras.models.load_model(H5_PATH)
print(f"✅ Model berhasil dimuat")
print(f"   Input shape:  {model.input_shape}")
print(f"   Output shape: {model.output_shape}")

# ─── Konversi ke TFLite ───────────────────────────────────────────────────────
print("\n🔄 Mengkonversi ke TFLite...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Optimasi: Dynamic range quantization (mengurangi ukuran ~2-4x)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Konversi
tflite_model = converter.convert()

# ─── Simpan ───────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(TFLITE_PATH), exist_ok=True)
with open(TFLITE_PATH, "wb") as f:
    f.write(tflite_model)

tflite_size = os.path.getsize(TFLITE_PATH) / (1024 * 1024)
reduction = (1 - tflite_size / h5_size) * 100

print(f"\n✅ Konversi berhasil!")
print(f"   File output:  {TFLITE_PATH}")
print(f"   Ukuran .h5:     {h5_size:.1f} MB")
print(f"   Ukuran .tflite: {tflite_size:.1f} MB")
print(f"   Pengurangan:    {reduction:.0f}%")
print(f"\n🚀 File .tflite siap digunakan untuk deployment Streamlit Cloud!")
