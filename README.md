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
#云端启动后端
1.Chrome浏览器修改（https://www.jianshu.com/p/751a9cb93a43）<br>
2.进入宝塔终端（http://118.178.254.65:8888/）<br>
3.进入虚拟环境: source /www/wwwroot/backend/facial_recognition/backend_venv/bin/activate<br>
4.进入项目目录: cd /www/wwwroot/backend/facial_recognition<br>
5.python manage.py runserver 0:8000<br>
6.永久运行 nohup python manage.py runserver 0:8000 &<br>
7.关闭永久运行 lsof -i:8000 找进程ID; kill -9 进程ID
-----
#5.11 新增：
1.张磊不用拉这版，上次我已经把改的代码微信发你了<br>
2.多线程启动失败，新增next[dashboard/next]:参量(username学号, question问题号)，判断上传是否成功，如果不成功要重新拍照，不能下一题<br>
3.emotion方法在同一题可以反复调用，用新的结果替换(反复点不会run报错)<br>
4.拍不够100张照片的方法还要解决<br>

-----
#基本流程：
1.用户注册时自动拍100张照片 存在Faces里对应用户名的Client文件夹下<br>
2.训练该用户模型存在trained_model里对应用户文件夹下<br>
3.每隔一段时间拍照进行预测，返回准确度<br>
4.用户运行代码后进行一次拍照，进行表情识别<br>
<br>
1.900s考试10s一张，一共90张<br>
2.准确度50以下为warning， 连续warning提升等级，所有warning照片都存<br>
3.写一个计数器函数存warninglist,考试结束上传数据库<br>
4.表情识别：点nextpage比对结果并拍照并存表<br>
5.EMOTION表（question，student_number，emotion，result, pic_name, acc）<br>
6.USER表 (username，student_number，password, model_loss, model_acc）<br>
7.ADMIN表（username，password）<br>
8.WARNING表（student_number，times, score）<br>
9.WARNING_PIC表（student_number, pic_name, acc, state）

#本地路径更改
152, 185, 354







