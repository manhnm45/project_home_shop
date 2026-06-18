# import faiss
import numpy as np
import cv2
from get_embeding_model import EmbeddingModel, DinoEmbeddingModel, CLIPEmbeddingModel
import os
import torch 
import scipy.io as sio
import faiss
import json
import timm
import open_clip



device = "cpu"
# model = DinoEmbeddingModel(pretrained=True, device=device)
model = CLIPEmbeddingModel(device=device)      

# model.load_state_dict(torch.load("./resnet50_embedding_model.pt", map_location=device))
# model_path_save = "resnet50_embedding_model.pt"
# torch.save(model.state_dict(), model_path_save)
# model.eval()
def augumentation(image, augument_name):
    """Thực hiện các phép biến đổi đơn giản để tăng dữ liệu"""
    if augument_name == "flip":
        image= cv2.flip(image, 1)  # Lật ngang
    elif augument_name == "rotate90":
        image= cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # Quay 90 độ
    elif augument_name == "brighten":
        image= cv2.convertScaleAbs(image, alpha=1.2, beta=30)  # Tăng độ sáng
    elif augument_name == "rotate-90":
        image= cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Quay -90 độ
    return image
class Searchfaiss():
    def __init__(self, folder_image_build_index = None, folder_path_mat="./mat_file_save_with_model_embedding_clip", path_index = "faiss_index_clip.index", label_file="index.json"):
        super().__init__()
        self.label_file = label_file
        self.folder_path_mat = folder_path_mat
        os.makedirs(self.folder_path_mat,exist_ok=True)
        self.path_index = path_index
        self.folder_image_build_index = folder_image_build_index
        if not os.path.exists(self.path_index):
            print("Chua co index, tao moi")
            if self.folder_image_build_index is not None:
                for label_name in os.listdir(self.folder_image_build_index):
                    folder_label = os.path.join(self.folder_image_build_index,label_name)
                    for idx, image_name in  enumerate( os.listdir(folder_label)):
                        image_path = os.path.join(folder_label,image_name)
                        mat_path = os.path.join(self.folder_path_mat,f"{label_name}_{idx}.mat")
                        self.extrac_feature(image_path,label_name,mat_path)
                self.build_index()
            else:
                print("Khong co folder de tao index, vui long cung cap folder_image_build_index")
                return
        else:
            self.index = self.load_index()
    def extrac_feature(self, image_path, label, mat_path):
        list_augument = ["rotate90","flip","brighten","rotate-90"]
        image = cv2.imread(image_path)
        origin_embedding = model.get_embedding(image).reshape(1,-1).astype('float32')
        features  = []
        labels =  []
        features.append(origin_embedding)
        labels.append(label)
        for augument_name in list_augument:
            image_augument = augumentation(image.copy(), augument_name)
            augument_embedding =  model.get_embedding(image_augument).reshape(1,-1).astype('float32')
            label_augument = label
            features.append(augument_embedding)
            labels.append(label_augument)
        dict_gen_augument = {
            "features": np.array(features),
            "labels": np.array(labels)
        }      
        sio.savemat(mat_path,dict_gen_augument) 
        print("save done")
    def build_index(self):
        # self.index = faiss.IndexFlatL2(1024)
        self.index = faiss.IndexFlatL2(512)
        features_save, labels_save = [], []
        for filemat_name in os.listdir(self.folder_path_mat):
            file_mat = os.path.join(self.folder_path_mat,filemat_name)
            data = sio.loadmat(file_mat)
            features = data["features"]
            labels = data["labels"]
            for i in range(len(labels)):
                features_save.append(features[i])
                labels_save.append(labels[i])
        for i in range(len(features_save)):
            feature =  features_save[i].reshape(1,-1).astype('float32')
            self.index.add(feature)
        # print("label_save", labels_save)
        faiss.write_index(self.index, self.path_index)
        with open(self.label_file , "w") as f:
            json.dump(labels_save, f)
        print("Index built and saved to faiss_index.index")
    def load_index(self):
        index = faiss.read_index(self.path_index)
        return index
    def search(self, image_search, k=1):
        # index = self.load_index()
        test_image = cv2.imread(image_search)
        test_embedding = model.get_embedding(test_image).reshape(1, -1).astype('float32')   
        distances, indices = self.index.search(test_embedding, k)
        print("Top {} nearest neighbors:".format(k))
        for i in range(k):
            print("Index:", indices[0][i], "Distance:", distances[0][i])
            with open(self.label_file , "r") as f:
                data = json.load(f)
                # print("data", data)
                file_name = data[indices[0][i]]
            print("File name:", file_name)

    def search_image(self, image, k=1):
        top_file_name = []
        test_embedding = model.get_embedding(image).reshape(1, -1).astype('float32')   
        distances, indices = self.index.search(test_embedding, k)
        print("Top {} nearest neighbors:".format(k))
        for i in range(k):
            print("Index:", indices[0][i], "Distance:", distances[0][i])
            with open(self.label_file , "r") as f:
                data = json.load(f)
                file_name = data[indices[0][i]]
            print("File name:", file_name)
            top_file_name.append(file_name)
        return top_file_name

    def add_product_to_index(self, image_path, label):
        # index = self.load_index()
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to load image at {image_path}")
            return
        embeding = model.get_embedding(image).reshape(1, -1).astype('float32')
        self.index.add(embeding)
        faiss.write_index(self.index, self.path_index)
        with open(self.label_file , "r") as f: 
            labels = json.load(f)
        labels.append(label)
        with open(self.label_file , "w") as f:
            json.dump(labels, f)
        print(f"Added image {label} to index.")      



