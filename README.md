# facial_recognition_back_end
  
后端接口：  
  
登录——  
请求：  
{  
    username:"", //String  
    password:""  //String  
}  
返回：  
{  
    code:100 //100为成功，200为用户名不存在，300为密码错误  
}  
  
注册——  
请求：  
{  
    username:"", //String  
    password:""  //String  
}  
返回：  
{  
    code:100 //100为成功，200为用户名已经存在  
}  
  
传照片——  
请求：  
{  
    username:"", //String  
    photo:...    //byte[]（应该是byte[]）  
}  
返回：  
{  
    code:100 //100为成功，200莫名其妙的错误  
}  
  
