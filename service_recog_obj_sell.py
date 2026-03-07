import cv2
import numpy as np
from ultralytics import YOLO
import os
import infer_classify_objsell
import time
import torch
import json
import requests
device = "cuda" if torch.cuda.is_available() else "cpu"

def send_to_django(label):
    url = "http://127.0.0.1:8000/upload_item/"  # Đổi sang URL backend của bạn
    data = {"name": label}
    data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    
    print("Đang gửi:", data)
    
    response = requests.post(url,data=data,headers=headers)
    print("response", response)
    if response.status_code == 200:
        print("Đã gửi:", response.json())
    else:
        print("Gửi thất bại:", response.status_code)
    
    

def sort_by_area(boxes):
    """Sort bounding boxes by area in descending order."""
    areas = [(box[2] - box[0]) * (box[3] - box[1]) for box in boxes]
    sorted_indices = np.argsort(areas)[::-1]  # Sort indices in descending order
    return [boxes[i] for i in sorted_indices]


def infer_model_detect_obj_sell(model_path, image):
    """Load YOLOv8 model and run inference on the image."""
    model = YOLO(model_path).to(device)  # Load the YOLOv8 model
    results = model(image, device=device)  # Run inference
    boxes = results[0].boxes  # Get the bounding boxes
    if len(boxes) > 1:
        boxes = boxes.cpu().numpy()
        try:
            box_bigest = sort_by_area(boxes)[0]
        except:
            return None
    elif len(boxes) == 1:
        box_bigest = boxes.cpu().numpy()[0]
    else:
        box_bigest = None
    if box_bigest is None:
        return None
    else:
        x1, y1, x2, y2 = map(int, box_bigest.xyxy[0])
        conf = box_bigest.conf[0].item()
        return x1, y1, x2, y2, conf

def main():
    rtsp = "/home/minhanh/Downloads/project_home/video_product_sell/488697878_29019590631022696_1354965986106958032_n.mp4"
    # model_detect_path = "/home/minhanh/Downloads/project_home/train8_detect_sell_obj/weights/best.pt"
    model_detect_path = "/home/minhanh/Downloads/project_home/runs/detect/train7/weights/best.pt"
    model_classify_path = "/home/minhanh/Downloads/project_home/best_model49.pth"
    CLASSES = ['namngudenhi', 'haohao_box', 'brash_teeth', 'omachi_box', 'bimbimkhoaitayoka', 'haohao', 'botchiengion', 'thuoclathanglong', 'omachi', 'namngucahoi', 'kemdanhrangcloseup', 'cocacolalon_big_size', 'banhgaomatongichi', 'biaheineken', 'botchiengionmeizan', 'ruataylifebouy', 'bohucredbul', 'botgiatomo3kg', 'thuoclabaso555', 'botgiatomo350g', 'kokomi_box', 'kokomi', 'kemdanhrangps', 'banhtrungcusta', 'nuocruabatsunlight', 'namngu', 'botgiatomo5kg', 'bia333', 'suathtruemilk_bigsize', 'suamilo_bigsize', 'michinh', 'suamilo_smallsize', 'batlua', 'vicocacola']
    cap = cv2.VideoCapture(rtsp,cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    frame_count = 0
    while True:
        time__infer = time.time()
        skip_frame = 5
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break
        frame_count += 1
        if frame_count % skip_frame != 0:
            continue
        try:
            time_detect = time.time()
            frame = cv2.resize(frame, (640, 640))
            height , width, _ = frame.shape
            x1, y1, x2, y2, conf = infer_model_detect_obj_sell(model_detect_path, frame)
            # print("shape", height, width)
            # print("detected box:", x1, y1, x2, y2)
            if x1> int(width*0.1) and x2 < int(width*0.9) and y1 > int(height*0.1) and y2 < int(height*0.9):
                print("time detect: ", time.time() - time_detect)
                img_crop = frame[y1:y2, x1:x2]
                
                time_classify= time.time()
                product_name = infer_classify_objsell.infer_image(model_classify_path, img_crop,CLASSES, device = device)
                print("time classify: ", time.time() - time_classify)
                cv2.imwrite(f"result_infer_detect/img_crop_{product_name}.jpg", img_crop)
                send_to_django(product_name)
                # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # cv2.putText(frame, product_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        except Exception as e:
            print("Error",e)
            continue
        print("time infer: ", time.time() - time__infer)
            
        # cv2.imshow("qObject Detection", frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Torch version:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    print("CUDA devices:", torch.cuda.device_count())
    if torch.cuda.is_available():
        print("GPU Name:", torch.cuda.get_device_name(0))
    main()