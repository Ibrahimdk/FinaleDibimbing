import os

# --- PENGATURAN ---
# Atur path ke folder yang berisi semua file label .txt Anda
LABELS_DIR = "all_labels" 
# ------------------

def fix_label_files():
    """
    Membaca semua file .txt di direktori, mengubah ID kelas dari desimal
    menjadi angka bulat, dan menulis ulang filenya.
    """
    try:
        label_files = [f for f in os.listdir(LABELS_DIR) if f.endswith('.txt')]
    except FileNotFoundError:
        print(f"Error: Folder '{LABELS_DIR}' tidak ditemukan.")
        return

    print(f"Memulai perbaikan untuk {len(label_files)} file di '{LABELS_DIR}'...")
    fixed_count = 0

    for filename in label_files:
        filepath = os.path.join(LABELS_DIR, filename)
        needs_fixing = False
        new_content = []

        with open(filepath, 'r') as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue # Lewati baris kosong

            class_id_str = parts[0]
            # Cek jika ada titik desimal di ID kelas
            if '.' in class_id_str:
                needs_fixing = True
                # Ubah '4.0' -> 4.0 -> 4 -> '4'
                class_id_int = int(float(class_id_str)) 
                parts[0] = str(class_id_int)
                new_content.append(" ".join(parts) + "\n")
            else:
                new_content.append(line)

        # Jika ada perubahan, tulis ulang file tersebut
        if needs_fixing:
            with open(filepath, 'w') as f:
                f.writelines(new_content)
            fixed_count += 1

    print(f"\nSelesai! {fixed_count} file telah ditemukan dan diperbaiki.")

if __name__ == "__main__":
    fix_label_files()