def extract_feature(image_path,label, mat_path):
    list_augument = ["rotate90","flip","brighten","rotate-90"]
    
    image = cv2.imread(image_path)
    origin_embedding = model.get_embedding(image).reshape(1, -1).astype('float32')
    features  = []
    labels =  []
    features.append(origin_embedding)
    labels.append(label)
    

    for augument_name in list_augument:
        image_augument = augumentation(image.copy(), augument_name)
        augument_embedding =  model.get_embedding(image_augument).reshape(1, -1).astype('float32')
        label_augument = label+ augument_name 
        features.append(augument_embedding)
        labels.append(label_augument)
    dict_gen_augument = {
        "features": np.array(features),
        "labels": np.array(labels)
    }      
    sio.savemat(mat_path,dict_gen_augument) 
    print(dict_gen_augument) 
    print("save done")
def build_index(folder_mat):
    # index = faiss.IndexFlatL2(1024)
    index = faiss.IndexFlatL2(512)
    features_save, labels_save = [], []
    for filemat_name in os.listdir(folder_mat):
        file_mat = os.path.join(folder_mat,filemat_name)
        data = sio.loadmat(file_mat)
        features = data["features"]
        labels = data["labels"]
        for i in range(len(labels)):
            features_save.append(features[i])
            labels_save.append(labels[i])
    # print("len_features_save", len(features_save))
    # print("labels", labels_save)  
    for i in range(len(features_save)):
        # print("feature", features_save[i].shape)
        feature =  features_save[i].reshape(1,-1).astype('float32')
        index.add(feature)
    

    faiss.write_index(index, "faiss_index.index")
    with open("index.json", "w") as f:
        json.dump(labels_save, f)
    print("Index built and saved to faiss_index.index")
def load_index(path_index):
    index = faiss.read_index(path_index)
    return index

if __name__=="__main__":
    import numpy as np
    folder_image_build_index = "./folder_image_crop_alige"
    # folder_mat = "/home/minhanh/Downloads/project_home/mat_file_save"
    # image_path="/home/minhanh/Downloads/project_home/image_smallmillo.png"
    # label="smallmillo"
    # mat_path="/home/minhanh/Downloads/project_home/mat_file_save/smallmillo.mat"
    # extract_feature(image_path,label, mat_path)

    #create mat file for all images in folder
    
    # for label_name in os.listdir(folder_image_build_index):
    #     folder_label = os.path.join(folder_image_build_index,label_name)
    #     for idx, image_name in  enumerate( os.listdir(folder_label)):
    #         image_path = os.path.join(folder_label,image_name)
    #         mat_path = os.path.join("/home/minhanh/Downloads/project_home/mat_file_save",f"{label_name}_{idx}.mat")
    #         extract_feature(image_path,label_name, mat_path)

    # build_index
    # build_index(folder_mat)
    # index = load_index("/home/minhanh/Downloads/project_home/faiss_index.index")
    # path_index = "/home/minhanh/Downloads/project_home/faiss_index.bin"
    # index = faiss.read_index(path_index)
    # Test tìm kiếm
    image_search = "/home/minhanh/Downloads/project_home/image_object_save/image_object_176262518892362_0.jpg"
    # test_image = cv2.imread(image_search)
    # test_embedding = model.get_embedding(test_image).reshape(1, -1).astype('float32')   
    # k = 5  # Số lượng kết quả trả về
    # distances, indices = index.search(test_embedding, k)
    # print("Top {} nearest neighbors:".format(k))
    # for i in range(k):
    #     print("Index:", indices[0][i], "Distance:", distances[0][i])
    #     with open("index.json", "r") as f:
    #         data = json.load(f)
    #         file_name = data[indices[0][i]]
    #     print("File name:", file_name)
    
    print("image_path search", image_search)
    
    # with torch.no_grad():
    #     e1 = model.get_embedding(test_image).reshape(1, -1).astype('float32')
    #     device = "cuda" if torch.cuda.is_available() else "cpu"
    #     model = EmbeddingModel(model_name='resnet50', pretrained=False, embedding_size=1024, device=device)
    #     model.load_state_dict(torch.load("/home/minhanh/Downloads/project_home/resnet50_embedding_model.pt", map_location=device))
    #     e2 = model.get_embedding(test_image).reshape(1, -1).astype('float32')
    # print(np.abs(e1 - e2).max())
    #use class Searchfaiss
    search_faiss = Searchfaiss(folder_image_build_index = "./folder_data_search_image_relative_product_name", folder_path_mat="./mat_file_save_with_model_embedding_clips_relative_avatar", path_index = "faiss_index_clip_relative_avatar.index", label_file="index.json")
    search_faiss.search(image_search, k=5)

