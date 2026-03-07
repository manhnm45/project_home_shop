import cv2
import os
import time
import pika
import json
import yaml
import numpy as np
import torch
import rabbitmq
import build_index
from get_embeding_model import EmbeddingModel

import get_infor_from_sql


# device = "cuda" if cv2.cuda.getCudaEnabledDeviceCount() > 0 else "cpu"
# model = EmbeddingModel(model_name='resnet50', pretrained=False, embedding_size=1024, device=device)
# model.load_state_dict(torch.load("/project_home/resnet50_embedding_model.pt", map_location=device))
Roi = [100, 200, 400, 800]  # Example ROI coordinates [x1, y1, x2, y2]
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

def callback_func(body):
    global continous_product,sended_message, queue_push, channel_push
    confidence = body.get("confidence", [])
    image_paths = body.get("image_path", [])
    timestamps = body.get("timestamp", [])
    xyxyxyxy = body.get("xyxyxyxy", [])
    print("Received message")
    Getinfo_from_sql = get_infor_from_sql.Getinfo_from_sql(user_name="postgres", password="1", host="localhost", port="5432", db_name="postgres")

    if len(xyxyxyxy)>0:
        # print("Processing xyxyxyxy:", xyxyxyxy)
        # print("Processing confidence:", confidence)
        # xyxyxyxy = xyxyxyxy[0]
        for idx in range(len(confidence)):
            # print("Processing xyxyxyxy index:", xyxyxyxy[idx])
            x_list = [x for [x,y] in xyxyxyxy[idx]]
            y_list = [y for [x,y] in xyxyxyxy[idx]]
            x_object_min = min(x_list)
            x_object_max = max(x_list)
            y_object_min = min(y_list)
            y_object_max = max(y_list)
            if x_object_min> Roi[0] and x_object_max<Roi[2] and y_object_min>Roi[1] and y_object_max<Roi[3]:
                # print("x list", x_list)
                # print("x_object_min",x_object_min)
                image_path = image_paths[idx]
                image = cv2.imread(image_path)
                image_copy = image.copy()
                # image_crop = align_obbox(image_copy, xyxyxyxy[idx])
                # image_crop = align_obbox(image, xyxyxyxy[idx])
                # Further processing with image_crop
                
                #search image
                search_faiss = build_index.Searchfaiss(folder_image_build_index = "./folder_data_search_image_relative_product_name", folder_path_mat="./mat_file_save_with_model_embedding_clips_relative_avatar", path_index = "faiss_index_clip_relative_avatar.index", label_file="index.json")
                top_file_name = search_faiss.search_image(image_copy)
                print("Top matching file:", top_file_name)
                if len(continous_product) == 0:
                    continous_product.append(top_file_name)
                else:
                    if continous_product[-1] != top_file_name:
                        continous_product = []
                        continous_product.append(top_file_name)
                        sended_message = False
                    else:
                        continous_product.append(top_file_name)
                        if len(continous_product) >= 3 and sended_message == False:
                            # Get product cost
                            product_cost = 0
                            try:
                                # product_obj = Product.objects.get(name=top_file_name)
                                product_cost = Getinfo_from_sql.get_cost_product(top_file_name[0], table_name="users")
                                print(f"Product cost for {top_file_name}: {product_cost}")  

                            except Exception as e:
                                print(f"Error getting product cost for {top_file_name}: {e}")

                            #send message to rabbitmq
                            message_send = {
                                "image_path": image_path,
                                "timestamp": timestamps[idx],
                                "product_id": top_file_name,
                                "cost": product_cost
                            }
                            print("Preparing to send alert message:", message_send)
                            rabbitmq.publish_message(channel_push, queue_push, message_send, priority=5)
                            print("Sent alert message:", message_send)
                            sended_message = True
                        else:
                            print("Continous product count:", len(continous_product))


            # image = cv2.imread(image_path)

if __name__ == "__main__":
    continous_product = []
    sended_message = False
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    rabbitmq_host = config["rabbimq_host"]
    rabbitmq_port = config["rabbimq_port"]
    rabbitmq_username = config["rabbimq_username"]
    rabbitmq_password = config["rabbimq_password"]
    exchange = config["exchange"]
    vitualhost = config["vitualhost"]
    rabbitmq = rabbitmq.RabbitmqClient(rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password, vitualhost)        
    rabbitmq.connect()
    queue_name_get = "read_rtsp"
    queue_push = "update_userui"
    channel = rabbitmq.init_queue(queue_name=queue_name_get, durable=True)
    channel_push = rabbitmq.init_queue(queue_name=queue_push, durable=True)
    rabbitmq.run_consummer(channel, queue_name_get, callback_func)

    