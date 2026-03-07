import os
import shutil

folder_dataset = "/home/minhanh/Downloads/project_home/datasest_lantam_shop"
folder_datalake = "/home/minhanh/Downloads/project_home/data_lake"
os.makedirs(folder_datalake, exist_ok=True)

for object_folder in os.listdir(folder_dataset):
    if os.path.isdir(os.path.join(folder_dataset, object_folder)):
        object_folder_path = os.path.join(folder_dataset, object_folder)
        for image_file in os.listdir(object_folder_path):
            if image_file.endswith(".jpg") or image_file.endswith(".png"):
                source_path = os.path.join(object_folder_path, image_file)
                # destination_path = os.path.join("data_lake", image_file)
                shutil.copy(source_path, folder_datalake)