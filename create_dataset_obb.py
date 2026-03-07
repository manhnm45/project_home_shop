import os
import shutil


folder_dataset_path = '/home/minhanh/Downloads/project_home/obb_datalake'  # Replace with your folder path
folder_labels = os.path.join(folder_dataset_path, 'labels')
folder_images = os.path.join(folder_dataset_path, 'images')
folder_image_lake = "/home/minhanh/Downloads/project_home/data_lake"
os.makedirs(folder_labels, exist_ok=True)
os.makedirs(folder_images, exist_ok=True)
for folder_name in os.listdir(folder_labels):
    folder_path = os.path.join(folder_labels, folder_name)
    folder_child_image = os.path.join(folder_images, folder_name)
    os.makedirs(folder_child_image, exist_ok=True)
    for label_file in os.listdir(folder_path):
        imge_name = label_file.split('.')[0] + '.jpg'
        image_path = os.path.join(folder_image_lake, imge_name)
        shutil.copy(image_path, folder_child_image)