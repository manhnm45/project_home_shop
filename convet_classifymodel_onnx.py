import os
import copy
import time
import tqdm

import numpy as np
import torch
from torch import autocast

from cls_model import *


class WrapperWithPreprocess(torch.nn.Module):
    def __init__(self, model, device):
        super().__init__()
        self.model = model.to(device)
        self.model.eval()

    def forward(self, x):
        # preprocess
        x[:,0,:,:] = ((x[:,0,:,:]/255.0) - 0.485)/0.229
        x[:,1,:,:] = ((x[:,1,:,:]/255.0) - 0.456)/0.224
        x[:,2,:,:] = ((x[:,2,:,:]/255.0) - 0.406)/0.225
        
        # x = x.to(device)
        logit = self.model(x)
        return torch.softmax(logit, dim = 1)

def finetune(is_load = False):
    weight_path = "/home1/data/vinhnguyen/Color_Car_Cls/weights_mobilenet_v3_large_v4_add_SEblock/best.pth"
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    
    model = ImageClassifier(image_encoder = None, classification_head = None, backbone_name="mobilenet_v3_large")
    model = model.load(weight_path)
    model = WrapperWithPreprocess(model, device)
    model.eval()
    
    
    # Export the model
    x = torch.randn(1, 3, 224, 224, requires_grad=True).to(device)
    torch.onnx.export(model,               
                      x,                         
                      "/home1/data/vinhnguyen/Color_Car_Cls/weights_mobilenet_v3_large_v4_add_SEblock/car_color_cls_mobilenet_v3_large_v4_add_SEblock.onnx",
                      export_params=True,
                      opset_version=11,
                      do_constant_folding=True,
                      input_names = ['input'],
                      output_names = ['output'],
                      dynamic_axes={'input' : {0 : 'batch_size'},
                                    'output' : {0 : 'batch_size'}})

if __name__ == '__main__':
    finetune()