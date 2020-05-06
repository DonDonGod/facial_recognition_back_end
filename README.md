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
#5.6 新增：
1.百分号的问题我给你改了
2.WARNING_PIC表新增state, 用来表示该照片是否通过了人工审查，没通过是not pass, 通过了是pass, 以后就不会出现在返回给前端的warning图片中(本来想着把通过了图片直接删了, 但是好像出于安全不让删, 搞到4点么办法只能想到这么解决了, 因为改了model记得本地测试运行两行代码)<br>
3.[dashboard/warning]： 参量(username学号)；返回warning图片,准确度,图片名称,状态（新增1.返回pic_name, 方便在remove时调用，不用显示出来; 2.state用于判断是否返回这张图，如果是pass就不返回了，调用下面接口就会把state从not pass 变成pass）<br>
4.[dashboard/remove]: 参量(username学号, index删的表中第几个图(第一张就是1，第二张就是2，注意删了第一张后刷新一下这张图就不显示了，所以原来的第二张就变成了第一张), pic_name删除图片的名字(在上一步帮你返回了, 这里拿出来用)); 移除没问题的照片并重新算分上传(后端本地照片并不能直接删，移除只是代表我不返回给你这张图的路径而已，所以要上面两步)<br>
5.新增返回参考人数和学生平均分方法，可以放在analysis页下面[dashboard/overall]: 无参量<br>
6.拍不够100张照片的方法我想了想, 最省事的是你写个restart按钮, 在底下写一句话: 如果等待超过30s没反应就点restart, 这个按钮调用[dashboard/check]: 参量(username学号)<br>

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
150, 186, 335







