import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageOps # Kita gunakan Pillow untuk auto-orient

# --- PENGATURAN ---
SOURCE_SPLIT_DIR = "split_dataset"
TARGET_PROCESSED_DIR = "prep_gray"
TARGET_SIZE = (640, 640)
CLASSES_TO_GRAYSCALE = [0, 2] # helmet=0, vest=2
# ------------------

def create_full_processed_dataset():
    print(f"Memulai pembuatan dataset di '{TARGET_PROCESSED_DIR}'...")

    if not os.path.exists(SOURCE_SPLIT_DIR):
        print(f"Error: Folder sumber '{SOURCE_SPLIT_DIR}' tidak ditemukan.")
        return

    for data_split in ["train", "valid", "test"]:
        print(f"\n--- Memproses set: {data_split} ---")
        
        source_img_dir = os.path.join(SOURCE_SPLIT_DIR, data_split, "images")
        source_lbl_dir = os.path.join(SOURCE_SPLIT_DIR, data_split, "labels")
        target_img_dir = os.path.join(TARGET_PROCESSED_DIR, data_split, "images")
        target_lbl_dir = os.path.join(TARGET_PROCESSED_DIR, data_split, "labels")
        
        os.makedirs(target_img_dir, exist_ok=True)
        os.makedirs(target_lbl_dir, exist_ok=True)

        try:
            image_files = [f for f in os.listdir(source_img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            print(f"Memproses {len(image_files)} gambar...")

            for filename in image_files:
                basename, _ = os.path.splitext(filename)
                source_path = os.path.join(source_img_dir, filename)
                output_path = os.path.join(target_img_dir, filename)

                # --- Langkah 1: Buka dengan Pillow untuk Auto-Orient ---
                with Image.open(source_path) as img:
                    img = ImageOps.exif_transpose(img)
                    # Konversi ke format OpenCV (numpy array)
                    image_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                
                height, width, _ = image_cv.shape

                # --- Langkah 2: Auto-Contrast dengan OpenCV (CLAHE) ---
                # Ubah ke LAB color space, terapkan kontras pada L-channel, lalu ubah kembali
                lab = cv2.cvtColor(image_cv, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
                cl = clahe.apply(l)
                limg = cv2.merge((cl,a,b))
                image_contrasted = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

                # --- Langkah 3: Grayscale Selektif ---
                gray_image = cv2.cvtColor(image_contrasted, cv2.COLOR_BGR2GRAY)
                gray_image_3ch = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
                mask = np.zeros(image_contrasted.shape[:2], dtype="uint8")
                
                label_path = os.path.join(source_lbl_dir, f"{basename}.txt")
                if os.path.exists(label_path):
                    with open(label_path, 'r') as f:
                        for line in f:
                            parts = line.strip().split()
                            class_id = int(parts[0])
                            if class_id in CLASSES_TO_GRAYSCALE:
                                x_center, y_center, w, h = map(float, parts[1:])
                                x1, y1 = int((x_center-w/2)*width), int((y_center-h/2)*height)
                                x2, y2 = int((x_center+w/2)*width), int((y_center+h/2)*height)
                                cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
                
                grayscale_part = cv2.bitwise_and(gray_image_3ch, gray_image_3ch, mask=mask)
                color_part = cv2.bitwise_and(image_contrasted, image_contrasted, mask=cv2.bitwise_not(mask))
                processed_image = cv2.add(grayscale_part, color_part)
                
                # --- Langkah 4: Resize (Stretch) ---
                final_image = cv2.resize(processed_image, TARGET_SIZE, interpolation=cv2.INTER_AREA)
                cv2.imwrite(output_path, final_image)

        except FileNotFoundError:
            print(f"  Warning: Folder gambar '{source_img_dir}' tidak ditemukan.")
            continue 

        # Salin file label yang sesuai
        try:
            shutil.copytree(source_lbl_dir, target_lbl_dir, dirs_exist_ok=True)
            print(f"Menyalin {len(os.listdir(source_lbl_dir))} file label...")
        except FileNotFoundError:
            print(f"  Warning: Folder label '{source_lbl_dir}' tidak ditemukan.")
            
    print("\n-------------------------------------------------")
    print("Semua proses selesai!")

if __name__ == "__main__":
    create_full_processed_dataset()