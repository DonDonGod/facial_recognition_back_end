from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
import os
import json
import shutil

from webApp.models import USER
from webApp.models import ADMIN
from webApp.models import EMOTION
from webApp.models import WARNING
from webApp.models import WARNING_PIC
from webApp.models import WARNING_LIST

from webApp.face_recognize_controller import face_predict
from webApp.face_recognize_controller import face_train
from webApp.face_deal import deal_face
from webApp.emotion_detect import emotion_predict

import subprocess
from django.views.decorators.csrf import csrf_exempt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = BASE_DIR.replace('\\', '/')
# warning_list = []

# Create your views here.
def homePage(request):
    return render(request, 'homepage.html')

def dashboard(request):
    return render(request, 'dashboard.html')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Add a user
def addUser(request):
    if request.method == 'POST':
        b = request.POST.get('username', None)
        c = request.POST.get('password', None)
        d = request.POST.get('student_number', None)
        USER.objects.create(username=b, password=c, student_number=d)
        return HttpResponse("Successful add user")
    else:
        return redirect('http://118.178.254.65')


def addAdmin(request):
    if request.method == 'POST':
        b = request.POST.get('username', None)
        c = request.POST.get('password', None)
        ADMIN.objects.create(username=b, password=c)
        return HttpResponse("Successful add admin")
    else:
        return redirect('http://118.178.254.65')


