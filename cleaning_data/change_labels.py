import os

# --- PENGATURAN ---
# Folder yang berisi semua file label .txt Anda
LABELS_DIR = "label_vest"

# Definisikan pemetaan dari ID lama ke ID baru
# Format: {id_lama: id_baru}
ID_MAPPING = {
    0: 2  # Mengubah  dari ID 0 ke 2
}
# ------------------

def update_class_ids():
    """
    Memperbarui ID kelas di semua file label sesuai dengan ID_MAPPING.
    """
    try:
        label_files = [f for f in os.listdir(LABELS_DIR) if f.endswith('.txt')]
    except FileNotFoundError:
        print(f"Error: Folder '{LABELS_DIR}' tidak ditemukan.")
        return

    print(f"Memulai pembaruan ID kelas untuk {len(label_files)} file di '{LABELS_DIR}'...")
    updated_count = 0

    for filename in label_files:
        filepath = os.path.join(LABELS_DIR, filename)
        new_content = []
        was_updated = False
        
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            try:
                parts = line.strip().split()
                old_id = int(parts[0])
                
                # Cek jika ID lama ada di dalam mapping kita
                if old_id in ID_MAPPING:
                    new_id = ID_MAPPING[old_id]
                    parts[0] = str(new_id)
                    new_content.append(" ".join(parts) + "\n")
                    was_updated = True
                else:
                    new_content.append(line) # Simpan baris seperti adanya
            except (ValueError, IndexError):
                new_content.append(line)
        
        # Tulis ulang file jika ada perubahan
        if was_updated:
            with open(filepath, 'w') as f:
                f.writelines(new_content)
            updated_count += 1
            
    print(f"\nSelesai! {updated_count} file telah diperbarui dengan ID kelas yang baru.")

if __name__ == "__main__":
    update_class_ids()