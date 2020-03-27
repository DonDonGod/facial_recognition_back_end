##可选
#1.安装pymysql
pip install pymysql
#2.主目录下_init_.py添加
import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

##必选
#1.主项目目录下settings.py
DATABASES = {}
改成自己的本地数据库
#2.如果mysql报timezone的错：
set global time_zone='+8:00';
#3. 启动
python manage.py runserver

#每次修改models.py都要执行这步
#4.1. 命令行cd到项目目录下执行：
python manage.py makemigrations
#4.2. 命令行cd到项目目录下执行：
python manage.py migrate

#根目录下media/img储存上传的图片； media/new_img储存识别后的图片

#3.27 新增：
1. dashboard/find_user， dashboard/modify_user， dashboard/delete_user请求（POST） 用来对user数据库进行增删改查
2. 将图片识别方别写在了homepage/upload请求中, 这样每次上传图片时就自动进行识别，并将识别后的图片存到了media/new_img里，以免一次识别太多图片造成卡顿。详见views.uploadImg
3. dashboard/path请求（GET） 【访问http://127.0.0.1:8000/dashboard/path即可】 该请求会将识别完的图片以{图片名：路径}的方式存在rec_path字典中，并在终端print出来。详见views.showPath





