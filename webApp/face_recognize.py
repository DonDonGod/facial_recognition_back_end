import numpy as np
#import matplotlib.pyplot as plt
import cv2
import  os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def detect_face(img, face_cascade):#检测人脸
    img_copy = img.copy()
    
    #scaleFactor表示在每个图像尺寸上图像大小减小了多少，minNeighbors表示选择矩形时应该训练多少个邻居
    #返回检测出的所有人脸矩形四个点的位置列表[[x,y,w,h]]（四个点为x，y，x+w，y+h）
    face_rects = face_cascade.detectMultiScale(img_copy,scaleFactor = 1.1,minNeighbors = 3)

    for (x, y, w, h) in face_rects:
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (255, 255, 255), 3)

    return img_copy

def face_recognize(img_path, img_new_path):#主方法，参数为.../a.jpg
    c_path = os.path.join(BASE_DIR, 'webApp/haarcascades/haarcascade_frontalface_default.xml').replace('\\', '/')

    face_cascade = cv2.CascadeClassifier(c_path)#加载Haar级联分类器

    img = cv2.imread(img_path)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_detection = detect_face(img, face_cascade)#人脸检测

    cv2.imwrite(img_new_path, img_detection)
