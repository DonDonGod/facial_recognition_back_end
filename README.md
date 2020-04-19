#安装
1.安装pymysql
pip install pymysql<br>
2.主目录下_init_.py添加<br>
import pymysql<br>
pymysql.version_info = (1, 3, 13, "final", 0)<br>
pymysql.install_as_MySQLdb()<br>

-----
#启动
1.主项目目录下settings.py中DATABASES = {}改成自己的本地数据库
2.如果mysql报timezone的错：set global time_zone='+8:00';
3.启动：python manage.py runserver

###每次修改models.py后都要执行这步
4.1. 命令行cd到项目目录下执行：python manage.py makemigrations
<br>
4.2. 命令行cd到项目目录下执行：python manage.py migrate

-----
#苹果电脑
1.face_recognize_controller.py 206行 predicted_photo, predict_name_accuracy = detect_face(predict_photo, model, names, 1)<br>
2.face_recognize_controller.py 91-95行 删曲线图<br>
3.主项目目录下settings.py中DATABASES = {}改成自己的本地数据库<br>
4.（建议，方便测试）删webApps里Faces,trained_model,里的用户文件夹（别动emotion_model.h5）; 删除media中4个文件夹下的用户文件夹
-----
#4.19 新增：
1.表情识别算法 接口[dashboard/emotion] 参数[username, face(需要识别的图)] <br>
2.在线ide
-----
#基本流程：
1.用户注册时自动拍100张照片 存在Faces里对应用户名的Client文件夹下<br>
2.训练该用户模型存在trained_model里对应用户文件夹下<br>
3.每隔一段时间拍照进行预测，返回准确度<br>
4.用户运行代码后进行一次拍照，进行表情识别







