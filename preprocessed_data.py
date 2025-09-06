import os
import shutil
from PIL import Image, ImageOps

SOURCE_SPLIT_DIR = "split_dataset"

# Folder tujuan untuk menyimpan semua hasil proses
TARGET_PROCESSED_DIR = "preprocessed_data"

# Ukuran gambar yang diinginkan (lebar, tinggi)
TARGET_SIZE = (640, 640)
# ------------------

def create_processed_dataset():
    """
    Menerapkan preprocessing ke setiap set (train, valid, test)
    dan langsung menyimpannya ke struktur folder target yang baru,
    sambil menyalin file label yang sesuai.
    """
    print(f"Memulai pembuatan dataset di '{TARGET_PROCESSED_DIR}'...")

    if not os.path.exists(SOURCE_SPLIT_DIR):
        print(f"Error: Folder sumber '{SOURCE_SPLIT_DIR}' tidak ditemukan.")
        return

    # Loop untuk setiap set data: train, valid, dan test
    for data_split in ["train", "valid", "test"]:
        print(f"\n--- Memproses set: {data_split} ---")
        
        source_img_dir = os.path.join(SOURCE_SPLIT_DIR, data_split, "images")
        source_lbl_dir = os.path.join(SOURCE_SPLIT_DIR, data_split, "labels")
        
        target_img_dir = os.path.join(TARGET_PROCESSED_DIR, data_split, "images")
        target_lbl_dir = os.path.join(TARGET_PROCESSED_DIR, data_split, "labels")
        
        # 1. Buat struktur folder tujuan
        os.makedirs(target_img_dir, exist_ok=True)
        os.makedirs(target_lbl_dir, exist_ok=True)

        # 2. Proses dan simpan gambar
        try:
            image_files = [f for f in os.listdir(source_img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            total_images = len(image_files)
            print(f"Memproses {total_images} gambar...")

            for i, filename in enumerate(image_files):
                source_path = os.path.join(source_img_dir, filename)
                output_path = os.path.join(target_img_dir, filename)

                with Image.open(source_path) as img:
                    # Terapkan Preprocessing
                    img = ImageOps.exif_transpose(img) # Auto-Orient - Prerocessed 1
                    img = ImageOps.autocontrast(img)   # Auto-Contrast -  Prerocessed 2
                    
                    # Resize dengan padding (letterboxing) -  Prerocessed 3
                    stretched_img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
                    stretched_img.save(output_path)

        except FileNotFoundError:
            print(f"  Warning: Folder gambar '{source_img_dir}' tidak ditemukan. Melewati...")
            continue 

        # 3. Salin file label yang sesuai
        try:
            label_files = [f for f in os.listdir(source_lbl_dir) if f.endswith('.txt')]
            print(f"Menyalin {len(label_files)} file label...")
            for filename in label_files:
                shutil.copy2(os.path.join(source_lbl_dir, filename), target_lbl_dir)
        except FileNotFoundError:
            print(f"  Warning: Folder label '{source_lbl_dir}' tidak ditemukan. Melewati...")
            
    print("\n-------------------------------------------------")
    print("Semua proses selesai!")
    print(f"Dataset Anda siap di dalam folder '{TARGET_PROCESSED_DIR}'.")

if __name__ == "__main__":
    create_processed_dataset()