import os
import shutil
import random
data_folder_path = "/home/minhanh/Downloads/project_home/img_sell_obj"
data_folder_dict = "/home/minhanh/Downloads/project_home/valid_data"
for folder_name in os.listdir(data_folder_path):
    print("folder_name",folder_name)
    folder_img = os.path.join(data_folder_path,folder_name)
    folder_dict = os.path.join(data_folder_dict,folder_name)
    os.makedirs(folder_dict, exist_ok=True)

    images = [f for f in os.listdir(folder_img) if os.path.isfile(os.path.join(folder_img, f))]

        # Chọn ngẫu nhiên 1/8 số ảnh
    num_valid = max(1, len(images) // 8)
    valid_images = random.sample(images, num_valid)

    # Di chuyển ảnh sang thư mục valid tương ứng
    for img in valid_images:
        src = os.path.join(folder_img, img)
        dst = os.path.join(folder_dict, img)
        shutil.move(src, dst)

