from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
import os
import json
import shutil


from webApp.models import USER
from webApp.models import ADMIN
from webApp.models import SCORE

from webApp.face_recognize_controller import face_predict
from webApp.face_recognize_controller import face_train
from webApp.face_deal import deal_face
from webApp.emotion_detect import emotion_predict

import subprocess
from django.views.decorators.csrf import csrf_exempt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = BASE_DIR.replace('\\', '/')

# Create your views here.

def homePage(request):
    return render(request, 'homepage.html')

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
        if a == '0':
            USER.objects.create(admin=a, username=b, password=c)
            return HttpResponse("Successful add user")
        if a == '1':
            ADMIN.objects.create(admin=a, username=b, password=c)
            return HttpResponse("Successful add admin")

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


# 登录
def login(request):
    if request.method == 'POST':
        admin = request.POST.get('admin', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if admin == '0':
            exist = USER.objects.filter(username=username)
            if exist:
                user = USER.objects.get(username=username)
                p = user.password
                if password == p:
                    return HttpResponse('Login successfully')
                else:
                    return HttpResponse('Wrong username or password')
            else:
                return HttpResponse('The user does not exist')

        if admin == '1':
            exist = ADMIN.objects.filter(username=username)
            if exist:
                admin = ADMIN.objects.get(username=username)
                p = admin.password
                if password == p:
                    return HttpResponse('Login successfully')
                else:
                    return HttpResponse('Wrong username or password')
            else:
                return HttpResponse('The admin does not exist')

    else:
        return redirect('http://127.0.0.1:8000/dashboard')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 将img里的图片根据username移动到Faces文件夹里(东哥算法)
def setFace(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('face', None)
        username = request.POST.get('username', None)
        username1 = file_obj.name
        userface = os.path.join(BASE_DIR, 'webApp/Faces/',username).replace('\\', '/')
        otherpath = os.path.join(BASE_DIR, 'webApp/Faces/',username, 'Other').replace('\\', '/')
        clientpath = os.path.join(BASE_DIR, 'webApp/Faces/',username, 'Client').replace('\\', '/')
        copypath = os.path.join(BASE_DIR, 'webApp/Other').replace('\\', '/')

        # 第一次注册，创建该用户文件夹
        if not os.path.exists(userface):
            os.mkdir(userface)
            os.mkdir(otherpath)
            os.mkdir(clientpath)
            # 把Other复制进来
            all_list = os.listdir(copypath)
            for i in all_list:
                a = os.path.join(BASE_DIR, 'webApp/Other',i).replace('\\', '/')
                b = os.path.join(BASE_DIR, 'webApp/Faces/',username, 'Other',i).replace('\\', '/')
                shutil.copyfile(a,b)

        # 将照片写入Client
        file = os.path.join(BASE_DIR, 'webApp/Faces/', username, 'Client/', username1).replace('\\', '/')
        with open(file, 'wb+') as f:
            f.write(file_obj.read())
            # 检测是否是人脸
            flag = deal_face(file, file)
        # 没有人别出人脸将其删除 (1:成功识别人脸; 0:未检测出人脸)
        if flag == 0:
            os.remove(file)

        # 返回当前Client文件夹下有多少张有效图片
        list = os.listdir(clientpath)
        size = len(list)
        return HttpResponse(size)


# 检查Client文件夹里是否有100张照片 如果小于100清空文件夹
def check(request):
    username = request.POST.get('username', None)
    clientpath = os.path.join(BASE_DIR, 'webApp/Faces/', username, 'Client').replace('\\', '/')
    all_list = os.listdir(clientpath)
    size = len(all_list)
    if size<100:
        for i in all_list:
            file = os.path.join(BASE_DIR, 'webApp/Faces/', username, 'Client/', i).replace('\\', '/')
            os.remove(file)
    return HttpResponse(size)


# 模型训练(每次有新的用户注册就要训练)
def trainModel(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        face_path = os.path.join(BASE_DIR, 'webApp/Faces',username).replace('\\', '/')
        model_path = os.path.join(BASE_DIR, 'webApp/trained_model',username).replace('\\', '/')

        if not os.path.exists(model_path):
            os.mkdir(model_path)

        face_train(face_path,100,model_path)
        return HttpResponse("train successfully")
    else:
        return redirect('http://127.0.0.1:8000/dashboard')


# 人脸识别算法2.0
def recImg(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('face', None)
        username = request.POST.get('username', None)
        username1 = file_obj.name
        a = os.path.join(BASE_DIR, 'media/test_origin', username).replace('\\', '/')
        b = os.path.join(BASE_DIR, 'media/test_predict', username).replace('\\', '/')
        old_path = os.path.join(BASE_DIR, 'media/test_origin', username, username1).replace('\\', '/')
        new_path = os.path.join(BASE_DIR, 'media/test_predict', username, username1).replace('\\', '/')
        if not os.path.exists(a):
            os.mkdir(a)
        if not os.path.exists(b):
            os.mkdir(b)

        with open(old_path, 'wb+') as f:
            f.write(file_obj.read())
        face_path = os.path.join(BASE_DIR, 'webApp/Faces',username).replace('\\', '/')
        model_path = os.path.join(BASE_DIR, 'webApp/trained_model',username,'trained_model.h5').replace('\\', '/')

        acc = face_predict(model_path,face_path,old_path,new_path)
        return HttpResponse(acc)
    else:
        return redirect('http://127.0.0.1:8000/dashboard')


# 表情识别算法
def emotion(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        file_obj = request.FILES.get('face', None)
        username1 = file_obj.name
        a = os.path.join(BASE_DIR, 'media/emotion_origin', username).replace('\\', '/')
        b = os.path.join(BASE_DIR, 'media/emotion_predict', username).replace('\\', '/')
        if not os.path.exists(a):
            os.mkdir(a)
        if not os.path.exists(b):
            os.mkdir(b)

        old_path = os.path.join(BASE_DIR, 'media/emotion_origin', username, username1).replace('\\', '/')
        new_path = os.path.join(BASE_DIR, 'media/emotion_predict', username, username1).replace('\\', '/')
        with open(old_path, 'wb+') as f:
            f.write(file_obj.read())

        model_path = os.path.join(BASE_DIR, 'webApp/trained_model/emotion_model.h5').replace('\\', '/')
        type, acc = emotion_predict(model_path, old_path, new_path)
        acc = float(acc)

        if type == -1:
            data = {'type':'No faces detected',
                    'acc':acc
                   }

            os.remove(old_path)
            os.remove(new_path)
            return JsonResponse(data)
        if type == 0:
            data = {'type': 'angry',
                    'acc': acc
                    }
            return JsonResponse(data)
        if type == 1:
            data = {'type': 'disgust',
                    'acc': acc
                    }
            return JsonResponse(data)
        if type == 2:
            data = {'type': 'fear',
                    'acc': acc
                    }
            return JsonResponse(data)
        if type == 3:
            data = {'type': 'happy',
                    'acc': acc
                    }
            return JsonResponse(data)
        if type == 4:
            data = {'type': 'sad',
                    'acc': acc
                    }
            return JsonResponse(data)
        if type == 5:
            data = {'type': 'surprise',
                    'acc': acc
                    }
            return JsonResponse(data)
        if type == 6:
            data = {'type': 'neutral',
                    'acc': acc
                    }
            return JsonResponse(data)
    else:
        return redirect('http://127.0.0.1:8000/dashboard')



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def run_code(code):
    try:
        output = subprocess.check_output(['python', '-c', code],
                                         universal_newlines=True,
                                         stderr=subprocess.STDOUT,
                                         timeout=30)
    except subprocess.CalledProcessError as e:
        output = e.output
    except subprocess.TimeoutExpired as e:
        output = '\r\n'.join(['Time Out!!!', e.output])
    return output


def ide(request):
    if request.method == 'POST':
        code = request.POST.get('code', None)
        output = run_code(code)
        return HttpResponse(output)
    else:
        return redirect('http://127.0.0.1:8000/dashboard')




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 删除所有数据
def delAllUser(request):
    USER.objects.all().delete()
    return HttpResponse('All users are deleted')
def delAllAdmin(request):
    ADMIN.objects.all().delete()
    return HttpResponse('All admins are deleted')


# 1.用户注册时前端拍10张照片，发给后端
# 2.把用户的10张照片存在Faces文件夹的顶部
# 3.训练该用户的模型
# 4.用户答题时拍照片，运行predict函数，返回准确度
