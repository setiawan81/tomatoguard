# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import numpy as np
from PIL import Image
import os
import json

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TomatoGuard — Deteksi Penyakit Tomat",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --green:   #2D6A4F;
    --green2:  #40916C;
    --lime:    #74C69D;
    --cream:   #F8F4EF;
    --red:     #C1392B;
    --yellow:  #F4A261;
    --dark:    #1A1A1A;
    --muted:   #6B7280;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
    color: var(--dark);
}

/* ── Header ─────────────────────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, var(--green) 0%, var(--green2) 60%, var(--lime) 100%);
    border-radius: 20px;
    padding: 48px 40px;
    color: white;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "🍅";
    position: absolute;
    font-size: 180px;
    right: -20px;
    top: -30px;
    opacity: 0.12;
    line-height: 1;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    letter-spacing: -1px;
}
.hero p {
    font-size: 1.1rem;
    margin: 0;
    opacity: 0.9;
    font-weight: 300;
}

/* ── Cards ──────────────────────────────────────────────────────────── */
.card {
    background: white;
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.05);
    margin-bottom: 20px;
    color: #1A1A1A !important;
}
.card * {
    color: #1A1A1A !important;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--green);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Result box ─────────────────────────────────────────────────────── */
.result-healthy {
    background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
    border-left: 5px solid var(--green);
    border-radius: 12px;
    padding: 20px 24px;
    margin: 16px 0;
    color: #1A1A1A !important;
}
.result-healthy * { color: #1A1A1A !important; }
.result-disease {
    background: linear-gradient(135deg, #FEE2E2, #FECACA);
    border-left: 5px solid var(--red);
    border-radius: 12px;
    padding: 20px 24px;
    margin: 16px 0;
    color: #1A1A1A !important;
}
.result-disease * { color: #1A1A1A !important; }
.result-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    margin: 0 0 4px 0;
}
.result-conf {
    font-size: 0.95rem;
    color: var(--muted);
    margin: 0;
}

/* ── Progress bar override ──────────────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--green2), var(--lime));
    border-radius: 8px;
}

/* ── Sidebar ─────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--dark) !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] p {
    color: #9CA3AF !important;
}

/* ── Top-k bar item ─────────────────────────────────────────────────── */
.topk-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #F3F4F6;
    font-size: 0.9rem;
}
.topk-item:last-child { border-bottom: none; }
.topk-rank {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    color: var(--green);
    width: 28px;
}
.topk-name { flex: 1; padding: 0 12px; }
.topk-score {
    font-weight: 600;
    color: #1A1A1A !important;
    min-width: 52px;
    text-align: right;
}

/* ── Pill badges ─────────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.badge-green { background:#D1FAE5; color:var(--green); }
.badge-red   { background:#FEE2E2; color:var(--red);   }
.badge-yellow{ background:#FEF3C7; color:#92400E;      }

/* ── File uploader ──────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--lime) !important;
    border-radius: 12px !important;
    background: rgba(116,198,157,0.06) !important;
}

/* ── Divider ─────────────────────────────────────────────────────────── */
hr { border-color: #F3F4F6; margin: 24px 0; }

/* ── Hide streamlit branding ─────────────────────────────────────────── */
#MainMenu, footer { visibility: hidden; }
/* Biarkan header tampil agar tombol sidebar tetap berfungsi */
</style>
""", unsafe_allow_html=True)


# ─── Constants ────────────────────────────────────────────────────────────────
IMG_SIZE = (224, 224)
TFLITE_MODEL_PATH = "model/tomato_disease_classifier.tflite"
H5_MODEL_PATH = "model/tomato_disease_classifier_final_fixed.h5"
CLASS_NAMES_PATH = "model/class_names.json"

DISEASE_INFO = {
    "Tomato_Bacterial_spot": {
        "label": "Bacterial Spot",
        "emoji": "🦠",
        "severity": "Sedang",
        "badge": "badge-yellow",
        "desc": "Bercak coklat kecil pada daun dengan tepi kuning. Disebabkan oleh bakteri Xanthomonas.",
        "treatment": "Semprot fungisida tembaga. Hindari irigasi overhead. Rotasi tanaman.",
    },
    "Tomato_Early_blight": {
        "label": "Early Blight",
        "emoji": "🟤",
        "severity": "Sedang",
        "badge": "badge-yellow",
        "desc": "Bercak konsentris seperti target pada daun tua. Disebabkan oleh jamur Alternaria solani.",
        "treatment": "Aplikasi fungisida klorotalonil atau mankozeb. Buang daun terinfeksi.",
    },
    "Tomato_Late_blight": {
        "label": "Late Blight",
        "emoji": "⚠️",
        "severity": "Tinggi",
        "badge": "badge-red",
        "desc": "Bercak basah abu-abu kehijauan yang menyebar cepat. Sangat destruktif, disebabkan Phytophthora infestans.",
        "treatment": "Segera semprot fungisida sistemik. Isolasi tanaman terinfeksi. Hindari kelembapan tinggi.",
    },
    "Tomato_Leaf_Mold": {
        "label": "Leaf Mold",
        "emoji": "🌫️",
        "severity": "Rendah",
        "badge": "badge-green",
        "desc": "Lapisan jamur kuning-hijau di bawah daun. Disebabkan oleh Passalora fulva.",
        "treatment": "Tingkatkan sirkulasi udara. Kurangi kelembapan. Fungisida ringan.",
    },
    "Tomato_Septoria_leaf_spot": {
        "label": "Septoria Leaf Spot",
        "emoji": "🔵",
        "severity": "Sedang",
        "badge": "badge-yellow",
        "desc": "Bercak kecil bulat dengan pusat putih dan tepi coklat. Disebabkan Septoria lycopersici.",
        "treatment": "Fungisida klorotalonil. Buang dan musnahkan daun yang terinfeksi.",
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "label": "Spider Mites",
        "emoji": "🕷️",
        "severity": "Sedang",
        "badge": "badge-yellow",
        "desc": "Bintik-bintik kuning kecil pada daun akibat gigitan tungau. Terlihat jaring halus di bawah daun.",
        "treatment": "Semprotkan akarisida atau air sabun. Tingkatkan kelembapan. Predator alami.",
    },
    "Tomato__Target_Spot": {
        "label": "Target Spot",
        "emoji": "🎯",
        "severity": "Sedang",
        "badge": "badge-yellow",
        "desc": "Lesi besar dengan pola cincin konsentris. Disebabkan oleh Corynespora cassiicola.",
        "treatment": "Fungisida sistemik. Perbaiki drainase. Hindari pemupukan nitrogen berlebih.",
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "label": "Yellow Leaf Curl Virus",
        "emoji": "🟡",
        "severity": "Tinggi",
        "badge": "badge-red",
        "desc": "Daun menggulung, menguning, dan mengkerut. Ditularkan oleh kutu kebul (Bemisia tabaci).",
        "treatment": "Tidak ada obat. Cabut tanaman terinfeksi. Kendalikan kutu kebul dengan insektisida.",
    },
    "Tomato__Tomato_mosaic_virus": {
        "label": "Mosaic Virus",
        "emoji": "🌿",
        "severity": "Tinggi",
        "badge": "badge-red",
        "desc": "Pola mosaik hijau-kuning tidak beraturan pada daun. Virus menyebar melalui kontak dan alat.",
        "treatment": "Tidak ada obat. Cabut tanaman sakit. Sterilkan alat. Gunakan benih bersertifikat.",
    },
    "Tomato_healthy": {
        "label": "Daun Sehat",
        "emoji": "✅",
        "severity": "Sehat",
        "badge": "badge-green",
        "desc": "Daun tomat dalam kondisi sehat tanpa tanda-tanda penyakit.",
        "treatment": "Pertahankan kondisi saat ini. Lanjutkan perawatan rutin.",
    },
}

def get_info(class_name):
    def normalize(s):
        return s.lower().replace("_", " ").replace("-", " ").strip()
    cn = normalize(class_name)
    for key in DISEASE_INFO:
        kn = normalize(key)
        if kn in cn or cn in kn:
            return DISEASE_INFO[key]
    # Fallback: cocokkan minimal 2 kata
    cn_words = set(cn.split())
    for key in DISEASE_INFO:
        kn_words = set(normalize(key).split())
        if len(cn_words & kn_words) >= 2:
            return DISEASE_INFO[key]
    return {
        "label": class_name.replace("_", " "),
        "emoji": "🍃",
        "severity": "Tidak Diketahui",
        "badge": "badge-yellow",
        "desc": "Informasi tambahan belum tersedia.",
        "treatment": "-",
    }


# ─── Load model (dual-mode: TFLite preferred, TensorFlow fallback) ───────────
@st.cache_resource(show_spinner=False)
def load_model():
    """
    Coba load model dengan urutan prioritas:
    1. TFLite (.tflite) — ringan, cocok untuk Streamlit Cloud
    2. TensorFlow (.h5) — fallback untuk development lokal
    
    Returns: (model_object, class_names, model_type)
    model_type: "tflite" atau "tensorflow"
    """
    # Load class names
    class_names = None
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH) as f:
            class_names = json.load(f)

    # ── Prioritas 1: TFLite ──────────────────────────────────────────────
    if os.path.exists(TFLITE_MODEL_PATH):
        try:
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter(model_path=TFLITE_MODEL_PATH)
            interpreter.allocate_tensors()
            if class_names is None:
                output_shape = interpreter.get_output_details()[0]['shape']
                class_names = [f"Kelas_{i}" for i in range(output_shape[-1])]
            return interpreter, class_names, "tflite"
        except ImportError:
            # tflite_runtime tidak tersedia, coba lewat tensorflow
            try:
                import tensorflow as tf
                interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL_PATH)
                interpreter.allocate_tensors()
                if class_names is None:
                    output_shape = interpreter.get_output_details()[0]['shape']
                    class_names = [f"Kelas_{i}" for i in range(output_shape[-1])]
                return interpreter, class_names, "tflite"
            except ImportError:
                pass  # Lanjut ke fallback .h5

    # ── Prioritas 2: TensorFlow .h5 ─────────────────────────────────────
    if os.path.exists(H5_MODEL_PATH):
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(H5_MODEL_PATH)
            if class_names is None:
                class_names = [f"Kelas_{i}" for i in range(model.output_shape[-1])]
            return model, class_names, "tensorflow"
        except ImportError:
            pass

    return None, None, None


# ─── Predict (supports both TFLite and TensorFlow) ───────────────────────────
def predict(model, class_names, image: Image.Image, top_k=3, model_type="tflite"):
    img = image.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, 0)

    if model_type == "tflite":
        # TFLite inference
        input_details = model.get_input_details()
        output_details = model.get_output_details()
        model.set_tensor(input_details[0]['index'], arr)
        model.invoke()
        preds = model.get_tensor(output_details[0]['index'])[0]
    else:
        # TensorFlow inference
        preds = model.predict(arr, verbose=0)[0]

    top_idx = np.argsort(preds)[::-1][:top_k]
    results = [(class_names[i], float(preds[i])) for i in top_idx]
    return results


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍅 TomatoGuard")
    st.markdown("---")
    st.markdown("### ⚙️ Pengaturan")
    top_k = st.slider("Jumlah top prediksi", 1, 5, 3)
    conf_threshold = st.slider("Minimum confidence (%)", 0, 100, 30) / 100
    st.markdown("---")
    st.markdown("### 📋 Panduan")
    st.markdown("""
- Upload foto daun tomat yang jelas
- Pastikan fokus pada area daun
- Pencahayaan cukup & latar bersih
- Format: JPG, PNG, WEBP
    """)
    st.markdown("---")
    st.markdown("### 🔬 Model Info")
    st.markdown("""
**Arsitektur:** MobileNetV2  
**Transfer Learning:** ImageNet  
**Input Size:** 224 × 224 px  
**Dataset:** PlantifyDR (Kaggle)  
    """)


# ─── Main content ──────────────────────────────────────────────────────────────
# Hero
st.markdown("""
<div class="hero">
  <h1>🍅 TomatoGuard</h1>
  <p>Deteksi penyakit tanaman tomat secara otomatis menggunakan Deep Learning (MobileNetV2)</p>
</div>
""", unsafe_allow_html=True)

# Load model
with st.spinner("Memuat model..."):
    model, class_names, model_type = load_model()

if model is None:
    st.error(
        "⚠️ **File model tidak ditemukan atau library tidak tersedia.**\n\n"
        "Pastikan salah satu file model ada di:\n"
        "```\nmodel/tomato_disease_classifier.tflite   (direkomendasikan)\n"
        "model/tomato_disease_classifier_final_fixed.h5   (fallback)\n```\n\n"
        "Dan install salah satu library:\n"
        "```\npip install tflite-runtime   (ringan, untuk deployment)\n"
        "pip install tensorflow       (untuk development)\n```"
    )
    st.info(
        "💡 **Cara konversi model ke TFLite:**\n\n"
        "Jalankan script `convert_to_tflite.py` di environment yang memiliki TensorFlow:\n"
        "```python\npython convert_to_tflite.py\n```\n"
        "Atau jalankan di Google Colab."
    )
    st.stop()

# Tampilkan info model yang digunakan
model_label = "⚡ TFLite (ringan)" if model_type == "tflite" else "🧠 TensorFlow (full)"
st.success(f"✅ Model berhasil dimuat — {len(class_names)} kelas terdeteksi | Mode: {model_label}")

st.markdown("---")

# Upload section
col_upload, col_result = st.columns([1, 1], gap="large")

with col_upload:
    st.markdown('<div class="card-title">📤 Upload Gambar Daun</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drag & drop atau klik untuk memilih file",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption=f"📁 {uploaded.name}", use_container_width=True)
        st.caption(f"Resolusi: {image.width} × {image.height} px | Format: {image.format or uploaded.type}")

with col_result:
    st.markdown('<div class="card-title">🔍 Hasil Analisis</div>', unsafe_allow_html=True)

    if not uploaded:
        st.markdown("""
        <div style="
            background: white;
            border: 2px dashed #D1D5DB;
            border-radius: 16px;
            padding: 60px 24px;
            text-align: center;
            color: #9CA3AF;
        ">
            <div style="font-size: 3rem; margin-bottom: 12px;">🌿</div>
            <p style="font-size: 1rem; margin: 0;">Upload gambar untuk memulai deteksi</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🔄 Menganalisis gambar..."):
            results = predict(model, class_names, image, top_k=top_k, model_type=model_type)

        top_class, top_conf = results[0]
        info = get_info(top_class)
        is_healthy = "healthy" in top_class.lower()

        # Main result card
        box_cls = "result-healthy" if is_healthy else "result-disease"
        badge_html = f'<span class="badge {info["badge"]}">{info["severity"]}</span>'

        st.markdown(f"""
        <div class="{box_cls}">
            <p class="result-label">{info["emoji"]} {info["label"]}</p>
            <p class="result-conf">Confidence: <strong>{top_conf*100:.1f}%</strong> &nbsp;|&nbsp; Tingkat Keparahan: {badge_html}</p>
        </div>
        """, unsafe_allow_html=True)

        # Confidence gauge
        st.markdown("**Confidence Score**")
        st.progress(min(top_conf, 1.0))

        # Warning jika confidence rendah
        if top_conf < conf_threshold:
            st.warning(f"⚠️ Confidence rendah ({top_conf*100:.1f}%). Coba foto yang lebih jelas.")

        # Description & treatment
        st.markdown(f"**📋 Deskripsi:** {info['desc']}")
        st.markdown(f"**💊 Penanganan:** {info['treatment']}")

        # Top-K
        if top_k > 1:
            st.markdown("---")
            st.markdown("**Top Prediksi Lainnya**")
            for rank, (cls, conf) in enumerate(results, 1):
                inf = get_info(cls)
                st.markdown(f"""
                <div class="topk-item">
                    <span class="topk-rank">#{rank}</span>
                    <span class="topk-name">{inf['emoji']} {inf['label']}</span>
                    <span class="topk-score">{conf*100:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
                st.progress(conf)

# ─── Info kelas ───────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📚 Daftar Penyakit yang Dapat Dideteksi"):
    cols = st.columns(2)
    for i, (key, info) in enumerate(DISEASE_INFO.items()):
        with cols[i % 2]:
            badge = f'<span class="badge {info["badge"]}">{info["severity"]}</span>'
            st.markdown(f"""
            <div class="card" style="padding:16px 20px; margin-bottom: 12px; background:white; color:#1A1A1A;">
                <div style="font-size: 0.95rem; font-weight: 600; color:#1A1A1A;">{info['emoji']} {info['label']} &nbsp;{badge}</div>
                <div style="font-size: 0.82rem; color: #6B7280; margin-top: 6px;">{info['desc']}</div>
            </div>
            """, unsafe_allow_html=True)