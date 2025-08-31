import os
from collections import defaultdict

# --- UBAH DUA BARIS DI BAWAH INI ---
LABEL_DIR = "split_dataset/train/labels" 
CLASS_NAMES = ['helmet', 'no-helmet', 'no-vest', 'person', 'vest']
# -----------------------------------

def quick_check():
    """Hanya menghitung dan menampilkan jumlah objek per kelas di terminal."""
    
    class_counts = defaultdict(int)
    
    try:
        # Mengambil semua file .txt di dalam direktori
        label_files = [f for f in os.listdir(LABEL_DIR) if f.endswith('.txt')]
    except FileNotFoundError:
        print(f"Error: Folder '{LABEL_DIR}' tidak ditemukan. Silakan periksa path Anda.")
        return

    # Menghitung setiap class_id dari semua file
    for filename in label_files:
        with open(os.path.join(LABEL_DIR, filename), 'r') as f:
            for line in f:
                class_id = int(line.split()[0])
                class_counts[class_id] += 1
    
    # Menampilkan hasil
    print(f"\n--- Hasil Pengecekan di Folder: {LABEL_DIR} ---")
    for class_id, count in sorted(class_counts.items()):
        class_name = CLASS_NAMES[class_id]
        print(f"  - {class_name:<15} (ID: {class_id}): {count} objek")
    
    print("-" * 45)
    print(f"  - Total Objek Ditemukan: {sum(class_counts.values())}\n")

if __name__ == "__main__":
    quick_check()