import time
import os
import numpy as np
class Trackingobject():
    def __init__(self, thres_distance=1.1):
        self.embedding = []
        self.timestamp = []
        self.id_tracking = []
    def clean(self):
        embedding_new = []
        timestamp_new = []
        id_tracking_new = []
        current_time = time.time()
        for i in range(len(self.timestamp)):
            if current_time - self.timestamp[i] < 10:
                embedding_new.append(self.embedding[i])
                timestamp_new.append(self.timestamp[i])
                id_tracking_new.append(self.id_tracking[i])
        self.embedding = embedding_new
        self.timestamp = timestamp_new
        self.id_tracking = id_tracking_new


    @staticmethod
    def caculate_l2_distance(emb1, emb2):
        dist = sum((a - b) ** 2 for a, b in zip(emb1, emb2)) ** 0.5
        return dist
    def check_distance(self, embedding):
        list_distance =  []
        for i in range(len(self.embedding)):
            list_distance.append(self.caculate_l2_distance(embedding, self.embedding[i]))
        print("list distance: ", list_distance)
    # def c