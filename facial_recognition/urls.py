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
    path('login/', views.login),

    path('dashboard/', views.dashboard),
    path('dashboard/add_user', views.addUser),

    path('homepage/upload', views.uploadImg),
    path('dashboard/show', views.showImg),

    path('dashboard/delUser', views.delUser),
    path('dashboard/delImg', views.delImg),



    # test
    # path('calpage/', views.calPage),
    # path('cal', views.calculate),
    # path('callist/',views.calList),
    # path('callist/del', views.deldata)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 47811160+FuZixin@users.noreply.github.com