def modifyUser(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    exist = USER.objects.filter(student_number=username)
    if exist:
        user = USER.objects.get(student_number=username)
        user.password = password
        user.save()
        return HttpResponse("modification complete: ", username)
    else:
        return HttpResponse("The user does not exist")


def deleteUser(request):
    username = request.POST.get('username', None)
    exist = USER.objects.filter(student_number=username)
    if exist:
        user = USER.objects.get(student_number=username)
        user.delete()
        return HttpResponse("deletion complete")
    else:
        return HttpResponse("The user does not exist")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Login
def login(request):
    if request.method == 'POST':
        admin = request.POST.get('admin', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if admin == '0':
            exist = USER.objects.filter(student_number=username)
            if exist:
                user = USER.objects.get(student_number=username)
                p = user.password
                if password == p:
                    path = os.path.join(BASE_DIR, 'webApp/trained_model', username, 'trained_model.h5').replace('\\', '/')
                    if os.path.exists(path):
                        return HttpResponse('Login successfully with model')
                    else:
                        return HttpResponse('Login successfully without model')
                else:
                    return HttpResponse('Wrong username or password')
            else:
                return HttpResponse('The user does not exist')
        if admin == '1':
            exist = ADMIN.objects.filter(username=username)
            if exist:
                admin = ADMIN.objects.get(username=username)
                p = admin.password
                if password == p:
                    return HttpResponse('Login successfully')
                else:
                    return HttpResponse('Wrong username or password')
            else:
                return HttpResponse('The admin does not exist')
    else:
        return redirect('http://118.178.254.65')


# Return all student information
def student_list(request):
    if request.method == 'POST':
        data = {}
        index = 0
        students = USER.objects.all()
        for student in students:
            data1 = {}
            exist = WARNING.objects.filter(student_number=student.student_number)
            if exist:
                w = WARNING.objects.get(student_number=student.student_number)
                data1['name'] = student.username
                data1['student_number'] = student.student_number
                data1['warning_times'] = w.times
                data1['warning_score'] = w.score
            else:
                data1['name'] = student.username
                data1['student_number'] = student.student_number
                data1['warning_times'] = 'No Warning Data'
                data1['warning_score'] = 'No Warning Data'
            data[index] = data1
            index += 1
        return JsonResponse(data)
    else:
        return redirect('http://118.178.254.65')


def student_info(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        exist = USER.objects.filter(student_number=username)
        data1 = {}
        if exist:
            # Use this for cloud deployment
            # p = os.path.join('facial_recognition/webApp/trained_model', username, 'plt.png').replace('\\', '/')
            # p = 'http://118.178.254.65/' + p

            # Use this local test
            p = os.path.join(BASE_DIR, 'webApp/trained_model', username, 'plt.png').replace('\\', '/')

            student = USER.objects.get(student_number=username)
            data1['name'] = student.username
            data1['student_number'] = student.student_number
            data1['password'] = student.password
            data1['model_loss'] = student.model_loss
            data1['model_acc'] = student.model_acc
            data1['plt_url'] = p
        else:
            data1['name'] = 'The user does not exist'
            data1['student_number'] = 'The user does not exist'
            data1['password'] = 'The user does not exist'
            data1['model_loss'] = 'The user does not exist'
            data1['model_acc'] = 'The user does not exist'
            data1['plt_url'] = 'The user does not exist'
        return JsonResponse(data1)
    else:
        return redirect('http://118.178.254.65')


# Return the sample photo path
def original_picture(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        pic_path = os.path.join(BASE_DIR, 'webApp/Faces', username, 'Client').replace('\\', '/')
        all_list = os.listdir(pic_path)
        data = {}
        index = 0
        for i in all_list:
            if index < 10:
                # Use this for cloud deployment
                # p = os.path.join('facial_recognition/webApp/Faces', username, 'Client', i).replace('\\', '/')
                # p = 'http://118.178.254.65/' + p

                # Use this for local test
                p = os.path.join(BASE_DIR, 'webApp/Faces', username, 'Client', i).replace('\\', '/')
                data[index] = p
                index += 1
            else:
                break
        return JsonResponse(data)
    else:
        return redirect('http://118.178.254.65')


def exam_result(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        exist1 = EMOTION.objects.filter(student_number=username)
        data1 = {}
        if exist1:
            for i in [0, 1, 2, 3, 4]:
                data2 = {}
                exist = EMOTION.objects.filter(student_number=username, question=i)
                if exist:
                    result = EMOTION.objects.get(student_number=username, question=i)
                    data2['result'] = result.result
                    data2['emotion'] = result.emotion
                    name = result.pic_name
                    p = os.path.join('facial_recognition/media/emotion_predict', username, name).replace('\\', '/')
                    p = 'http://118.178.254.65/' + p
                    data2['url'] = p
                    data2['emotion_acc'] = result.acc
                else:
                    data2['result'] = "No exam record"
                    data2['emotion'] = "No exam record"
                    data2['url'] = "No exam record"
                    data2['emotion_acc'] = "No exam record"
                data1[i] = data2
        else:
            for i in [0, 1, 2, 3, 4]:
                data2 = {}
                data2['result'] = "The user does not exist"
                data2['emotion'] = "The user does not exist"
                data2['url'] = "The user does not exist"
                data2['emotion_acc'] = "The user does not exist"
                data1[i] = data2
        return JsonResponse(data1)
    else:
        return redirect('http://118.178.254.65')


def analysis(request):
    if request.method == 'POST':
        data1 = {}
        for i in [0, 1, 2, 3, 4]:
            data2 = {}
            true = EMOTION.objects.filter(result='true', question=i).count()
            false = EMOTION.objects.filter(result='false', question=i).count()
            acc = true/(true+false)
            data2['correct'] = str(round(acc, 2)*100) + '%'

            happy = EMOTION.objects.filter(emotion='happy', question=i).count()
            neutral = EMOTION.objects.filter(emotion='neutral', question=i).count()
            angry = EMOTION.objects.filter(emotion='angry', question=i).count()
            sad = EMOTION.objects.filter(emotion='sad', question=i).count()
            fear = EMOTION.objects.filter(emotion='fear', question=i).count()
            disgust = EMOTION.objects.filter(emotion='disgust', question=i).count()
            surprise = EMOTION.objects.filter(emotion='surprise', question=i).count()
            total = happy + neutral + angry + sad + fear + disgust + surprise
            data2['emotion_happy'] = str(round(happy/total, 4)*100) + '%'
            data2['emotion_neutral'] = str(round(neutral/total, 4)*100) + '%'
            data2['emotion_angry'] = str(round(angry/total, 4)*100) + '%'
            data2['emotion_sad'] = str(round(sad/total, 4)*100) + '%'
            data2['emotion_fear'] = str(round(fear/total, 4)*100) + '%'
            data2['emotion_disgust'] = str(round(disgust/total, 4)*100) + '%'
            data2['emotion_surprise'] = str(round(surprise/total, 4)*100) + '%'
            data1[i] = data2
        return JsonResponse(data1)
    else:
        return redirect('http://118.178.254.65')


def overall(request):
    if request.method == 'POST':
        data = {}
        total_user = USER.objects.all().count()
        attendance = EMOTION.objects.filter(question=0).count()
        true = EMOTION.objects.filter(result='true').count()
        average = str(round(true/(attendance*5), 4)*100) + '%'
        data["total_user"] = total_user
        data["attendance"] = attendance
        data["average_score"] = average
        return JsonResponse(data)
    else:
        return redirect('http://118.178.254.65')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Warning Algorithm
# Record warning times and warning score
def warning(flag, username):
    exist = WARNING_LIST.objects.filter(student_number=username)
    if exist:
        a = WARNING_LIST.objects.get(student_number=username)
        slist = list(a.list)
        if flag == 0:
            slist.append('0')
        elif flag == 1:
            slist.append('1')
        else:
            print('######False######')
        s = "".join(slist)
        a.list = s
        print(s)
        a.save()
    else:
        if flag == 0:
            WARNING_LIST.objects.create(student_number=username, list='0')
        if flag == 1:
            WARNING_LIST.objects.create(student_number=username, list='1')


# Calculate the warning scores
def warning_calculation(warn_photo_list):

    l = list(warn_photo_list)
    warn_photo_list = list(map(int, l))
    # print(warn_photo_list)

    score_total = 0
    warn_num = len(warn_photo_list)  # list总大小
    # print(warn_num)
    score_each = 1 / warn_num  # 每份得分
    priority = [2, 10, 20, 30, 50]  # 每种警告得分权重
    warn_sum_list = [0, 0, 0, 0, 0]
    warn_rank = 0
    ###读取数据
    for warn in warn_photo_list:  # 对每个warn
        if warn == 1:  # 如果没识别出人脸，则rank++
            if warn_rank < 5:  # 没到五级警告时
                warn_rank += 1
        else:  # 如果识别出人脸了
            if warn_rank != 0:  # 如果之前有rank，则对应rank计数器++
                warn_sum_list[warn_rank - 1] += 1
                warn_rank = 0
    if warn_rank != 0:  # 在最后如果还有rank
        warn_sum_list[warn_rank - 1] += 1
        warn_rank = 0
    # print(warn_sum_list)
    # warn_sum_list = [    0, 0, 0, 0, 1]  # 测试用例！！！！！！！
    ###计算分数
    for i in range(0, 5):
        score_total += warn_sum_list[i] * score_each * priority[i]  # 警告得分
        # print(score_total)
    if score_total > 1:
        score_total = 1
    return score_total  # 返回该学生有作弊嫌疑的可能性，有些情况下会大于100%
    # 当作弊嫌疑达到50%时，请人工查看拍摄图片


# Return the warning picture paths
def warning_picture(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        warning_path = os.path.join(BASE_DIR, 'media/test_predict', username, 'warning').replace('\\', '/')
        all_list = os.listdir(warning_path)
        data = {}
        index = 0
        for i in all_list:
            data1 = {}
            # Use this for cloud deployment
            # p = os.path.join('facial_recognition/media/test_predict', username, 'warning', i).replace('\\', '/')
            # p = 'http://118.178.254.65/' + p

            # Use this for local test
            p = os.path.join(BASE_DIR, 'media/test_predict', username, 'warning', i).replace('\\', '/')
            exist = WARNING_PIC.objects.filter(pic_name=i, student_number=username)
            if exist:
                pic = WARNING_PIC.objects.get(pic_name=i, student_number=username)
                if pic.state == "not pass":
                    data1['pic_name'] = i
                    data1['url'] = p
                    data1['acc'] = float(pic.acc)
                    data1['state'] = pic.state
                    data[index] = data1
                    index += 1
            # else:
            #     data1['url'] = 'No warning pics'
            #     data1['acc'] = 0.010101
            #     index += 1
        return JsonResponse(data)
    else:
        return redirect('http://118.178.254.65')


# Pass the OK pictures
def remove_warning(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        pic_name = request.POST.get('pic_name', None)
        index = request.POST.get('index', None)
        # 删除照片本体
        # p = os.path.join('facial_recognition/media/test_predict', username, 'warning', pic_name).replace('\\', '/')
        # p = 'http://118.178.254.65/' + p
        # p = os.path.join(BASE_DIR, 'media/test_predict', username, 'warning', pic_name).replace('\\', '/')
        # os.remove(p)

        # 将照片的状态变成pass
        exist2 = WARNING_PIC.objects.filter(student_number=username, pic_name=pic_name)
        if exist2:
            w = WARNING_PIC.objects.get(student_number=username, pic_name=pic_name)
            w.state = 'pass'
            w.save()
        else:
            print('0')

        # 修改warning_list, 重新算分
        exist1 = WARNING_LIST.objects.filter(student_number=username)
        if exist1:
            a = WARNING_LIST.objects.get(student_number=username)
            wlist = a.list
            l = list(wlist)
            warn_list = list(map(int, l))
            count = 0
            x = 0
            for i in warn_list:
                if i == 1:
                    count = count+1
                    if count == int(index):
                        break
                x = x+1
            warn_list[x] = 0
            tmp = list(map(str, warn_list))
            s = "".join(tmp)
            a.list = s
            a.save()
            score = warning_calculation(a.list)
            # 重新计算分数并上传
            exist = WARNING.objects.filter(student_number=username)
            if exist:
                student = WARNING.objects.get(student_number=username)
                time = student.times
                time = time - 1
                student.times = time
                student.score = score
                student.save()
            else:
                print('3')
            return HttpResponse('Remove successfully')
            # return JsonResponse(data)
        else:
            return HttpResponse('The user does not exist')
    else:
        return redirect('http://118.178.254.65')


# Check if the data is entered before the next question
def next(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        question = request.POST.get('question', None)
        exist = EMOTION.objects.filter(student_number=username, question=question)
        if exist:
            return HttpResponse("1")
        else:
            return HttpResponse("0")

    else:
        return redirect('http://118.178.254.65')


# End the exam and upload the information
def finish(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        # 东哥算法放这里
        path = os.path.join(BASE_DIR, 'media/test_predict', username, 'warning').replace('\\', '/')
        all_list = os.listdir(path)

        exist2 = WARNING_LIST.objects.filter(student_number=username)
        if exist2:
            a = WARNING_LIST.objects.get(student_number=username)
            times = len(all_list)
            score = warning_calculation(a.list)
        else:
            times = len(all_list)
            score = 1
        print('times: ', times)
        print('score: ', score)
        # 上传数据库
        exist = WARNING.objects.filter(student_number=username)
        if exist:
            student = WARNING.objects.get(student_number=username)
            student.times = times
            student.score = score
            student.save()
        else:
            WARNING.objects.create(student_number=username, times=times, score=score)
        # # 清空warning_list
        # exist1 = WARNING_LIST.objects.filter(student_number=username)
        # if exist1:
        #     a = WARNING_LIST.objects.get(student_number=username)
        #     a.list = '0'
        #     a.save()
        # warning_list.clear()
        return HttpResponse("upload warning_list successfully")
    else:
        return redirect('http://118.178.254.65')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Recognition Algorithm
# 将img里的图片根据username移动到Faces文件夹里(东哥算法)
def setFace(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('face', None)
        username = request.POST.get('username', None)
        username1 = file_obj.name

        userface = os.path.join(BASE_DIR, 'webApp/Faces/',username).replace('\\', '/')
        otherpath = os.path.join(BASE_DIR, 'webApp/Faces/',username, 'Other').replace('\\', '/')
        clientpath = os.path.join(BASE_DIR, 'webApp/Faces/',username, 'Client').replace('\\', '/')
        copypath = os.path.join(BASE_DIR, 'webApp/Other').replace('\\', '/')

        # 第一次注册，创建该用户文件夹
        if not os.path.exists(userface):
            os.mkdir(userface)
            os.mkdir(otherpath)
            os.mkdir(clientpath)
            # 把Other复制进来
            all_list = os.listdir(copypath)
            for i in all_list:
                a = os.path.join(BASE_DIR, 'webApp/Other',i).replace('\\', '/')
                b = os.path.join(BASE_DIR, 'webApp/Faces/',username, 'Other',i).replace('\\', '/')
                shutil.copyfile(a,b)

        # 将照片写入Client
        file = os.path.join(BASE_DIR, 'webApp/Faces/', username, 'Client/', username1).replace('\\', '/')
        with open(file, 'wb+') as f:
            f.write(file_obj.read())
            # 检测是否是人脸
            flag = deal_face(file, file)
        # 没有人别出人脸将其删除 (1:成功识别人脸; 0:未检测出人脸)
        if flag == 0:
            os.remove(file)

        if username1 == "99.jpg":
            if check(username) == 0:
                return HttpResponse("Restart")
            elif check(username) == 100:
                return HttpResponse(100)

        elif username1 != "99.jpg":
            # 返回当前Client文件夹下有多少张有效图片
            list = os.listdir(clientpath)
            size = len(list)
            return HttpResponse(size)


# Check if there are 100 photos in the Client folder. If less than 100, clear the folder
def check(username):
    clientpath = os.path.join(BASE_DIR, 'webApp/Faces/', username, 'Client').replace('\\', '/')
    all_list = os.listdir(clientpath)
    size = len(all_list)
    if size < 100:
        for i in all_list:
            file = os.path.join(BASE_DIR, 'webApp/Faces/', username, 'Client/', i).replace('\\', '/')
            os.remove(file)
        return 0
    else:
        print("100 good pictures")
        return 100


# Train the model
def trainModel(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        face_path = os.path.join(BASE_DIR, 'webApp/Faces',username).replace('\\', '/')
        model_path = os.path.join(BASE_DIR, 'webApp/trained_model',username).replace('\\', '/')
        if not os.path.exists(model_path):
            os.mkdir(model_path)
        loss, acc = face_train(face_path, 100, model_path, username)

        exist = USER.objects.filter(student_number=username)
        if exist:
            a = USER.objects.get(student_number=username)
            a.model_loss = loss
            a.model_acc = acc
            a.save()
        return HttpResponse("train successfully")
    else:
        return redirect('http://118.178.254.65')


# Facial recognition algorithm
def recImg(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('face', None)
        username = request.POST.get('username', None)
        username1 = file_obj.name
        a = os.path.join(BASE_DIR, 'media/test_origin', username).replace('\\', '/')
        b = os.path.join(BASE_DIR, 'media/test_predict', username).replace('\\', '/')
        warning_path = os.path.join(BASE_DIR, 'media/test_predict', username, 'warning').replace('\\', '/')
        warning_path1 = os.path.join(BASE_DIR, 'media/test_predict', username, 'warning', username1).replace('\\', '/')
        all_path = os.path.join(BASE_DIR, 'media/test_predict', username, 'all').replace('\\', '/')
        all_path1 = os.path.join(BASE_DIR, 'media/test_predict', username, 'all', username1).replace('\\', '/')
        origin_path = os.path.join(BASE_DIR, 'media/test_origin', username, username1).replace('\\', '/')
        if not os.path.exists(a):
            os.mkdir(a)
        if not os.path.exists(b):
            os.mkdir(b)
        if not os.path.exists(warning_path):
            os.mkdir(warning_path)
        if not os.path.exists(all_path):
            os.mkdir(all_path)

        with open(origin_path, 'wb+') as f:
            f.write(file_obj.read())
        face_path = os.path.join(BASE_DIR, 'webApp/Faces',username).replace('\\', '/')
        model_path = os.path.join(BASE_DIR, 'webApp/trained_model',username,'trained_model.h5').replace('\\', '/')
        acc = face_predict(model_path, face_path, origin_path, all_path1)

        if acc < 0.5:
            shutil.copyfile(all_path1, warning_path1)
            WARNING_PIC.objects.create(student_number=username, pic_name=username1, acc=acc, state='not pass')
            flag = 1
        else:
            flag = 0
        warning(flag, username)
        # print(warning_list)
        return HttpResponse(acc)
    else:
        return redirect('http://118.178.254.65')


# Emotion recognition algorithm
def emotion(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        question = request.POST.get('question', None)
        result = request.POST.get('result', None)
        file_obj = request.FILES.get('face', None)
        username1 = file_obj.name
        a = os.path.join(BASE_DIR, 'media/emotion_origin', username).replace('\\', '/')
        b = os.path.join(BASE_DIR, 'media/emotion_predict', username).replace('\\', '/')
        if not os.path.exists(a):
            os.mkdir(a)
        if not os.path.exists(b):
            os.mkdir(b)
        old_path = os.path.join(BASE_DIR, 'media/emotion_origin', username, username1).replace('\\', '/')
        new_path = os.path.join(BASE_DIR, 'media/emotion_predict', username, username1).replace('\\', '/')
        with open(old_path, 'wb+') as f:
            f.write(file_obj.read())

        model_path = os.path.join(BASE_DIR, 'webApp/trained_model/emotion_model.h5').replace('\\', '/')
        type, acc = emotion_predict(model_path, old_path, new_path)
        acc = float(acc)

        exist = EMOTION.objects.filter(student_number=username, question=question)

        if type == -1:
            data = {'type':'No faces detected', 'acc': acc}
            os.remove(old_path)
            os.remove(new_path)
            return JsonResponse(data)
        if type == 0:
            if exist:
                a = EMOTION.objects.get(student_number=username, question=question)
                a.emotion = 'angry'
                a.acc = acc
                a.pic_name = username1
                a.result = result
                a.save()
                data = {'type': 'angry', 'acc': acc, 'pic_name': username1}
                return JsonResponse(data)
            else:
                data = {'type': 'angry', 'acc': acc}
                EMOTION.objects.create(question=question, student_number=username, emotion='angry', result=result, pic_name=username1, acc=acc)
                return JsonResponse(data)
        if type == 1:
            if exist:
                a = EMOTION.objects.get(student_number=username, question=question)
                a.emotion = 'disgust'
                a.acc = acc
                a.pic_name = username1
                a.result = result
                a.save()
                data = {'type': 'disgust', 'acc': acc}
                return JsonResponse(data)
            else:
                data = {'type': 'disgust', 'acc': acc, 'pic_name': username1}
                EMOTION.objects.create(question=question, student_number=username, emotion='disgust', result=result, pic_name=username1, acc=acc)
                return JsonResponse(data)
        if type == 2:
            if exist:
                a = EMOTION.objects.get(student_number=username, question=question)
                a.emotion = 'fear'
                a.acc = acc
                a.pic_name = username1
                a.result = result
                a.save()
                data = {'type': 'fear', 'acc': acc, 'pic_name': username1}
                return JsonResponse(data)
            else:
                data = {'type': 'fear', 'acc': acc}
                EMOTION.objects.create(question=question, student_number=username, emotion='fear', result=result, pic_name=username1, acc=acc)
                return JsonResponse(data)
        if type == 3:
            if exist:
                a = EMOTION.objects.get(student_number=username, question=question)
                a.emotion = 'happy'
                a.acc = acc
                a.pic_name = username1
                a.result = result
                a.save()
                data = {'type': 'happy', 'acc': acc, 'pic_name': username1}
                return JsonResponse(data)
            else:
                data = {'type': 'happy', 'acc': acc}
                EMOTION.objects.create(question=question, student_number=username, emotion='happy', result=result, pic_name=username1, acc=acc)
                return JsonResponse(data)
        if type == 4:
            if exist:
                a = EMOTION.objects.get(student_number=username, question=question)
                a.emotion = 'sad'
                a.acc = acc
                a.pic_name = username1
                a.result = result
                a.save()
                data = {'type': 'sad', 'acc': acc, 'pic_name': username1}
                return JsonResponse(data)
            else:
                data = {'type': 'sad', 'acc': acc}
                EMOTION.objects.create(question=question, student_number=username, emotion='sad', result=result, pic_name=username1, acc=acc)
                return JsonResponse(data)
        if type == 5:
            if exist:
                a = EMOTION.objects.get(student_number=username, question=question)
                a.emotion = 'surprise'
                a.acc = acc
                a.pic_name = username1
                a.result = result
                a.save()
                data = {'type': 'surprise', 'acc': acc, 'pic_name': username1}
                return JsonResponse(data)
            else:
                data = {'type': 'surprise', 'acc': acc}
                EMOTION.objects.create(question=question, student_number=username, emotion='surprise', result=result, pic_name=username1, acc=acc)
                return JsonResponse(data)
        if type == 6:
            if exist:
                a = EMOTION.objects.get(student_number=username, question=question)
                a.emotion = 'neutral'
                a.acc = acc
                a.pic_name = username1
                a.result = result
                a.save()
                data = {'type': 'neutral', 'acc': acc, 'pic_name': username1}
                return JsonResponse(data)
            else:
                data = {'type': 'neutral', 'acc': acc}
                EMOTION.objects.create(question=question, student_number=username, emotion='neutral', result=result, pic_name=username1, acc=acc)
                return JsonResponse(data)
    else:
        return redirect('http://118.178.254.65')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# IDE
def run_code(code):
    try:
        output = subprocess.check_output(['python', '-c', code],
                                         universal_newlines=True,
                                         stderr=subprocess.STDOUT,
                                         timeout=30)
    except subprocess.CalledProcessError as e:
        output = e.output
    except subprocess.TimeoutExpired as e:
        output = '\r\n'.join(['Time Out!!!', e.output])
    return output


def ide(request):
    if request.method == 'POST':
        code = request.POST.get('code', None)
        output = run_code(code)
        return HttpResponse(output)
    else:
        return redirect('http://118.178.254.65')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Clear the tables in the database
def delAllUser(request):
    USER.objects.all().delete()
    return HttpResponse('All users are deleted')
def delAllAdmin(request):
    ADMIN.objects.all().delete()
    return HttpResponse('All admins are deleted')
def delAllWarning(request):
    WARNING.objects.all().delete()
    return HttpResponse('All warnings are deleted')
def delAllEmotion(request):
    EMOTION.objects.all().delete()
    return HttpResponse('All emotions are deleted')
def delAllPic(request):
    WARNING_PIC.objects.all().delete()
    return HttpResponse('All pics are deleted')

