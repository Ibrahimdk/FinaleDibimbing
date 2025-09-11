import os

# --- PENGATURAN ---
# Pastikan path ini benar
LABELS_DIR = "all_labels"
IMAGES_DIR = "all_images"

# Masukkan ID kelas yang ingin Anda hapus.
# Pastikan ini sesuai dengan file data.yaml Anda!
# 'no-helmet'=1, 'no-vest'=2)
CLASS_IDS_TO_DELETE = [1, 2] 
# ------------------

def remove_classes_from_dataset():
    """
    Menghapus baris yang mengandung ID kelas tertentu dari semua file label.
    Jika file label menjadi kosong, file label dan gambar terkait akan dihapus.
    """
    try:
        label_files = [f for f in os.listdir(LABELS_DIR) if f.endswith('.txt')]
    except FileNotFoundError:
        print(f"Error: Folder '{LABELS_DIR}' tidak ditemukan.")
        return

    print(f"Memindai {len(label_files)} file label untuk menghapus kelas: {CLASS_IDS_TO_DELETE}...")
    
    modified_files = 0
    deleted_files = 0

    for filename in label_files:
        filepath = os.path.join(LABELS_DIR, filename)
        kept_lines = []
        
        with open(filepath, 'r') as f:
            lines = f.readlines()

        for line in lines:
            try:
                class_id = int(line.strip().split()[0])
                if class_id not in CLASS_IDS_TO_DELETE:
                    kept_lines.append(line)
            except (ValueError, IndexError):
                kept_lines.append(line) # Simpan baris yang formatnya salah

        # Jika ada perubahan, tulis ulang file
        if len(kept_lines) != len(lines):
            modified_files += 1
            # Jika file menjadi kosong setelah baris dihapus
            if not kept_lines:
                os.remove(filepath) # Hapus file label
                
                # Cari dan hapus file gambar yang sesuai
                basename, _ = os.path.splitext(filename)
                for ext in ['.jpg', '.jpeg', '.png']:
                    image_path = os.path.join(IMAGES_DIR, basename + ext)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        break
                deleted_files += 1
            else:
                # Tulis ulang file label dengan baris yang tersisa
                with open(filepath, 'w') as f:
                    f.writelines(kept_lines)

    print("\nProses selesai!")
    print(f"Total file label yang diubah: {modified_files}")
    print(f"Total file label (dan gambar) yang kosong dan dihapus: {deleted_files}")

if __name__ == "__main__":
    remove_classes_from_dataset()