from ultralytics import YOLO
import cv2
import torch
import os
import numpy as np
model_path = "/home/minhanh/Downloads/project_home/train_results_obb3/train/weights/best.pt"
model = YOLO(model_path)
def align_obbox(image, xyxyxyxy, output_size=(224, 224)):
    # Đảm bảo là numpy array float32
    pts = np.array(xyxyxyxy, dtype=np.float32).reshape(4, 2)

    # Kích thước đầu ra
    w, h = output_size

    # 4 điểm đích (theo thứ tự tương ứng với pts)
    dst_pts = np.array([
        [0, 0],
        [w - 1, 0],
        [w - 1, h - 1],
        [0, h - 1]
    ], dtype=np.float32)

    # Tính ma trận biến đổi perspective
    M = cv2.getPerspectiveTransform(pts, dst_pts)

    # Warp ảnh về khung chuẩn
    aligned_img = cv2.warpPerspective(image, M, (w, h))

    return aligned_img
folder_image =  "/home/minhanh/Downloads/project_home/data_lake"
folder_save_result = "/home/minhanh/Downloads/project_home/folder_image_crop_alige"
os.makedirs(folder_save_result, exist_ok=True)
for image_name in os.listdir(folder_image):
    image_path = os.path.join(folder_image, image_name)
    results = model(image_path)
    for result in results:
        conf = float(result.obb.conf[0])
        xyxyxyxy = result.obb.xyxyxyxy.detach().cpu().numpy()
        if conf>0.8:
            image = cv2.imread(image_path)
            image_alige = align_obbox(image, xyxyxyxy)
            image_path_save = os.path.join(folder_save_result, image_name)
            cv2.imwrite(image_path_save,image_alige)



# image_path = "/home/minhanh/Downloads/project_home/data_lake/IMG_20250430_171448.jpg"
# results =  model(image_path)
# print(len(results))
# for result in results:
    
#     conf = result.obb.conf
#     print("conf",float(conf[0]))
#     xyxyxyxy= result.obb.xyxyxyxy.detach().cpu().numpy()
# image = cv2.imread(image_path)
# image_alige = align_obbox(image, xyxyxyxy)
# cv2.imwrite("image_alige.jpg",image_alige)
