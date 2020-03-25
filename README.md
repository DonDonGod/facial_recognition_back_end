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

##每次修改models.py都要执行这步
#4.1. 命令行cd到项目目录下执行：
python manage.py makemigrations
#4.2. 命令行cd到项目目录下执行：
python manage.py migrate

#根目录下media/img储存上传的图片； media/new_img储存识别后的图片
#先在homepage上传图片， 然后去dashborad查看，最后点recognize，可以发现media/new_img里有了识别后的图片

#问题：删库只能删图片的url路由，想删本地media里的图必须手动删





