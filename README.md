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


#4.3 新增：
1. 所有POST方法返回值以HttpResponse的形式返回(所有方法基本都是POST)
2. 更新了东哥的2.0算法，原理比较复杂建议语音说
3. 增加了dashboard/set方法，需要传username和图片（多张），可以将该用户的照片存在Faces文件夹下，以便训练该用户模型
4. 增加了dashboard/train dashboard/rec方法，用来训练模型并返回预测结果

#基本流程：
1.用户注册时前端拍10张照片，发给后端
2.把用户的10张照片存在Faces文件夹的顶部(文件名必须 0.jpg,1.jpg,...)
3.训练该用户的模型
4.用户答题时拍照片，运行predict函数，返回准确度







