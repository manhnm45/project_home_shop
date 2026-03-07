
from ultralytics import YOLO

model = YOLO("/home/minhanh/Downloads/project_home/train8_detect_sell_obj/weights/best.pt")  # đổi sang yolov8s, m, l tùy
model.export(
    format="onnx",         # Định dạng xuất
    imgsz=640,             # Kích thước ảnh (640x640)
    opset=12,              # Đảm bảo ONNX opset >= 12
    dynamic=False,         # False = input cố định
    simplify=True          # Tối ưu ONNX bằng onnx-simplifier
)
