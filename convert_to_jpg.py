import os
from PIL import Image

# Thư mục chứa ảnh
data_folder = "/home/minhanh/Downloads/project_home/img_sell_obj"
for folder_name in os.listdir(data_folder):
    image_folder = os.path.join(data_folder, folder_name)
    # Duyệt qua tất cả các file trong thư mục
    for file in os.listdir(image_folder):
        # Kiểm tra nếu file là ảnh cần chuyển đổi
        if file.lower().endswith((".jpeg", ".png", ".webp",".jpg")):
            # Đường dẫn ảnh gốc
            old_path = os.path.join(image_folder, file)

            # Lấy tên file (không có đuôi mở rộng)
            name, _ = os.path.splitext(file)

            # Đường dẫn mới với đuôi ".jpg"
            new_path = os.path.join(image_folder, f"{name}.jpg")

            # Mở ảnh và chuyển đổi sang định dạng JPG
            try:
                image = Image.open(old_path).convert("RGB")
                os.remove(old_path)  # Chuyển sang RGB để đảm bảo không bị lỗi khi lưu JPG
                image.save(new_path, "JPEG", quality=95)  # Lưu ảnh dưới dạng JPG
                print(f"Chuyển đổi: {file} ➝ {name}.jpg")

            except:
                os.remove(old_path)
                print(f"remove path {old_path}")

