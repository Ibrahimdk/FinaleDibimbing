import os
import random
import shutil

# --- PENGATURAN ---
IMAGE_SOURCE_DIR = "./all_images"
LABEL_SOURCE_DIR = "./all_labels"
TARGET_DIR = "split_dataset"
TRAIN_RATIO = 0.8  # 80% untuk training
VAL_RATIO = 0.15   # 15% untuk validation
# Sisanya (5%) akan menjadi test set
# ------------------

def split_dataset_full():
    """
    Membagi dataset ke dalam struktur folder train/valid/test 
    yang masing-masing berisi subfolder images dan labels.
    """
    print("Memulai proses split dataset (Train/Valid/Test)...")
    
    if TRAIN_RATIO + VAL_RATIO >= 1.0:
        print("Error: Total TRAIN_RATIO dan VAL_RATIO harus kurang dari 1.0.")
        return

    try:
        all_images = [f for f in os.listdir(IMAGE_SOURCE_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(all_images)
    except FileNotFoundError:
        print(f"Error: Folder sumber '{IMAGE_SOURCE_DIR}' tidak ditemukan.")
        return

    total_images = len(all_images)
    train_count = int(total_images * TRAIN_RATIO)
    val_count = int(total_images * VAL_RATIO)

    train_files = all_images[:train_count]
    val_files = all_images[train_count : train_count + val_count]
    test_files = all_images[train_count + val_count:]

    print(f"Total gambar: {total_images}")
    print(f"Jumlah data train: {len(train_files)} ({TRAIN_RATIO:.0%})")
    print(f"Jumlah data validation: {len(val_files)} ({VAL_RATIO:.0%})")
    print(f"Jumlah data test: {len(test_files)} (~{1 - TRAIN_RATIO - VAL_RATIO:.0%})")

    # --- PERUBAHAN 1: Membuat struktur folder baru ---
    # Nama folder validasi diubah menjadi "valid" agar sesuai dengan file yaml
    for d_type in ["train", "valid", "test"]:
        os.makedirs(os.path.join(TARGET_DIR, d_type, "images"), exist_ok=True)
        os.makedirs(os.path.join(TARGET_DIR, d_type, "labels"), exist_ok=True)

    def copy_files(file_list, data_type):
        print(f"\nMenyalin file {data_type}...")
        for filename in file_list:
            basename, _ = os.path.splitext(filename)
            img_src_path = os.path.join(IMAGE_SOURCE_DIR, filename)
            label_src_path = os.path.join(LABEL_SOURCE_DIR, f"{basename}.txt")

            # --- PERUBAHAN 2: Menyesuaikan path tujuan ---
            img_dest_path = os.path.join(TARGET_DIR, data_type, "images", filename)
            label_dest_path = os.path.join(TARGET_DIR, data_type, "labels", f"{basename}.txt")
            
            if os.path.exists(img_src_path): shutil.copy(img_src_path, img_dest_path)
            if os.path.exists(label_src_path): shutil.copy(label_src_path, label_dest_path)

    copy_files(train_files, "train")
    # --- PERUBAHAN 3: Menggunakan "valid" sebagai nama tipe data ---
    copy_files(val_files, "valid") 
    copy_files(test_files, "test")
    
    print("\nProses selesai! Dataset telah berhasil")

if __name__ == "__main__":
    split_dataset_full()