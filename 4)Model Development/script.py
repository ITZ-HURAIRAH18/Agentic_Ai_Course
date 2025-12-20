import os
import shutil
import random

base_dir = "PetImages"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "validation")

classes = ["Cat", "Dog"]
val_ratio = 0.2  # 20% validation

for cls in classes:
    src_dir = os.path.join(base_dir, cls)

    images = [img for img in os.listdir(src_dir)
              if img.lower().endswith(('.jpg', '.png', '.jpeg'))]

    random.shuffle(images)

    val_size = int(len(images) * val_ratio)

    val_images = images[:val_size]
    train_images = images[val_size:]

    # Create directories
    os.makedirs(os.path.join(train_dir, cls), exist_ok=True)
    os.makedirs(os.path.join(val_dir, cls), exist_ok=True)

    # Move training images (80%)
    for img in train_images:
        shutil.move(
            os.path.join(src_dir, img),
            os.path.join(train_dir, cls, img)
        )

    # Move validation images (20%)
    for img in val_images:
        shutil.move(
            os.path.join(src_dir, img),
            os.path.join(val_dir, cls, img)
        )

    print(f"{cls}: {len(train_images)} train | {len(val_images)} validation")

print("✅ Dataset split completed successfully!")
