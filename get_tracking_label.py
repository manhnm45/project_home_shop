import os
import pika
import json
import rabbitmq
import yaml
import cv2
import numpy as np
from get_embeding_model import EmbeddingModel
import torch
import faiss

device = "cuda" if torch.cuda.is_available() else "cpu"
model = EmbeddingModel(model_name='resnet50', pretrained=False, embedding_size=1024, device=device)
model.load_state_dict(torch.load("/home/minhanh/Downloads/project_home/resnet50_embedding_model.pt", map_location=device))
def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config

queu_name_push = "tracking_label"
queu_name_get = "read_rtsp"

def callback_func(body):
    confidence = body.get("confidente", [])
    image_paths = body.get("image_path", [])
    timestamps = body.get("timestamp", [])
    xyxyxyxy = body.get("xyxyxyxy", [])
    print("Received message")
    for idx, image_path in enumerate(image_paths):
        image = cv2.imread(image_path)
        image_crop  = 
        
