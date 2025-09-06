import os
import cv2
import albumentations as A
import shutil

# --- PENGATURAN ---
SOURCE_DIR = "augment_temp"
TARGET_IMG_DIR = "all_images"
TARGET_LBL_DIR = "all_labels"
NUM_COPIES_PER_IMAGE = 10
# ------------------

transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.GaussianBlur(p=0.2),
    A.Rotate(limit=15, p=0.5),
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

def augment_to_main_folder():
    source_img_dir = os.path.join(SOURCE_DIR, "images")
    source_lbl_dir = os.path.join(SOURCE_DIR, "labels")

    os.makedirs(TARGET_IMG_DIR, exist_ok=True)
    os.makedirs(TARGET_LBL_DIR, exist_ok=True)

    image_files = [f for f in os.listdir(source_img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"Meng-augmentasi {len(image_files)} gambar 'no-helmet'...")

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
            
            aug_filename = f"{basename}_aug_nh_{i}{ext}"
            aug_labelname = f"{basename}_aug_nh_{i}.txt"
            
            cv2.imwrite(os.path.join(TARGET_IMG_DIR, aug_filename), cv2.cvtColor(augmented['image'], cv2.COLOR_RGB2BGR))
            
            with open(os.path.join(TARGET_LBL_DIR, aug_labelname), 'w') as f:
                for j, bbox in enumerate(augmented['bboxes']):
                    class_id = augmented['class_labels'][j]
                    f.write(f"{class_id} {' '.join(map(str, bbox))}\n")

    print(f"\nSelesai! Data augmentasi baru telah ditambahkan ke 'all_images' dan 'all_labels'.")

if __name__ == "__main__":
    try:
        import albumentations
    except ImportError:
        print("Menginstall library... pip install albumentations opencv-python")
        os.system("pip install albumentations opencv-python")
    
    augment_to_main_folder()