import gradio as gr
from ultralytics import YOLO
import torch

# Cek ketersediaan GPU, jika tidak ada gunakan CPU
device = 0 if torch.cuda.is_available() else "cpu"
print(f"Menggunakan device: {device}")

# Muat model custom 'best9.pt' Anda
try:
    model = YOLO("best9.pt")
    model.to(device)
    print("Model 'best9.pt' berhasil dimuat.")
except Exception as e:
    print(f"Error memuat model: {e}")
    # Fallback ke model standar jika 'best.pt' tidak ditemukan
    model = YOLO("yolov8n.pt")
    model.to(device)

def detect_apd(image, conf_threshold):
    """
    Fungsi untuk melakukan deteksi. 
    Sekarang menerima gambar dan nilai confidence threshold.
    """
    if image is None:
        return None
    
    # Gunakan conf_threshold dari slider
    results = model(image, conf=conf_threshold, verbose=False) 
    
    # Matikan masker agar tidak ada lapisan warna transparan
    annotated_image = results[0].plot(masks=False)
    
    # Konversi BGR (dari OpenCV) ke RGB (untuk Gradio)
    annotated_image_rgb = annotated_image[..., ::-1]
    
    return annotated_image_rgb

# --- Gunakan gr.Blocks untuk membuat UI custom dengan Tab dan Slider ---
with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as demo:
    gr.Markdown("# 🚀 Deteksi APD Real-Time (Helm & Rompi)")
    
    with gr.Tabs():
        with gr.TabItem("Webcam Real-Time"):
            with gr.Row():
                webcam_input = gr.Image(sources=["webcam"], streaming=True, label="Input Webcam")
                webcam_output = gr.Image(label="Hasil Deteksi")
            webcam_slider = gr.Slider(
                minimum=0.1, maximum=1.0, value=0.5, step=0.05, label="Confidence Threshold"
            )
            # Interface untuk streaming webcam tidak bisa pakai tombol, jadi kita gunakan event .stream
            webcam_input.stream(fn=detect_apd, inputs=[webcam_input, webcam_slider], outputs=webcam_output)

        with gr.TabItem("Upload Gambar"):
            with gr.Row():
                image_input = gr.Image(sources=["upload"], type="numpy", label="Unggah Gambar Anda")
                image_output = gr.Image(label="Hasil Deteksi")
            image_slider = gr.Slider(
                minimum=0.1, maximum=1.0, value=0.5, step=0.05, label="Confidence Threshold"
            )
            image_button = gr.Button("Deteksi Gambar", variant="primary")
            
            # Hubungkan tombol dengan fungsi, sertakan slider sebagai input
            image_button.click(fn=detect_apd, inputs=[image_input, image_slider], outputs=image_output)

# Jalankan aplikasi
if __name__ == "__main__":
    demo.launch()