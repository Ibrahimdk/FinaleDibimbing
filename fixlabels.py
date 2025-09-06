import os

# --- PENGATURAN ---
# Ubah variabel ini menjadi sebuah list berisi semua path folder label Anda
LABEL_DIRS = [
    "all_labels",
    "path/lain/ke/labels",
    "dan/seterusnya"
] 
# ------------------

def fix_label_files_in_multiple_dirs():
    """
    Menjalankan perbaikan file label untuk setiap direktori yang ada di dalam list LABEL_DIRS.
    """
    total_fixed_count = 0
    
    # Loop melalui setiap path folder yang ada di dalam list
    for labels_dir in LABEL_DIRS:
        try:
            label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
        except FileNotFoundError:
            print(f"\nWarning: Folder '{labels_dir}' tidak ditemukan. Melewati...")
            continue
        
        print(f"\nMemulai perbaikan untuk {len(label_files)} file di '{labels_dir}'...")
        fixed_count_in_dir = 0
        
        for filename in label_files:
            filepath = os.path.join(labels_dir, filename)
            needs_fixing = False
            new_content = []

            with open(filepath, 'r') as f:
                lines = f.readlines()

            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue
                
                class_id_str = parts[0]
                if '.' in class_id_str:
                    needs_fixing = True
                    class_id_int = int(float(class_id_str)) 
                    parts[0] = str(class_id_int)
                    new_content.append(" ".join(parts) + "\n")
                else:
                    new_content.append(line)
            
            if needs_fixing:
                with open(filepath, 'w') as f:
                    f.writelines(new_content)
                fixed_count_in_dir += 1

        print(f"  -> Selesai! {fixed_count_in_dir} file telah diperbaiki di folder ini.")
        total_fixed_count += fixed_count_in_dir
    
    print(f"\n==================================================")
    print(f"Proses Selesai Total! {total_fixed_count} file telah diperbaiki dari semua direktori.")

if __name__ == "__main__":
    fix_label_files_in_multiple_dirs()