<<<<<<< HEAD
import time
import requests
import flask
import threading
from flask import Flask,render_template,request
from function import login,erji,pingjiao,connect


app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def index():
    '''主页的视图函数'''
    if request.method == 'GET':
        # try:
            # use_times=r.get("use_times").decode()
        # except Exception as e:
            # print(e)
        #return render_template("index.html",use_times=use_times)
        return render_template("index.html")
    else:
        username=request.form.get("username")
        password=request.form.get("password")
        if username=='' or password=='':
            return "请输入学号或密码"
        
        s=login(username,password)
        if s=='fail':
            return "<h1>账号或密码错误！</h1>"
        #多线程评教评教的过程
        thread_ping=threading.Thread(target=pingjiao,args=(s,))
        thread_ping.start()
        # pingjiao(s)

        return '<h1>评价成功！</h1> \n <h2> <a href="http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fbkjw.chd.edu.cn%2Feams%2Fhome.action%3Bjsessionid%3D3ECA527C2DF78DA0D88DB231959FF11D">教务链接</a></h2>'


@app.route('/feedback/',methods=["POST","GET"])
def feedback():
    if request.method == 'GET':
        return render_template("feedback.html")
    else:
        feedback_content=request.form.get("feedback_content")
        if feedback_content=="":
            return"<h1>请输入内容！</h1>"
        with open("反馈建议.txt","a+")as fp:
            fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"   "+feedback_content+"\n\n")
        #r.lpush('feedback',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"   "+feedback_content)
        return "<h1>提交成功</h1>"
     
     
@app.route('/test_connect/',methods=["POST","GET"])        
def test_connect():
    result=connect()
    if result==True:
        return "<h1>连接成功</h1>"
    else:
        return "<h1>连接失败</h1>"

    

if __name__=="__main__":
    app.run(host='0.0.0.0',port=82, threaded = True)
    
    
=======
import time
import requests
import flask
import threading
from flask import Flask,render_template,request
from function import login,erji,pingjiao,connect


app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def index():
    '''主页的视图函数'''
    if request.method == 'GET':
        # try:
            # use_times=r.get("use_times").decode()
        # except Exception as e:
            # print(e)
        #return render_template("index.html",use_times=use_times)
        return render_template("index.html")
    else:
        username=request.form.get("username")
        password=request.form.get("password")
        if username=='' or password=='':
            return "请输入学号或密码"
        
        s=login(username,password)
        if s=='fail':
            return "<h1>账号或密码错误！</h1>"
        #多线程评教评教的过程
        thread_ping=threading.Thread(target=pingjiao,args=(s,))
        thread_ping.start()
        # pingjiao(s)

        return '<h1>评价成功！</h1> \n <h2> <a href="http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fbkjw.chd.edu.cn%2Feams%2Fhome.action%3Bjsessionid%3D3ECA527C2DF78DA0D88DB231959FF11D">教务链接</a></h2>'


@app.route('/feedback/',methods=["POST","GET"])
def feedback():
    if request.method == 'GET':
        return render_template("feedback.html")
    else:
        feedback_content=request.form.get("feedback_content")
        if feedback_content=="":
            return"<h1>请输入内容！</h1>"
        with open("反馈建议.txt","a+")as fp:
            fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"   "+feedback_content+"\n\n")
        #r.lpush('feedback',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"   "+feedback_content)
        return "<h1>提交成功</h1>"
     
     
@app.route('/test_connect/',methods=["POST","GET"])        
def test_connect():
    result=connect()
    if result==True:
        return "<h1>连接成功</h1>"
    else:
        return "<h1>连接失败</h1>"

    

if __name__=="__main__":
    app.run(host='0.0.0.0',port=82, threaded = True)
    
    
>>>>>>> b9b1d3beb40675aaf2210094740247461b083098
    