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
    path('dashboard/add_admin', views.addAdmin),
    # 修改用户
    path('dashboard/modify_user', views.modifyUser),
    # 删除用户
    path('dashboard/delete_user', views.deleteUser),

    # 登录
    path('dashboard/login', views.login),

    # 返回全部学生
    path('dashboard/student_list', views.student_list),
    # 返回某个学生个人信息
    path('dashboard/student_info', views.student_info),
    # 返回某个学生考试及表情信息
    path('dashboard/exam_result', views.exam_result),

    # 返回本人正常图片
    path('dashboard/origin', views.original_picture),
    # 返回warning照片
    path('dashboard/warning', views.warning_picture),
    path('dashboard/remove', views.remove_warning),


    # 结束考试，上传数据至database
    path('dashboard/finish', views.finish),
    # 分析考试数据
    path('dashboard/analysis', views.analysis),
    # 分析学生平均分
    path('dashboard/overall', views.overall),


    # 将拍的图存在Faces/username/Client文件夹
    path('dashboard/set', views.setFace),
    # 检查Client里是否有100张图 如果小于100清空文件夹
    path('dashboard/check', views.check),
    # 训练模型
    path('dashboard/train', views.trainModel),
    # 识别图片
    path('dashboard/rec', views.recImg),
    # 表情识别
    path('dashboard/emotion', views.emotion),
    # 检查是否可以下一题
    path('dashboard/next', views.next),

    # 处理PYTHON代码
    path('dashboard/ide', views.ide),

    # 删除全部数据
    path('dashboard/delUser', views.delAllUser),
    path('dashboard/delAdmin', views.delAllAdmin),
    path('dashboard/delWarning', views.delAllWarning),
    path('dashboard/delEmotion', views.delAllEmotion),
    path('dashboard/delPic', views.delAllPic),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 47811160+FuZixin@users.noreply.github.com