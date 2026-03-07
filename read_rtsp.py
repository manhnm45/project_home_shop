import cv2
import os
from ultralytics import YOLO
import time
import pika
import json
import rabbitmq
import yaml
import numpy as np
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

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config

config = load_config()
rabbitmq_host = config["rabbimq_host"]
rabbitmq_port = config["rabbimq_port"]
rabbitmq_username = config["rabbimq_username"]
rabbitmq_password = config["rabbimq_password"]
exchange = config["exchange"]
vitualhost = config["vitualhost"]

rabbitmq = rabbitmq.RabbitmqClient(rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password, vitualhost)
rabbitmq.connect()
queue_name = "read_rtsp"
if __name__ == "__main__":
    channel = rabbitmq.init_queue(queue_name=queue_name, durable=True)
    model = YOLO('./train_results_obb3/train/weights/best.pt')
    path_rtsp = "./video_product_sell/487976405_24243682478565205_842528384009456328_n.mp4"
    cap = cv2.VideoCapture(path_rtsp)
    skip_frame = 0
    frame_count = 0
    while True:
        confident_push = []
        image_path_push= []
        time_stamp_push = []
        xyxyxyxy_push = []
        ret, frame = cap.read()
        frame_count += 1
        if not ret:
            print("Failed to grab frame")
            break
        if frame_count % (skip_frame + 1) != 0:
            continue
        
        results = model(frame, conf=0.5, save=False, device='cpu')
        if len(results)!=0:
            for result in results:
                conf = result.obb.conf.detach().cpu().numpy()
                xyxyxyxy = result.obb.xyxyxyxy.detach().cpu().numpy()
                print("len xyxyxy",result.obb.conf)

                print("xyxyxyxy", xyxyxyxy)
                for i in range(len(conf)):
                    if conf[i]>0.8:
                        time_stamp = time.time()
                        confident_push.append(float(conf[i]))
                        image_alige = align_obbox(frame, xyxyxyxy[i])
                        frame_save_name = f"image_object_{int(time_stamp*100000)}_{i}.jpg"
                        image_crop_path = os.path.join("./web_sell/media/product_search/", frame_save_name)
                        image_path_push.append(image_crop_path)
                        cv2.imwrite(image_crop_path, image_alige)
                        time_stamp_push.append(time_stamp*100000)
                        xyxyxyxy_push.append(xyxyxyxy[i].tolist())
                detected_obj = {
                    'confidence': confident_push,
                    'image_path': image_path_push,
                    'timestamp': time_stamp_push,
                    'xyxyxyxy': xyxyxyxy_push 
                }
                rabbitmq.publish_message(channel, queue_name, detected_obj, priority=5)
                print(f"Published: {detected_obj}")
            
    






