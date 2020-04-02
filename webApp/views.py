from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
import os
import json

from facial_recognition import settings
from webApp.models import USER
from webApp.models import IMG
from webApp.face_recognize import face_recognize
from webApp.face_recognize_controller import face_predict
from webApp.face_recognize_controller import face_train

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = BASE_DIR.replace('\\', '/')

# Create your views here.

def homePage(request):
    return render(request,'homepage.html')

def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def addUser(request):
    if request.method == 'POST':
        a = request.POST.get('admin',None)
        b = request.POST.get('username',None)
        c = request.POST.get('password',None)
        USER.objects.create(admin=a, username=b, password=c)
        return HttpResponse("Successful add user: ", b)
    else:
        return redirect('http://127.0.0.1:8000/dashboard')


def findUser(request):
    username = request.POST.get('username', None)
    result = USER.objects.filter(username = username)
    arr = []
    for i in result:
        content = {'admin': i.admin, 'username': i.username, 'password': i.password}
        arr.append(content)
    if arr:
        return HttpResponse(arr)
    else:
        return HttpResponse("The user does not exist")

def modifyUser(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    exist = USER.objects.filter(username=username)
    if exist:
        user = USER.objects.get(username=username)
        user.password = password
        user.save()
        return HttpResponse("modification complete: ",username)
    else:
        return HttpResponse("The user does not exist")

def deleteUser(request):
    username = request.POST.get('username', None)
    exist = USER.objects.filter(username = username)
    if exist:
        user = USER.objects.get(username = username)
        user.delete()
        return HttpResponse("deletion complete")
    else:
        return HttpResponse("The user does not exist")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 手动上传照片
def uploadImg(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name = request.FILES.get('img').name
        )
        new_img.save()
        old_path = os.path.join(BASE_DIR, 'media', new_img.img.name).replace('\\', '/')
        new_path = os.path.join(BASE_DIR, 'media', new_img.img.name).replace('\\', '/').replace('img', 'new_img')
        face_recognize(old_path, new_path)
        return HttpResponse("upload successfully")
    else:
        return redirect('http://127.0.0.1:8000/homepage')

# 展示全部原始图片path
def showImg(request):
    if request.method == 'POST':
        imgs = IMG.objects.all()
        content = {'imgs': imgs}
        return render(request, 'dashboard.html', content)
    else:
        return redirect('http://127.0.0.1:8000/dashboard')

# 返回所有new_img里图片的路径
def showPath(request):
    if request.method == 'POST':
        rec_path = {}
        imgs = IMG.objects.all()
        for new_img in imgs:
            old_path = os.path.join(BASE_DIR, 'media', new_img.img.name).replace('\\', '/')
            new_path = os.path.join(BASE_DIR, 'media', new_img.img.name).replace('\\', '/').replace('img', 'new_img')
            rec_path[new_img.name]=new_path
        # print(rec_path)
        # return HttpResponse(rec_path)
        return HttpResponse(json.dumps(rec_path), content_type="application/json")
    else:
        return redirect('http://127.0.0.1:8000/dashboard')

# def showImg(request):
#     if request.method == 'POST':
#         imgs = IMG.objects.all()
#         path = []
#         for img in imgs:
#             path.append(img.img.url)
#         return HttpResponse(path)
#     else:
#         return redirect('http://127.0.0.1:8000/dashboard')


# 人脸识别算法1.0
# def recImg(request):
#     if request.method == 'POST':
#         imgs = IMG.objects.all()
#         for i in imgs:
#             old_path = os.path.join(BASE_DIR, 'media', i.img.name).replace('\\', '/')
#             new_path = os.path.join(BASE_DIR, 'media', i.img.name).replace('\\', '/').replace('img','new_img')
#             face_recognize(old_path, new_path)
#         return  HttpResponse("recognize successfully")
#     else:
#         return redirect('http://127.0.0.1:8000/dashboard')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 将img里的图片根据username移动到Faces文件夹里(东哥算法)
def setFace(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('face', None)
        username = request.POST.get('username', None)
        username1 = file_obj.name
        file = os.path.join(BASE_DIR, 'webApp/Faces/',username,username1).replace('\\', '/')
        userface = os.path.join(BASE_DIR, 'webApp/Faces/',username).replace('\\', '/')
        if not os.path.exists(userface):
            os.mkdir(userface)
        with open(file, 'wb+') as f:
            f.write(file_obj.read())
        return HttpResponse("set face successfully")

# 模型训练
def trainModel(request):
    if request.method == 'POST':
        face_path = os.path.join(BASE_DIR, 'webApp/Faces').replace('\\', '/')
        model_path = os.path.join(BASE_DIR, 'webApp/trained_model/test').replace('\\', '/')
        face_train(face_path,10,model_path)
        return HttpResponse("train successfully")
    else:
        return redirect('http://127.0.0.1:8000/dashboard')

# 模型训练(每次有新的用户注册就要训练)
# def trainModel(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         face_path = os.path.join(BASE_DIR, 'webApp/Faces').replace('\\', '/')
#         model_path = os.path.join(BASE_DIR, 'webApp/trained_model',username).replace('\\', '/')
#         if not os.path.exists(model_path):
#             os.mkdir(model_path)
#         face_train(face_path,10,model_path)
#         return HttpResponse("train successfully")
#     else:
#         return redirect('http://127.0.0.1:8000/dashboard')

# 人脸识别算法2.0
def recImg(request):
    if request.method == 'POST':
        face_path = os.path.join(BASE_DIR, 'webApp/Faces').replace('\\', '/')
        model_path = os.path.join(BASE_DIR, 'webApp/trained_model/test/trained_model.h5').replace('\\', '/')
        old_path = os.path.join(BASE_DIR, 'media/test_origin/1.jpg').replace('\\', '/')
        new_path = os.path.join(BASE_DIR, 'media/test_predict/1.jpg').replace('\\', '/')
        a = face_predict(model_path,face_path,old_path,new_path)
        return HttpResponse(a)
    else:
        return redirect('http://127.0.0.1:8000/dashboard')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# 删除所有数据
def delAllUser(request):
    USER.objects.all().delete()
    return HttpResponse('All users are deleted')
def delImg(request):
    IMG.objects.all().delete()
    return HttpResponse('All images are deleted')


# 1.用户注册时前端拍10张照片，发给后端
# 2.把用户的10张照片存在Faces文件夹的顶部
# 3.训练该用户的模型
# 4.用户答题时拍照片，运行predict函数，返回准确度
