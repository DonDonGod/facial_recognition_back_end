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

def uploadImg(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name = request.FILES.get('img').name
        )
        new_img.save()
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

def delUser(request):
    USER.objects.all().delete()
    return HttpResponse('All users are deleted')

def delImg(request):
    IMG.objects.all().delete()
    return HttpResponse('All images are deleted')

