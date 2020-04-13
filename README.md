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


#4.13 新增：
1.更新算法
2.setFace算法用户上传100张照片时，照片有效返回1，未检测出人脸返回0


#基本流程：
1.用户注册时自动拍100张照片 存在Faces里对应用户名的Client文件夹下
2.训练该用户模型存在trained_model里对应用户文件夹下
3.每隔一段时间拍照进行预测，返回准确度







