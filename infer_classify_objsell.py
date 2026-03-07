import cv2
import torch
import torchvision.transforms as transforms
import torch.nn as nn
import timm
import numpy
CLASSES = ['namngudenhi', 'haohao_box', 'brash_teeth', 'omachi_box', 'bimbimkhoaitayoka', 'haohao', 'botchiengion', 'thuoclathanglong', 'omachi', 'namngucahoi', 'kemdanhrangcloseup', 'cocacolalon_big_size', 'banhgaomatongichi', 'biaheineken', 'botchiengionmeizan', 'ruataylifebouy', 'bohucredbul', 'botgiatomo3kg', 'thuoclabaso555', 'botgiatomo350g', 'kokomi_box', 'kokomi', 'kemdanhrangps', 'banhtrungcusta', 'nuocruabatsunlight', 'namngu', 'botgiatomo5kg', 'bia333', 'suathtruemilk_bigsize', 'suamilo_bigsize', 'michinh', 'suamilo_smallsize', 'batlua', 'vicocacola']
device = "cuda" if torch.cuda.is_available() else "cpu"
class Model(nn.Module):
  def __init__(self, num_classes):
    super(Model, self).__init__()
    self.backbone = timm.create_model('resnet50', pretrained=True)
    self.fc = nn.Linear(1000, num_classes)
  def forward(self, x):
    x = self.backbone(x)
    x = self.fc(x)
    return x
def infer(model_checkpoint, image_path):
    model = Model(num_classes=34)
    model.load_state_dict(torch.load(model_checkpoint))
    model.eval()
    model.to(device)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = torch.from_numpy(image).permute(2, 0, 1).float().unsqueeze(0) / 255.0
    image = image.to(device)
    with torch.no_grad():
        result = model(image)
        result = result.argmax(dim=1)
    return result
def infer_image(model_checkpoint, image,CLASSES, device = device):
    model = Model(num_classes=34)
    model.load_state_dict(torch.load(model_checkpoint))
    model.eval()
    model.to(device)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = torch.from_numpy(image).permute(2, 0, 1).float().unsqueeze(0) / 255.0
    image = image.to(device)
    with torch.no_grad():
        result = model(image)
        result = result.argmax(dim=1)
        result = CLASSES[result]
    return result
if __name__=="__main__":
    model_checkpoint = "/home/minhanh/Downloads/project_home/best_model49.pth"
    image_path = "/home/minhanh/Downloads/project_home/image_thtruemilk_bigsize.png"
    result = infer(model_checkpoint, image_path)
    print("rerult",CLASSES[result])