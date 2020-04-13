import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import  os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resize_img(img):
    h, w, _ = img.shape
    top, bottom, left, right = (0, 0, 0, 0)#需要增加的像素长
    
    if h > w:
        left = (h - w) // 2       #“//”为整数除法的意思，“/”为小数除法的意思
        right = (h - w) - left    #左右各一半
    elif w > h:
        top = (w - h) // 2        #“//”为整数除法的意思，“/”为小数除法的意思
        bottom = (w - h) - top    #上下各一半
    
    constant = cv2.copyMakeBorder(img, top , bottom, left, right, cv2.BORDER_CONSTANT, value=[0,0,0])#resize参数，黑色补边像素
    img_resize = cv2.resize(constant, (64, 64))#补成64*64大小
    
    return img_resize

def detect_face(img):
    img_copy = img.copy()
    img_save = img_copy
    isDetected = False
    
    path = os.path.join(BASE_DIR, 'webApp/haarcascades/haarcascade_frontalface_alt2.xml').replace('\\', '/')
    face_cascade = cv2.CascadeClassifier(path)#创建Haar级联分类器 alt2的效果好一些
    
    #scaleFactor表示在每个图像尺寸上图像大小减小了多少，minNeighbors表示选择矩形时应该训练多少个邻居
    #返回检测出的所有人脸矩形四个点的位置列表[[x,y,w,h]]（四个点为x，y，x+w，y+h）
    face_rects = face_cascade.detectMultiScale(img_copy,scaleFactor = 1.1,minNeighbors = 3)

    for (x, y, w, h) in face_rects:#对于每一张脸画框框
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 0, 255), 3)
        img_save = img[y:y+h,x:x+w]
        img_save = resize_img(img_save)#把保存的图片调整为64*64像素
        isDetected = True
        break#只检测一张脸
    
    return img_save, isDetected

# def deal_face(img):
# #     return detect_face(img)#返回一张处理好的人脸图片
# #

def deal_face(img_path, save_path):
    flag = 0
    img = cv2.imread(img_path)#jpg
    img, isDetected = detect_face(img)#返回一张处理好的人脸图片
    if isDetected:
        cv2.imwrite(save_path, img)#jpg
        flag += 1
    return flag

# count
# save_path 是fuzixin/Client

