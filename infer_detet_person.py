from ultralytics import YOLO
import cv2
import torch

def load_model(model_path):
    """Load YOLOv8 fine-tuned model using Ultralytics"""
    model = YOLO(model_path)  # Load model fine-tune
    return model

def infer_image(model, image_path):
    """Run inference on an image"""
    results = model(image_path)  # Dự đoán ảnh
    return results

def draw_results(image_path, results):
    """Draw detection results on the image"""
    image = cv2.imread(image_path)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            label = f"Class {cls}: {conf:.2f}"

            # Vẽ bounding box và label
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow("Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    
    model_path = "/home/minhanh/Downloads/project_home/runs/detect/train5/weights/best.pt"  # Đường dẫn model fine-tuned
    image_path = "/home/minhanh/Downloads/project_home/yu_masks_jpg.rf.b400f0a2d69db94aeba591b1e6bf955e.jpg"  # Đường dẫn ảnh

    model = load_model(model_path)
    results = infer_image(model, image_path)
    draw_results(image_path, results)

if __name__ == "__main__":
    
    main()
