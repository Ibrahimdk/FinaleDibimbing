import os
import random

# --- PENGATURAN ---

# Atur path ke folder gambar dan label Anda
IMAGE_DIR = "image_vest"
LABEL_DIR = "label_vest"

# Persentase data yang ingin Anda simpan (0.20 = 20%)
PERSENTASE_SIMPAN = 0.20

# ------------------

def downsample_dataset():
    """
    Secara acak memilih persentase tertentu dari dataset untuk disimpan,
    dan menghapus sisanya. Sinkron antara gambar dan label.
    """
    print("--- Memulai Proses Pengurangan Dataset ---")
    
    # Validasi folder
    if not os.path.exists(IMAGE_DIR) or not os.path.exists(LABEL_DIR):
        print(f"Error: Pastikan folder '{IMAGE_DIR}' dan '{LABEL_DIR}' ada.")
        return

    # Ambil daftar semua file gambar
    try:
        image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    except FileNotFoundError:
        print(f"Error: Folder gambar '{IMAGE_DIR}' tidak ditemukan.")
        return

    total_files = len(image_files)
    if total_files == 0:
        print("Tidak ada gambar yang ditemukan untuk diproses.")
        return

    # Acak urutan file agar pilihan menjadi random
    random.shuffle(image_files)

    # Hitung berapa banyak file yang akan disimpan dan dihapus
    num_to_keep = int(total_files * PERSENTASE_SIMPAN)
    num_to_delete = total_files - num_to_keep

    # Pisahkan daftar file menjadi yang akan disimpan dan dihapus
    files_to_keep = image_files[:num_to_keep]
    files_to_delete = image_files[num_to_keep:]

    print(f"Total gambar ditemukan: {total_files}")
    print(f"Jumlah yang akan disimpan (20%): {num_to_keep}")
    print(f"Jumlah yang akan dihapus (80%): {num_to_delete}")

    # Hapus file yang tidak diinginkan
    deleted_count = 0
    for filename in files_to_delete:
        basename, _ = os.path.splitext(filename)
        
        image_path = os.path.join(IMAGE_DIR, filename)
        label_path = os.path.join(LABEL_DIR, f"{basename}.txt")

        # Hapus file gambar
        if os.path.exists(image_path):
            os.remove(image_path)
            deleted_count += 1
        
        # Hapus file label yang sesuai
        if os.path.exists(label_path):
            os.remove(label_path)

    print(f"\nProses selesai. Berhasil menghapus {deleted_count} gambar dan label yang sesuai.")
    print("Folder Anda sekarang berisi 20% dari data asli.")


if __name__ == "__main__":
    downsample_dataset()