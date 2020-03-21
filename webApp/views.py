from django.shortcuts import render
from django.http import HttpResponse

from webApp.models import cal
from webApp.models import user
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
        a = request.POST['admin']
        b = request.POST['username']
        c = request.POST['password']
        user.objects.create(admin=a, username=b, password=c)
        return render(request, 'result.html', context={'data': b})
    else:
        HttpResponse("Go to dashboard first")

def uploadImg(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name = request.FILES.get('img').name
        )
        new_img.save()
    return render(request, 'homepage.html')

def showImg(request):
    imgs = IMG.objects.all()
    content = {'imgs':imgs}
    for i in imgs:
        print (i.img.url)
    return render(request, 'dashboard.html', content)

def delUser(request):
    user.objects.all().delete()
    return HttpResponse('All users are deleted')

def delImg(request):
    IMG.objects.all().delete()
    return HttpResponse('All images are deleted')



# Test
# def calPage(request):
#     return render(request,'cal.html')
# def calculate(request):
#     if request.POST:
#         a = request.POST['valueA']
#         b = request.POST['valueB']
#         sum = int(a)+int(b)
#         cal.objects.create(valueA=a, valueB=b,result=sum)
#         return render(request, 'result.html', context={'data':sum})
#     else:
#         HttpResponse("Go to homepage first")
# def calList(request):
#     data = cal.objects.all()
#     # for data in data:
#     #     print(data.valueA, data.valueB, data.result)
#     return render(request, "cal_list.html", context={"data": data})
# def deldata(request):
#     cal.objects.all().delete()
#     return HttpResponse('All data deleted')