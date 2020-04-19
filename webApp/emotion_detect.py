import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_model(path):
    model = keras.models.load_model(path)
    return model

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
    img_resize = cv2.resize(constant, (48, 48))#补成64*64大小
    
    return img_resize

def detect_face(img, model):
    img_copy = img.copy()
    predict_emotion = -1
    predict_accuracy = 0
    path = os.path.join(BASE_DIR, 'webApp/haarcascades/haarcascade_frontalface_alt2.xml').replace('\\', '/')
    face_cascade = cv2.CascadeClassifier(path)#创建Haar级联分类器 alt2的效果好一些

    
    #scaleFactor表示在每个图像尺寸上图像大小减小了多少，minNeighbors表示选择矩形时应该训练多少个邻居
    #返回检测出的所有人脸矩形四个点的位置列表[[x,y,w,h]]（四个点为x，y，x+w，y+h）
    face_rects = face_cascade.detectMultiScale(img_copy,scaleFactor = 1.1,minNeighbors = 3)

    for (x, y, w, h) in face_rects:#对于每一张脸画框框
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 0, 255), 3)
        img_predict = img[y:y+h,x:x+w]
        img_predict = resize_img(img_predict)#把图片调整为48*48像素
        
        img_predict = cv2.cvtColor(img_predict, cv2.COLOR_BGR2GRAY)#转化为单通道
        
        img_predict = np.array(img_predict)  #转化成张量？
        img_predict = img_predict.reshape((1,48,48,1))
        
        label_predict = model.predict(img_predict)  #预测
        max_possible = np.argmax(label_predict[0])  #预测结果的最大值的index
        
        
        #print(label_predict)
        
        if max_possible == 0:
            cv2.putText(img_copy, text='angry(' + str(int(label_predict[0][max_possible]*100)) + '%)', org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1, color=(0,0,255),thickness=2, lineType=cv2.LINE_AA)#打印对应的表情和概率
        elif max_possible == 1:
            cv2.putText(img_copy, text='disgust(' + str(int(label_predict[0][max_possible]*100)) + '%)', org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1, color=(0,0,255),thickness=2, lineType=cv2.LINE_AA)#打印对应的表情和概率
        elif max_possible == 2:
            cv2.putText(img_copy, text='fear(' + str(int(label_predict[0][max_possible]*100)) + '%)', org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1, color=(0,0,255),thickness=2, lineType=cv2.LINE_AA)#打印对应的表情和概率
        elif max_possible == 3:
            cv2.putText(img_copy, text='happy(' + str(int(label_predict[0][max_possible]*100)) + '%)', org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1, color=(0,0,255),thickness=2, lineType=cv2.LINE_AA)#打印对应的表情和概率
        elif max_possible == 4:
            cv2.putText(img_copy, text='sad(' + str(int(label_predict[0][max_possible]*100)) + '%)', org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1, color=(0,0,255),thickness=2, lineType=cv2.LINE_AA)#打印对应的表情和概率
        elif max_possible == 5:
            cv2.putText(img_copy, text='surprise(' + str(int(label_predict[0][max_possible]*100)) + '%)', org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1, color=(0,0,255),thickness=2, lineType=cv2.LINE_AA)#打印对应的表情和概率
        elif max_possible == 6:
            cv2.putText(img_copy, text='neutral(' + str(int(label_predict[0][max_possible]*100)) + '%)', org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1, color=(0,0,255),thickness=2, lineType=cv2.LINE_AA)#打印对应的表情和概率

        predict_emotion = max_possible
        predict_accuracy = max(predict_accuracy, label_predict[0][max_possible])

        break#只检测一张脸
          
    return img_copy, predict_emotion, predict_accuracy

def emotion_predict(trained_model_path, predict_photo_path, predicted_photo_save_path):#路径类似'C:\\Users\\LUOJ\\Desktop\\Faces'
    model = read_model(trained_model_path)#读取保存的模型，表情专属模型
        
    predict_photo = cv2.imread(predict_photo_path)#读取要预测的图片

    predicted_photo, predict_emotion, predict_accuracy = detect_face(predict_photo, model)#预测图片，返回以预测的图片和最大的精确度

    cv2.imwrite(predicted_photo_save_path, predicted_photo)#保存画了框框的图片到保存路径

    return predict_emotion, predict_accuracy #返回表情index和准确度

##########
#-1为没脸
#0为angy
#1为disgust
#2为fear
#3为happy
#4为sad
#5为surprise
#6为neutral
