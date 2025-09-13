import gradio as gr
from ultralytics import YOLO
import torch
import cv2 # Library untuk memproses video
import os

# --- Pengaturan Awal ---
# Cek ketersediaan GPU, jika tidak ada gunakan CPU
device = 0 if torch.cuda.is_available() else "cpu"
print(f"Menggunakan device: {device}")

# Muat model custom 'best.pt' Anda
try:
    model = YOLO("best11.pt")
    model.to(device)
    print("Model 'best11.pt' berhasil dimuat.")
except Exception as e:
    print(f"Error memuat model: {e}")
    # Fallback ke model standar jika 'best.pt' tidak ditemukan
    model = YOLO("yolov8n.pt")
    model.to(device)

# --- Fungsi Deteksi ---

def detect_on_image(image, conf_threshold):
    """Fungsi untuk melakukan deteksi pada satu gambar."""
    if image is None:
        return None
    
    results = model(image, conf=conf_threshold, verbose=False) 
    annotated_image = results[0].plot(masks=False) # masks=False agar tidak ada lapisan warna
    annotated_image_rgb = annotated_image[..., ::-1] # Konversi BGR ke RGB
    
    return annotated_image_rgb

def detect_on_video(video_path, conf_threshold, progress=gr.Progress()):
    """
    Fungsi untuk melakukan deteksi pada file video dengan perbaikan dan logging.
    """
    print("--- FUNGSI DETEKSI VIDEO DIPANGGIL ---")
    if video_path is None:
        print("Path video kosong. Proses dihentikan.")
        return None

    print(f"Menerima path video: {video_path}")

    # Membuat nama file output
    output_folder = "output_videos"
    os.makedirs(output_folder, exist_ok=True)
    video_name = os.path.basename(video_path)
    output_video_path = os.path.join(output_folder, f"detected_{video_name}")
    print(f"Path video output: {output_video_path}")

    # Buka video menggunakan OpenCV
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("!!! ERROR: Gagal membuka file video input.")
        return None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Siapkan penulis video dengan codec yang lebih kompatibel
    fourcc = cv2.VideoWriter_fourcc(*'avc1') # Mengganti codec ke H.264
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    if not out.isOpened():
        print("!!! ERROR: Gagal membuat file video output. Cek codec.")
        cap.release()
        return None

    print("Video berhasil disiapkan. Memulai pemrosesan frame...")
    # Loop melalui setiap frame
    progress(0, desc="Memulai deteksi video...")
    for frame_idx in range(total_frames):
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, conf=conf_threshold, verbose=False)
        annotated_frame = results[0].plot(masks=False)
        out.write(annotated_frame)
        progress((frame_idx + 1) / total_frames, desc=f"Memproses frame {frame_idx+1}/{total_frames}")

    print("Pemrosesan frame selesai. Menutup file...")
    cap.release()
    out.release()
    
    print(f"Video hasil deteksi berhasil disimpan. Mengembalikan path: {output_video_path}")
    return output_video_path

# --- Antarmuka Gradio ---
with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as demo:
    gr.Markdown("# 🚀 Deteksi APD (Helm & Rompi)")
    gr.Markdown("Unggah gambar atau video untuk mendeteksi penggunaan APD pada pekerja.")
    
    with gr.Tabs():
        with gr.TabItem("Unggah Gambar"):
            with gr.Row():
                image_input = gr.Image(type="numpy", label="Input Gambar")
                image_output = gr.Image(label="Hasil Deteksi")
            image_slider = gr.Slider(minimum=0.1, maximum=1.0, value=0.5, step=0.05, label="Confidence Threshold")
            image_button = gr.Button("Deteksi Gambar", variant="primary")

        with gr.TabItem("Unggah Video"):
            with gr.Row():
                video_input = gr.Video(label="Input Video")
                video_output = gr.Video(label="Hasil Deteksi")
            video_slider = gr.Slider(minimum=0.1, maximum=1.0, value=0.5, step=0.05, label="Confidence Threshold")
            video_button = gr.Button("Deteksi Video", variant="primary")
            
    # Hubungkan tombol dengan fungsi yang sesuai
    image_button.click(fn=detect_on_image, inputs=[image_input, image_slider], outputs=image_output)
    video_button.click(fn=detect_on_video, inputs=[video_input, video_slider], outputs=video_output)

# Jalankan aplikasi
if __name__ == "__main__":
    # Install opencv jika belum ada
    try:
        import cv2
    except ImportError:
        print("Menginstall library... pip install opencv-python")
        os.system("pip install opencv-python")

    demo.launch()