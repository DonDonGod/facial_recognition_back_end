###Introduction
Welcome to use the facial recognition test system. You need to pay attention. This is the version used by our team for local testing.<br> 
The front-end and back-end systems should be placed on the same computer and the environment should be configured.<br>
Please visit http://118.178.254.65/ for the cloud version.<br>
Before running the front end to access our web pages, you need to start the back end first.<br>
-----
###Environment
Our backend is written in Python3, so make sure that your computer has a Python3 environment (Python 3.7.2 is recommended).<br>
At the same time, you need to update your "pip" to the latest version: [python -m pip install --upgrade pip]<br>
You also need to install MySQL in advance, the version we use is 5.7
-----
###Install
1. Install "pymysql": [pip install pymysql]<br>
2. Install "TensorFlow": [pip install tensorflow]<br>
3. Install "OpenCV": [pip install opencv-python]<br>
-----
###Configuration
1. facial_recognition/facial_recognition/settings.py, line 90 (DATABASES = {}) Change the parameters to your computer's local database<br>
2. In the terminal, cd to the root directory of the project: [python manage.py makemigrations]<br>
3. In the terminal, cd to the root directory of the project: [python manage.py migrate]
-----
###If you are using a Mac
face_recognition/face_recognize_controller.py, line 215: [predicted_photo, predict_name_accuracy = detect_face(predict_photo, model, names, 1)]

-----
###Start up
In the terminal, cd to the root directory of the project: [python manage.py runserver]

-----
###If you want to start the backend in the cloud server
1. Enter BT dashboard（http://118.178.254.65:8888/666666, username: facial, password: zl19980413.）<br>
2. facial_recognition/webApp/views.py, line 156, 192, 364: change the path<br>
3. Enter the virtual environment: [source /www/wwwroot/backend/facial_recognition/backend_venv/bin/activate]<br>
4. Enter the project directory: [cd /www/wwwroot/backend/facial_recognition]<br>
5. Start: [python manage.py runserver 0:8000]<br>
6. Non-stop start: [nohup python manage.py runserver 0:8000 &]<br>
7. Stop non-stop:[lsof -i:8000] find the processID; [kill -9 processID]
-----
###Photo storage
1. 100 photos taken during user registration: facial_recognition/webApp/Faces/studentID <br>
2. Original pictures taken during the exam: facial_recognition/media/test_origin/studentID <br>
3. Predicted pictures of facial recognition: facial_recognition/media/test_predict/studentID <br>
4. Original snapshots when the student see the running log: facial_recognition/media/emotion_origin/studentID <br>
4. Predicted pictures of emotion recognition: facial_recognition/media/emotion_predict/studentID <br>
-----









