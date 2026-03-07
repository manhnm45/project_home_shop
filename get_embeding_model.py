import timm
import torch
import torch.nn as nn
import cv2
import numpy as np
from torchvision import transforms
from PIL import Image
import os
import open_clip


class EmbeddingModel(nn.Module):
    def __init__(self, model_name='resnet50', pretrained=True, embedding_size=1024, device='cpu'):
        super(EmbeddingModel, self).__init__()
        self.device = device

        # Load pretrained backbone
        self.model = timm.create_model(model_name, pretrained=pretrained)
        
        # Lấy số feature đầu ra
        in_features = self.model.get_classifier().in_features

        # Bỏ layer classifier gốc
        self.model.reset_classifier(0)

        # Thêm layer embedding
        self.embedding_layer = nn.Linear(in_features, embedding_size)

        # Đưa model lên device
        self.to(self.device)

    def preprocess(self, image):
        """Chuyển ảnh BGR (cv2) -> tensor normalized cho model"""
        image = cv2.resize(image, (224, 224))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype(np.float32) / 255.0
        image = (image - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
        image = image.transpose(2, 0, 1)  # HWC → CHW
        tensor = torch.tensor(image, dtype=torch.float32).unsqueeze(0).to(self.device)
        return tensor

    @torch.no_grad()
    def get_embedding(self, image):
        """Trả về vector embedding 1D"""
        x = self.preprocess(image)
        features = self.model.forward_features(x)
        features = features.mean(dim=[2, 3])   # Global Average Pooling
        embedding = self.embedding_layer(features)
        embedding = nn.functional.normalize(embedding, p=2, dim=1)  # Chuẩn hóa vector (optional)
        return embedding.squeeze(0).cpu().numpy()  # chuyển về numpy để build FAISS index

# -------------------------------

class DinoEmbeddingModel(nn.Module):
    def __init__(self, pretrained=True, device='cpu'):
        super(DinoEmbeddingModel, self).__init__()
        self.model = timm.create_model("vit_large_patch14_dinov2.lvd142m", pretrained=pretrained)
        self.model.eval()
        # DINOv2 trả ra embedding 1024 hoặc 1536 tùy model
        embed_dim = self.model.num_features
        self.transform = transforms.Compose([
            transforms.Resize((518,518), interpolation=transforms.InterpolationMode.BICUBIC),
            # transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
            ])


    @torch.no_grad()
    def get_embedding(self, image):
        # img = Image.open(img_path).convert("RGB")
        img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        x = self.transform(img).unsqueeze(0)  # shape: [1, 3, 224, 224]

        # Forward để lấy embedding
        feat = self.model.forward_features(x)  # tensor [1, tokens, dim]

        # Lấy CLS token
        emb = feat[:, 0]  # shape [1, D]

        # Normalize
        emb = emb / (emb.norm(dim=1, keepdim=True) + 1e-12)

        return emb.squeeze(0).cpu().numpy()

class CLIPEmbeddingModel(nn.Module):
    def __init__(self, device='cpu'):
        super(CLIPEmbeddingModel, self).__init__()
        self.device = device
        # Sử dụng model CLIP ViT-Base từ timm
        # vit_base_patch32_clip_224.openai tương đương với CLIP ViT-B/32
        
        
        self.model ,_, self.preprocess = open_clip.create_model_and_transforms('ViT-B-16', pretrained='laion2b_s34b_b88k')
        self.model = self.model.to(self.device)
        self.model.eval()
        self.to(self.device)

        # Lấy data config chuẩn của model để tạo transform (quan trọng vì CLIP normalize khác ImageNet)
        # data_config = timm.data.resolve_data_config(self.model.pretrained_cfg)
        # self.transform = timm.data.create_transform(**data_config, is_training=False)

    @torch.no_grad()
    def get_embedding(self, image):
        """
        Input: image (numpy array BGR from cv2)
        Output: embedding vector (numpy array)
        """
        # Chuyển BGR -> RGB và convert sang PIL Image để dùng transform của timm
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        x = self.preprocess(image).unsqueeze(0).to(self.device)
        
        # Preprocess: resize, center crop, normalize, to tensor
        # x = self.transform(img).unsqueeze(0).to(self.device)

        # Forward pass
        # Model của timm cho CLIP thường trả về output sau head rồi
        # Với vit_base_patch32_clip_224, output shape là [batch, 512]
        with torch.no_grad():
            features = self.model.encode_image(x)

        # Normalize vector (CLIP trained với normalized features)
        features = features / (features.norm(dim=1, keepdim=True) + 1e-12)

        return features.squeeze(0).cpu().numpy()

if __name__ == "__main__":
    # Khởi tạo model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = DinoEmbeddingModel(pretrained=True, device=device)
    print("Testing CLIPEmbeddingModel...")
    # model = CLIPEmbeddingModel(device=device)

    # Đọc ảnh
    image_path = "/home/minhanh/Downloads/project_home/image_smallmillo.png"
    if os.path.exists(image_path):
        image = cv2.imread(image_path)
        if image is not None:
            # Lấy embedding
            embedding_vector = model.get_embedding(image)
            print("Embedding shape:", embedding_vector.shape) # Should be (512,) for ViT-B/32
            print(embedding_vector[:10])  # in thử 10 giá trị đầu
        else:
            print(f"Failed to read image at {image_path}")
    else:
        print(f"Image not found at {image_path}")
