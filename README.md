#1.主项目目录下settings.py
DATABASES = {}
改成自己的本地数据库

#2.安装pymysql
pip install pymysql

#3.主目录下_init_.py添加
import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

#4.命令行cd到项目目录下执行：
python manage.py makemigrations
python manage.py migrate

图片还不是字节流，但是已经把sqlite数据库换成本地MYSQL了

