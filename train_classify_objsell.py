import torch
import numpy
import cv2
import os
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import timm
CLASSES = ['namngudenhi', 'haohao_box', 'brash_teeth', 'omachi_box', 'bimbimkhoaitayoka', 'haohao', 'botchiengion', 'thuoclathanglong', 'omachi', 'namngucahoi', 'kemdanhrangcloseup', 'cocacolalon_big_size', 'banhgaomatongichi', 'biaheineken', 'botchiengionmeizan', 'ruataylifebouy', 'bohucredbul', 'botgiatomo3kg', 'thuoclabaso555', 'botgiatomo350g', 'kokomi_box', 'kokomi', 'kemdanhrangps', 'banhtrungcusta', 'nuocruabatsunlight', 'namngu', 'botgiatomo5kg', 'bia333', 'suathtruemilk_bigsize', 'suamilo_bigsize', 'michinh', 'suamilo_smallsize', 'batlua', 'vicocacola']
def convert_one_host(classes, label_index):
  one_hot = torch.zeros(len(classes))
  one_hot[label_index] = 1
  return one_hot
  
class dataset():
  def __init__(self, root_dir, transform=None, phase="train"):
    self.root_dir = root_dir
    self.transform = transform
    self.data_folder = os.path.join(root_dir, phase)
    self.image_paths = []
    self.label_paths = []
    classes = []
    for folder in os.listdir(self.data_folder):
      classes.append(folder)
      folder_path = os.path.join(self.data_folder, folder)
      for image in os.listdir(folder_path):
        self.image_paths.append(os.path.join(folder_path, image))
        self.label_paths.append(folder)
    self.classes = classes
    # print("self.classes",self.classes)

  
  
  def __getitem__(self, idx):
    image_path = self.image_paths[idx]
    label = self.label_paths[idx]
    label_index = CLASSES.index(label)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    one_hot = convert_one_host(CLASSES, label_index)
    image = image.astype(numpy.float32) / 255.0
    if self.transform:
      image = self.transform(image)
    return image, one_hot
  def __len__(self):
    return len(self.image_paths)


class Model(nn.Module):
  def __init__(self, num_classes):
    super(Model, self).__init__()
    self.backbone = timm.create_model('resnet50', pretrained=True)
    self.fc = nn.Linear(1000, num_classes)
  def forward(self, x):
    x = self.backbone(x)
    x = self.fc(x)
    return x

data_path = "./dataset_obj_sell"
data_train = dataset(data_path, transform=transforms.ToTensor(), phase="train")
data_val = dataset(data_path, transform=transforms.ToTensor(), phase="valid")
data_loader_train = DataLoader(data_train, batch_size=32, shuffle=True,drop_last=True)
data_loader_val = DataLoader(data_val, batch_size=32, shuffle=True,drop_last=True)

model = Model(num_classes=34)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
train_losses = []
val_losses = []
train_accuracies = []
# val_accuracies = []
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
epochs = 50
for epoch in range(epochs):
    model.train()
    train_loss = 0
    correct = 0
    total = 0
    
    for images, labels in tqdm(data_loader_train):
        images, labels = images.to(device), labels.to(device)  # Chuyển dữ liệu lên GPU nếu có
        
        optimizer.zero_grad()
        outputs = model(images)
        print("output",outputs.argmax(dim=1))
        print("label",labels.argmax(dim=1))
        # ✅ Chuyển labels về dạng 1D (nếu cần)
        # if labels.ndim > 1:
        #     labels = labels.squeeze()
        
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        train_loss += loss.item()
        
        # ✅ Chuyển outputs về dạng index của lớp
        # _, predicted = torch.max(outputs, 1)
        
        total += labels.size(0)
        predicted = outputs.argmax(dim=1)
        labels = labels.argmax(dim=1)  
        correct += (predicted == labels).sum().item()
    
    train_loss /= len(data_loader_train)
    train_accuracy = correct / total
    train_losses.append(train_loss)
    train_accuracies.append(train_accuracy)

    # **🔹 Evaluate on validation set**
    model.eval()
    val_loss = 0
    correct = 0
    total = 0
    val_accuracy_max = 0.0
    with torch.no_grad():
        for images, labels in tqdm(data_loader_val):
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            
            # if labels.ndim > 1:
            #     labels = labels.squeeze()
            
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            
            total += labels.size(0)
            predicted = outputs.argmax(dim=1)
            labels = labels.argmax(dim=1)  
            correct += (predicted == labels).sum().item()
    
    val_loss /= len(data_loader_val)
    val_accuracy = correct / total
    val_losses.append(val_loss)
    # val_accuracies.append(val_accuracy)
    
    print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f}, Train Acc: {train_accuracy:.4f}, Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}")
    if val_accuracy > val_accuracy_max:
        print("saved")
        val_accuracy_max = val_accuracy
        torch.save(model.state_dict(), f"./best_model{epoch}.pth")
  


  