import os
import shutil

# --- PENGATURAN ---
# Tentukan path sumber secara terpisah
SOURCE_IMG_DIR = "all_images"
SOURCE_LBL_DIR = "all_labels"

# Folder tujuan untuk menampung data yang difilter
TARGET_DIR = "augment_vest_temp"

# ID Kelas untuk 'vest'
CLASS_ID_TO_FILTER = 2
# ------------------

def filter_and_copy():
    """Menemukan dan menyalin semua gambar yang mengandung ID kelas tertentu."""
    target_img_dir = os.path.join(TARGET_DIR, "images")
    target_lbl_dir = os.path.join(TARGET_DIR, "labels")

    os.makedirs(target_img_dir, exist_ok=True)
    os.makedirs(target_lbl_dir, exist_ok=True)

    try:
        # Langsung baca dari SOURCE_LBL_DIR
        label_files = [f for f in os.listdir(SOURCE_LBL_DIR) if f.endswith('.txt')]
    except FileNotFoundError:
        print(f"Error: Folder sumber '{SOURCE_LBL_DIR}' tidak ditemukan.")
        return

    print(f"Memindai {len(label_files)} file label untuk kelas ID: {CLASS_ID_TO_FILTER}...")
    
    found_count = 0
    for label_file in label_files:
        found_in_file = False
        # Buka file label dari path sumber yang benar
        with open(os.path.join(SOURCE_LBL_DIR, label_file), 'r') as f:
            for line in f:
                if line.strip().startswith(str(CLASS_ID_TO_FILTER)):
                    found_in_file = True
                    break
        
        if found_in_file:
            basename, _ = os.path.splitext(label_file)
            
            image_filename = ""
            for ext in ['.jpg', '.jpeg', '.png']:
                # Cari file gambar di SOURCE_IMG_DIR
                potential_image_path = os.path.join(SOURCE_IMG_DIR, basename + ext)
                if os.path.exists(potential_image_path):
                    image_filename = basename + ext
                    break
            
            if image_filename:
                # Salin dari path sumber yang benar ke path tujuan
                shutil.copy2(os.path.join(SOURCE_IMG_DIR, image_filename), target_img_dir)
                shutil.copy2(os.path.join(SOURCE_LBL_DIR, label_file), target_lbl_dir)
                found_count += 1

    print(f"\nSelesai! Berhasil menyalin {found_count} gambar 'vest' ke '{TARGET_DIR}'.")

if __name__ == "__main__":
    filter_and_copy()