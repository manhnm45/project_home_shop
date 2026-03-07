import os
import shutil

# Move all files from one folder to another folder
def move_all_files_to_other_folder(src_folder, dest_folder):
    for folder_name in os.listdir(src_folder):
        folder_path = os.path.join(src_folder, folder_name)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                shutil.move(file_path, dest_folder)
                print(f"Đã chuyển file {file_name} từ {folder_path} đến {dest_folder}")
            except :
                pass

if __name__ == "__main__":
    src_folder = "/home/minhanh/Downloads/project_home/img_sell_obj_backup"
    dest_folder = "/home/minhanh/Documents/object-detection-data-synthesis/objects/object_sell"
    move_all_files_to_other_folder(src_folder, dest_folder)
        