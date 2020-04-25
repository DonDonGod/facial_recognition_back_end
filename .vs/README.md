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
#4.25 新增：
1.warning计数与分数计算<br>
2.返回全部学生信息 [dashboard/student_list]<br>
3.结束考试，上传数据warning至database [dashboard/finish]<br>
4.emotion算法改动 [dashboard/emotion]: 需要4个参量(question题目序号，username学号，result答题对错， face拍的照片)
5.返回warning图片 [dashboard/warning]: 参量(username学号)
6.强烈建议上传100张片，训练模型，考试拍照时传到后端的username用学号而不是姓名，以免重名

-----
#基本流程：
1.用户注册时自动拍100张照片 存在Faces里对应用户名的Client文件夹下<br>
2.训练该用户模型存在trained_model里对应用户文件夹下<br>
3.每隔一段时间拍照进行预测，返回准确度<br>
4.用户运行代码后进行一次拍照，进行表情识别<br>

1.900s考试10s一张，一共90张<br>
2.准确度50以下为warning， 连续warning提升等级，所有warning照片都存<br>
3.写一个计数器函数存warninglist,考试结束上传数据库<br>
4.表情识别：点nextpage比对结果并拍照并存表<br>
5.EMOTION表（question，student_number，emotion，result）<br>
6.USER表 (username，student_number，password）<br>
7.ADMIN表（username，password）<br>
8.WARNING表（student_number，times, score）<br>







