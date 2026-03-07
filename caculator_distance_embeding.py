import torch
import clip
from PIL import Image
import torchvision.transforms as transforms
import torch.nn.functional as F

# Load model và thiết bị (CPU hoặc GPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Hàm trích xuất đặc trưng của ảnh
def extract_features(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)  # chuẩn hóa
    return image_features

# Hàm tính cosine similarity giữa 2 tensor
def cosine_similarity(tensor1, tensor2):
    return F.cosine_similarity(tensor1, tensor2).item()

# Đường dẫn ảnh
image_path1 = "/home/minhanh/Downloads/project_home/image_smallmillo.png"
image_path2 = "/home/minhanh/Downloads/project_home/datasest_lantam_shop/sua_milo_vi_4hop_180ml/IMG_20250501_092319.jpg"

# Trích xuất đặc trưng
features1 = extract_features(image_path1)
features2 = extract_features(image_path2)

# Tính độ tương đồng cosine
similarity = cosine_similarity(features1, features2)

print(f"Cosine Similarity: {similarity:.4f}")
