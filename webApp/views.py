from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from webApp.models import USER
from webApp.models import IMG



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
        content = {'imgs':imgs}
        for i in imgs:
            print (i.img.url)
        return render(request, 'dashboard.html', content)
    else:
        return redirect('http://127.0.0.1:8000/dashboard')

def delUser(request):
    USER.objects.all().delete()
    return HttpResponse('All users are deleted')

def delImg(request):
    IMG.objects.all().delete()
    return HttpResponse('All images are deleted')

