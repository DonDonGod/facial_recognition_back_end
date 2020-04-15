import os
import numpy as np
import time
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import cv2
import  os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_img(path, read_num):#读取文件夹图片，文件夹名为标签
    images = []
    labels = []
    names = []
    folder_index = 0
    for folder_name in os.listdir(path):
        if folder_name == '.DS_Store':
            continue

        names.append(folder_name)
        for i in range(read_num):
            img = cv2.imread(str(path) + '/' + str(folder_name) + '/' + str(i) + '.jpg')#加载检测人物的脸
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#转化为单通道
            images.append(img)
            labels.append(folder_index)
        folder_index += 1
    
    images = np.array(images)  #x和y转化成张量？不然没法学习
    images = images.reshape((-1,64,64,1))
    
    labels = np.array(labels)  #把y转换成np.array形式

    return images, labels, names

def build_model(x_train, y_train, x_test, y_test, out_num):#模型训练
    model = keras.Sequential([
    keras.layers.Conv2D(
        input_shape=(x_train.shape[1],x_train.shape[2],x_train.shape[3]),
        filters=32,
        kernel_size=(3,3),
        strides=(1,1),
        padding='same',
        activation='relu'
    ),
    #keras.layers.BatchNormalization(),
    keras.layers.Conv2D(
        filters=16,
        kernel_size=(1,1),
        strides=(1,1),
        padding='valid',
        activation='relu'
    ),
    #keras.layers.BatchNormalization(),
    keras.layers.MaxPool2D(pool_size=(2,2)),
    keras.layers.Conv2D(
        filters=32,
        kernel_size=(3,3),
        strides=(1,1),
        padding='same',
        activation='relu'
    ),
    #keras.layers.BatchNormalization(),
    keras.layers.Conv2D(
        filters=16,
        kernel_size=(1,1),
        strides=(1,1),
        padding='valid',
        activation='relu'
    ),
    #keras.layers.BatchNormalization(),
    keras.layers.MaxPool2D(pool_size=(2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(out_num, activation='softmax')
    ])#NIN：卷BN卷BN池卷BN卷BN池 平 全连接 Dropout Softmax
    
    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )
    
    model.summary()
    
    #训练
    history = model.fit(x_train, y_train, batch_size=64, epochs=50, validation_split=0.1)#一般都是0.1的验证集，但是只有一张图片就不能有验证集了
    
    plt.figure()
    plt.plot(history.history['accuracy'], label='training')
    plt.plot(history.history['val_accuracy'], label='validation')
    plt.legend(loc='lower right')
    plt.show()
    
    
    #测试
    evaluate_result = model.evaluate(x_test, y_test)
    
    
    return model

def save_model(model, path):
    model.save(str(path) + '/trained_model.h5')


##################################################
def face_train(train_folder_path, read_faces_num, train_model_save_path):#路径格式类似'C:\\Users\\LUOJ\\Desktop\\Faces'   每个文件夹读几张脸张脸   图片为jpg
    x_data, y_data, names = load_img(train_folder_path, read_faces_num)
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.02, random_state=int(time.time()), shuffle=True)#分训练集、测试集
    out_num = len(names)#有几种标签
    #print(x_data.shape, y_data.shape)测试用的输出
    #print(x_train.shape, y_train.shape)
    #print(x_test.shape, y_test.shape)
    #print(names)
    #print(out_num)
    model = build_model(x_train, y_train, x_test, y_test, out_num)
    save_model(model, train_model_save_path)
###################################################


def read_model(model_name):
    model = keras.models.load_model(model_name)
    return model

def read_names(path):
    names = []
    for folder_name in os.listdir(path):
        if folder_name == '.DS_Store':
            continue
        names.append(folder_name)
    return names

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

def detect_face(img, model, names, predict_name_index):
    img_copy = img.copy()
    predict_name_accuracy = 0#用户脸中的准确度
    path = os.path.join(BASE_DIR, 'webApp/haarcascades/haarcascade_frontalface_alt2.xml').replace('\\', '/')
    face_cascade = cv2.CascadeClassifier(path)#创建Haar级联分类器 alt2的效果好一些
    
    #scaleFactor表示在每个图像尺寸上图像大小减小了多少，minNeighbors表示选择矩形时应该训练多少个邻居
    #返回检测出的所有人脸矩形四个点的位置列表[[x,y,w,h]]（四个点为x，y，x+w，y+h）
    face_rects = face_cascade.detectMultiScale(img_copy,scaleFactor = 1.1,minNeighbors = 3)

    if len(face_rects) == 0:#没检测到人脸
        return img_copy, predict_name_accuracy


    for (x, y, w, h) in face_rects:#对于每一张脸画框框
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 0, 255), 3)
        img_predict = img[y:y+h,x:x+w]
        img_predict = resize_img(img_predict)#把图片调整为64*64像素
        
        img_predict = cv2.cvtColor(img_predict, cv2.COLOR_BGR2GRAY)#转化为单通道
        
        img_predict = np.array(img_predict)  #转化成张量？
        img_predict = img_predict.reshape((1,64,64,1))
        
        label_predict = model.predict(img_predict)  #预测
        max_possible = np.argmax(label_predict[0])  #预测结果的最大值的index
        
        
        #print(label_predict)

         
        
        if label_predict[0][max_possible] >= 0.5:  #概率大于50%输出
            cv2.putText(img_copy, text=names[max_possible] + '(' + str(int(label_predict[0][max_possible]*100)) + '%)', org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1, color=(0,0,255),thickness=2, lineType=cv2.LINE_AA)#打印对应的名字和概率            
        else:
            cv2.putText(img_copy, text='Unknown', org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1, color=(0,0,255), thickness=2, lineType=cv2.LINE_AA)#打印Unknown

        
        predict_name_accuracy = max(predict_name_accuracy, label_predict[0][predict_name_index])#返回所有检测的脸中预测用户脸的最大准确度

        break#只检测一张脸
        
    return img_copy, predict_name_accuracy


###################################################
def face_predict(trained_model_path, face_folder_path, predict_photo_path, predicted_photo_save_path):#路径类似'C:\\Users\\LUOJ\\Desktop\\Faces'
    model = read_model(trained_model_path)#读取保存的模型
    names = read_names(face_folder_path)#读取所有脸文件夹的标签
    # print('0:' + names[0] + ' and 1:' + names[1] + '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    
    predict_photo = cv2.imread(predict_photo_path)#读取要预测的图片

    predicted_photo, predict_name_accuracy = detect_face(predict_photo, model, names, 0)#预测图片，返回以预测的图片和最大的精确度

    cv2.imwrite(predicted_photo_save_path, predicted_photo)#保存画了框框的图片到保存路径

    return predict_name_accuracy #返回准确度
###################################################

# 206行苹果电脑predicted_photo, predict_name_accuracy = detect_face(predict_photo, model, names, 1)

# 106行 1.fuzixin文件夹 3.模型存在哪里 4.读取模型
# 189行trained_model_path是trained_model下.h5文件 // face_folder_path是fuzixin文件夹 // predict_photo_path 要检测.jpg文件 // predicted_photo_save_path检测完图片存在哪

# 89行 50/100