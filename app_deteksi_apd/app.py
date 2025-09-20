import streamlit as st
from ultralytics import YOLO
import torch
import cv2
import os
from PIL import Image
import tempfile

# --- Pengaturan Halaman ---
st.set_page_config(page_title="Deteksi APD", page_icon="🚀", layout="wide")

# --- Judul Aplikasi ---
st.title("🚀 Aplikasi Deteksi APD")
st.markdown("Unggah gambar atau video untuk mendeteksi penggunaan APD.")

# --- Pilihan Model di Sidebar ---
st.sidebar.title("Pengaturan Model")
model_list = ["best11s-nongray.pt", "best11s-grayselect.pt", "bestv10m.pt", "bestv10mnograys.pt"]
model_selection = st.sidebar.selectbox("Pilih model yang akan digunakan:", model_list)

# --- Fungsi Caching Model ---
@st.cache_resource
def load_model(model_path):
    device = 0 if torch.cuda.is_available() else "cpu"
    try:
        model = YOLO(model_path)
        model.to(device)
        return model, device
    except Exception as e:
        st.error(f"Error memuat model '{model_path}': {e}")
        return None, None

model, device = load_model(model_selection)
if model:
    st.sidebar.success(f"Model '{model_selection}' berhasil dimuat di device anda")


# --- Tampilan Utama dengan Tab ---
tab1, tab2 = st.tabs(["🖼️ Unggah Gambar", "🎬 Unggah Video"])

# --- TAB UNGGAH GAMBAR ---
with tab1:
    st.header("Deteksi pada Gambar")
    conf_threshold_image = st.slider("Confidence Threshold (Gambar)", 0.1, 1.0, 0.5, 0.05, key="slider_img")
    uploaded_image = st.file_uploader("Pilih sebuah gambar...", type=["jpg", "jpeg", "png"], key="uploader_img")
    
    if uploaded_image and model:
        col1, col2 = st.columns(2)
        image = Image.open(uploaded_image)
        with col1:
            st.image(image, caption="Gambar Asli", use_container_width=True)

        if st.button("Deteksi Gambar"):
                with st.spinner("Sedang memproses..."):
                    results = model(image, conf=conf_threshold_image, verbose=False)
                    
                    # --- UBAH BARIS INI ---
                    annotated_image = results[0].plot(
                        masks=False,
                        line_width=3,       # Lebih tipis
                        font_size=1.5,      # Lebih kecil
                        labels=True,        # Tetap tampilkan label
                        conf=True           # Tetap tampilkan confidence
                    )
                    # ---------------------
                    
                    annotated_image_rgb = annotated_image[..., ::-1]
                    with col2:
                        st.image(annotated_image_rgb, caption="Hasil Deteksi", use_container_width=True)

# --- TAB UNGGAH VIDEO (DENGAN TOMBOL DOWNLOAD DAN UKURAN LABEL DIATUR) ---
with tab2:
    st.header("Deteksi pada Video")
    conf_threshold_video = st.slider("Confidence Threshold (Video)", 0.1, 1.0, 0.5, 0.05, key="slider_vid")
    uploaded_video = st.file_uploader("Pilih sebuah file video...", type=["mp4", "mov", "avi"], key="uploader_vid")
    
    if uploaded_video and model:
        if st.button("Deteksi Video"):
            with st.spinner("Video sedang diproses, ini bisa memakan waktu..."):
                tfile_input = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                tfile_input.write(uploaded_video.read())
                video_path_input = tfile_input.name

                tfile_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                video_path_output = tfile_output.name
                
                # Proses video seperti biasa
                cap = cv2.VideoCapture(video_path_input)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                fps, width, height = (int(cap.get(p)) for p in (cv2.CAP_PROP_FPS, cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))
                out = cv2.VideoWriter(video_path_output, fourcc, fps, (width, height))
                
                progress_bar = st.progress(0, text="Memproses...")
                for frame_idx in range(total_frames):
                    success, frame = cap.read()
                    if not success: break
                    results = model(frame, conf=conf_threshold_video, verbose=False)
                    
                    # --- ATUR UKURAN LABEL BOX DI SINI ---
                    annotated_frame = results[0].plot(
                        masks=False,
                        line_width=3,
                        font_size=1.5,
                        labels=True,
                        conf=True
                    )
                    # -----------------------------------
                    
                    out.write(annotated_frame)
                    progress_bar.progress((frame_idx + 1) / total_frames, text=f"Frame {frame_idx+1}/{total_frames}")

                cap.release()
                out.release()
                
                # Baca file video output sebagai bytes
                with open(video_path_output, 'rb') as video_file:
                    video_bytes = video_file.read()

                st.success("Proses deteksi video selesai!")
                
                # Tampilkan tombol download
                st.download_button(
                    label="📥 Download Video Hasil Deteksi",
                    data=video_bytes,
                    file_name=f"detected_{uploaded_video.name}",
                    mime='video/mp4'
                )

                # Hapus file-file sementara
                # os.remove(video_path_input)
                # os.remove(video_path_output)