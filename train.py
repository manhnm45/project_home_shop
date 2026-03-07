import ultralytics 
from ultralytics import YOLO

# Load model YOLOv8m pre-trained
model = YOLO("yolov8s.pt")

# Train model
results = model.train(
    data="/home/minhanh/Downloads/project_home/data_lantamshop.yaml",
    epochs=50,  # Số vòng lặp huấn luyện
    batch=2,  # Số batch (có thể giảm nếu bị lỗi thiếu VRAM)
    imgsz=224,  # Kích thước ản
    workers=2,  # Số luồng xử lý dữ liệu
)