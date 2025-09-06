import gradio as gr
from ultralytics import YOLO
import torch

# Cek ketersediaan GPU, jika tidak ada gunakan CPU
device = 0 if torch.cuda.is_available() else "cpu"
print(f"Menggunakan device: {device}")

# Muat model custom 'best.pt' Anda
try:
    model = YOLO("best.pt")
    model.to(device)
    print("Model 'best.pt' berhasil dimuat.")
except Exception as e:
    print(f"Error memuat model: {e}")
    model = YOLO("yolov8n.pt")
    model.to(device)

def detect_apd(frame_or_image):
    if frame_or_image is None:
        return None
    
    results = model(frame_or_image, verbose=False) 
    annotated_frame = results[0].plot()
    annotated_frame_rgb = annotated_frame[..., ::-1]
    
    return annotated_frame_rgb

# --- Gunakan gr.Blocks untuk membuat UI custom dengan Tab ---
with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as demo:
    gr.Markdown("# 🚀 Deteksi APD Real-Time (Helm & Rompi)")
    
    with gr.Tabs():
        with gr.TabItem("Webcam Real-Time"):
            gr.Interface(
                fn=detect_apd,
                inputs=gr.Image(sources=["webcam"], streaming=True, label="Input Webcam"),
                outputs=gr.Image(label="Hasil Deteksi"),
                live=True,
                title="Deteksi dari Webcam",
                description="Arahkan webcam ke seseorang untuk memulai deteksi."
            )
        
        with gr.TabItem("Upload Gambar"):
            gr.Interface(
                fn=detect_apd,
                inputs=gr.Image(sources=["upload"], type="numpy", label="Unggah Gambar Anda"),
                outputs=gr.Image(label="Hasil Deteksi"),
                title="Deteksi dari Gambar",
                description="Unggah sebuah gambar untuk dideteksi."
            )

# Jalankan aplikasi
if __name__ == "__main__":
    demo.launch()