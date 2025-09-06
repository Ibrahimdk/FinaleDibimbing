import os
import shutil

# --- PENGATURAN ---
SOURCE_IMG_DIR = "all_images"
SOURCE_LBL_DIR = "all_labels"
TARGET_DIR = "augment_temp"
CLASS_ID_TO_FILTER = 1  # Pastikan ID untuk 'no-helmet' adalah 1
# ------------------

def filter_and_copy():
    target_img_dir = os.path.join(TARGET_DIR, "images")
    target_lbl_dir = os.path.join(TARGET_DIR, "labels")

    os.makedirs(target_img_dir, exist_ok=True)
    os.makedirs(target_lbl_dir, exist_ok=True)

    try:
        label_files = os.listdir(SOURCE_LBL_DIR)
    except FileNotFoundError:
        print(f"Error: Folder '{SOURCE_LBL_DIR}' tidak ditemukan.")
        return

    print(f"Memindai {len(label_files)} file label untuk kelas ID: {CLASS_ID_TO_FILTER}...")
    
    found_count = 0
    for label_file in label_files:
        if not label_file.endswith('.txt'):
            continue

        found_in_file = False
        with open(os.path.join(SOURCE_LBL_DIR, label_file), 'r') as f:
            for line in f:
                if line.strip().startswith(str(CLASS_ID_TO_FILTER)):
                    found_in_file = True
                    break
        
        if found_in_file:
            basename, _ = os.path.splitext(label_file)
            
            image_filename = ""
            for ext in ['.jpg', '.jpeg', '.png']:
                potential_image_path = os.path.join(SOURCE_IMG_DIR, basename + ext)
                if os.path.exists(potential_image_path):
                    image_filename = basename + ext
                    break
            
            if image_filename:
                shutil.copy2(os.path.join(SOURCE_IMG_DIR, image_filename), target_img_dir)
                shutil.copy2(os.path.join(SOURCE_LBL_DIR, label_file), target_lbl_dir)
                found_count += 1

    print(f"\nSelesai! Berhasil menyalin {found_count} gambar 'no-helmet' ke '{TARGET_DIR}'.")

if __name__ == "__main__":
    filter_and_copy()