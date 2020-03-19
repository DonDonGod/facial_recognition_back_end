# facial_recognition_back_end

后端接口：\n

登录——\n
请求：\n
{\n
    username:"", //String\n
    password:""  //String\n
}\n
返回：\n
{\n
    code:100 //100为成功，200为用户名不存在，300为密码错误\n
}\n

注册——\n
请求：\n
{\n
    username:"", //String\n
    password:""  //String\n
}\n
返回：\n
{\n
    code:100 //100为成功，200为用户名已经存在\n
}\n

传照片——\n
请求：\n
{\n
    username:"", //String\n
    photo:...    //byte[]（应该是byte[]）\n
}\n
返回：\n
{\n
    code:100 //100为成功，200莫名其妙的错误\n
}\n
