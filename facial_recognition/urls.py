"""facial_recognition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('homepage/', views.homePage),
    path('dashboard/', views.dashboard),

    # 添加用户
    path('dashboard/add_user', views.addUser),
    # 查找用户
    path('dashboard/find_user', views.findUser),
    # 修改用户
    path('dashboard/modify_user', views.modifyUser),
    # 删除用户
    path('dashboard/delete_user', views.deleteUser),


    # 上传图片并识别（原图在media/img, 识别后的图在media/new_img）
    path('homepage/upload', views.uploadImg),
    # 展示图片
    path('dashboard/show', views.showImg),
    # 统一识别全部图片
    path('dashboard/rec', views.recImg),
    # 展示所有识别后图片路径（字典）
    path('dashboard/path', views.showPath),

    # 删除全部数据
    path('dashboard/delUser', views.delAllUser),
    path('dashboard/delImg', views.delImg),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 47811160+FuZixin@users.noreply.github.com