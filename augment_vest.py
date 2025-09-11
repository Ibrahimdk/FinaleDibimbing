import os
import cv2
import albumentations as A

# --- PENGATURAN ---
SOURCE_DIR = "augment_vest_temp"      # Ambil dari folder sementara
TARGET_IMG_DIR = "all_images"         # <--- UBAH INI
TARGET_LBL_DIR = "all_labels"         # <--- UBAH INI
NUM_COPIES_PER_IMAGE = 1              # Buat 1 salinan augmentasi
# ------------------

# Definisikan pipeline augmentasi
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.GaussianBlur(p=0.2),
    A.Rotate(limit=15, p=0.5),
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))


def augment_and_add():
    """Membuat salinan augmentasi dan menambahkannya ke folder all_images dan all_labels."""
    source_img_dir = os.path.join(SOURCE_DIR, "images")
    source_lbl_dir = os.path.join(SOURCE_DIR, "labels")
    

    # Pastikan folder target ada
    os.makedirs(TARGET_IMG_DIR, exist_ok=True)
    os.makedirs(TARGET_LBL_DIR, exist_ok=True)
    
    try:
        image_files = [f for f in os.listdir(source_img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    except FileNotFoundError:
        print(f"Error: Folder sumber '{source_img_dir}' tidak ditemukan.")
        return

    print(f"Membuat {NUM_COPIES_PER_IMAGE} salinan augmentasi dari {len(image_files)} gambar...")

    for filename in image_files:
        basename, ext = os.path.splitext(filename)
        
        image = cv2.imread(os.path.join(source_img_dir, filename))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        bboxes, class_labels = [], []
        with open(os.path.join(source_lbl_dir, f"{basename}.txt"), 'r') as f:
            for line in f:
                parts = line.strip().split()
                class_labels.append(int(parts[0]))
                bboxes.append([float(x) for x in parts[1:]])

        for i in range(NUM_COPIES_PER_IMAGE):
            augmented = transform(image=image, bboxes=bboxes, class_labels=class_labels)
            
            aug_filename = f"{basename}_aug_vest_{i}{ext}"
            aug_labelname = f"{basename}_aug_vest_{i}.txt"
            
            # --- UBAH DUA BARIS INI ---
            # Simpan gambar dan label baru langsung ke folder target
            cv2.imwrite(os.path.join(TARGET_IMG_DIR, aug_filename), cv2.cvtColor(augmented['image'], cv2.COLOR_RGB2BGR))
            
            with open(os.path.join(TARGET_LBL_DIR, aug_labelname), 'w') as f:
                for j, bbox in enumerate(augmented['bboxes']):
                    class_id = augmented['class_labels'][j]
                    f.write(f"{class_id} {' '.join(map(str, bbox))}\n")

    print(f"\nSelesai! Data augmentasi telah ditambahkan ke '{TARGET_IMG_DIR}' dan '{TARGET_LBL_DIR}'.")


if __name__ == "__main__":
    try:
        import albumentations
    except ImportError:
        print("Menginstall library: albumentations, opencv-python")
        os.system("pip install albumentations opencv-python")
    
    augment_and_add()