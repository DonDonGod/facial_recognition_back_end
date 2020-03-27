from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import os

from facial_recognition import settings
from webApp.models import USER
from webApp.models import IMG
from webApp.face_recognize import face_recognize

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = BASE_DIR.replace('\\', '/')

# Create your views here.

def homePage(request):
    return render(request,'homepage.html')

def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')



def addUser(request):
    if request.POST:
        a = request.POST.get('admin',None)
        b = request.POST.get('username',None)
        c = request.POST.get('password',None)
        USER.objects.create(admin=a, username=b, password=c)
        return render(request, 'result.html', context={'data': b})
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
        return render(request, 'dashboard.html', context={'user': arr})
    else:
        return render(request, 'dashboard.html', context={'user': "This user doesn't exist"})

def modifyUser(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    exist = USER.objects.filter(username=username)
    if exist:
        user = USER.objects.get(username=username)
        user.password = password
        user.save()
        return render(request, 'dashboard.html', context={'mod_result': "modification complete"})
    else:
        return render(request, 'dashboard.html', context={'mod_result': "This user doesn't exist"})


def deleteUser(request):
    username = request.POST.get('username', None)
    exist = USER.objects.filter(username = username)
    if exist:
        user = USER.objects.get(username = username)
        user.delete()
        return render(request, 'dashboard.html', context={'del_result': "deletion complete"})
    else:
        return render(request, 'dashboard.html', context={'del_result': "This user doesn't exist"})


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

        return render(request, 'homepage.html')
    else:
        return redirect('http://127.0.0.1:8000/homepage')

def showImg(request):
    if request.method == 'POST':
        imgs = IMG.objects.all()
        content = {'imgs': imgs}
        return render(request, 'dashboard.html', content)
    else:
        return redirect('http://127.0.0.1:8000/dashboard')

# 人脸识别
def recImg(request):
    if request.method == 'POST':
        imgs = IMG.objects.all()
        for i in imgs:
            old_path = os.path.join(BASE_DIR, 'media', i.img.name).replace('\\', '/')
            new_path = os.path.join(BASE_DIR, 'media', i.img.name).replace('\\', '/').replace('img','new_img')
            # print(old_path)
            # print(new_path)
            face_recognize(old_path, new_path)
    return redirect('http://127.0.0.1:8000/dashboard')

# 返回所有new_img里图片的路径
def showPath(request):
    if request.method == 'GET':
        rec_path = {}
        imgs = IMG.objects.all()
        for new_img in imgs:
            old_path = os.path.join(BASE_DIR, 'media', new_img.img.name).replace('\\', '/')
            new_path = os.path.join(BASE_DIR, 'media', new_img.img.name).replace('\\', '/').replace('img', 'new_img')
            rec_path[new_img.img.name] = new_path
        print(rec_path)
        return  redirect('http://127.0.0.1:8000/dashboard')
    else:
        return redirect('http://127.0.0.1:8000/dashboard')



# 删除所有数据
def delAllUser(request):
    USER.objects.all().delete()
    return HttpResponse('All users are deleted')
def delImg(request):
    IMG.objects.all().delete()
    return HttpResponse('All images are deleted')

