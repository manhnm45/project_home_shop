import os
import cv2
import numpy as np
import albumentations as A
# from albumentations.augmentations.dropout import Cutout
# Định nghĩa các augmentations
augmentations = {
    "flip": A.HorizontalFlip(p=1),  # Lật ngang
    "rotate_30": A.Rotate(limit=30, p=1),  # Xoay ±30 độ
    "rotate_45": A.Rotate(limit=45, p=1),  # Xoay ±30 độ
    "rotate_90": A.Rotate(limit=90, p=1),  # Xoay ±30 độ
    "rotate_120": A.Rotate(limit=120, p=1),  # Xoay ±30 độ
    "rotate_180": A.Rotate(limit=180, p=1),  # Xoay ±30 độ
    "brightness": A.RandomBrightnessContrast(p=1),  # Điều chỉnh độ sáng, độ tương phản
    "blur": A.GaussianBlur(blur_limit=(4, 7), p=1),  # Làm mờ ảnh
    "noise": A.GaussNoise(var_limit=(10.0, 50.0), p=1),  # Thêm nhiễu Gaussian
    "cutout_5": A.CoarseDropout(num_holes=5, max_h_size=5, max_w_size=5, p=1),  # Cắt một phần ảnh
    "cutout_3": A.CoarseDropout(num_holes=3, max_h_size=10, max_w_size=10, p=1),  # Cắt một phần ảnh

#     "sharpness": A.Sharpen(alpha=(0.2, 0.5), lightness=(0.5, 1.0), p=1),  # Làm sắc nét
#     "hue": A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=1)  # Điều chỉnh màu sắc
}

def augment_image(image_path):
    # Đọc ảnh
    image = cv2.imread(image_path)
    if image is None:
        print(f"Lỗi: Không thể đọc {image_path}")
        return

    # Lấy tên file và thư mục
    folder, filename = os.path.split(image_path)
    name, ext = os.path.splitext(filename)  # Tách tên file và đuôi mở rộng

    # Áp dụng từng augmentation và lưu file mới
    for aug_name, aug in augmentations.items():
        augmented = aug(image=image)["image"]
        
        # Tạo tên file mới: originalname_augtype.jpg
        new_filename = f"{name}_{aug_name}{ext}"
        new_path = os.path.join(folder, new_filename)

        # Lưu ảnh
        cv2.imwrite(new_path, augmented)
        print(f"Lưu: {new_path}")

# 📌 Thư mục chứa ảnh gốc
data_folder = "/home/minhanh/Downloads/project_home/img_sell_obj"

# Duyệt qua tất cả ảnh trong thư mục và augment
for folder_name in os.listdir(data_folder):
    image_folder = os.path.join(data_folder, folder_name)
    for file in os.listdir(image_folder):
        if file.endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(image_folder, file)
            augment_image(image_path)
