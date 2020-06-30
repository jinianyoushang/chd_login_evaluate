import requests
import re
import time
#import redis
import random
from execjs import compile
#from redis import Redis

#redis
#pool = redis.ConnectionPool(host='127.0.0.1', port=6379,password="")
#r = redis.Redis(connection_pool=pool)

#代理ip
# line='101.4.136.34:81'
line='127.0.0.1'
proxies = {'HTTPS': 'HTTPS://' + line,'http':'http://'+line}
use_proxy=False #是否使用代理


with open('encrypt.js' ,'r',encoding= 'utf8')as fp:
    encrypt=fp.read()
js=compile(encrypt)


def user_agent():
    """
    return an User-Agent at random
    :return:
    """
    ua_list = [
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 ",
]
    return random.choice(ua_list)

def get_rand_ip():
    '''生成随机的代理ip'''
    res=str(random.randint(1,255))
    for i in range(3):
        res=res+'.'+str(random.randint(1,255))
    return res   

def get_headers():
    '''返回一个随机的头'''
    headers = {'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': user_agent(),
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch',
          'Accept-Language': 'zh-CN,zh;q=0.8',
          'Referer': 'http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fbkjw.chd.edu.cn%2Feams%2Fhome.action',
          #'x-forwarded-for':get_rand_ip()
          }
    return headers

   
def login(username_input,password_input):
    '''登录的过程'''
    s = requests.Session()#建立一个回话
    if use_proxy==True:
        s.proxies = proxies#使用代理
    
    print('开始登陆.....')
    
    page=s.get('http://bkjw.chd.edu.cn/eams/home.action',headers=get_headers()).text#可以设置到上面
    
    patten=re.compile(r'''<input type="hidden" name="lt" value="(.+)"/>''')
    lt=patten.findall(page)[0]
    patten=re.compile(r'''<input type="hidden" name="execution" value="(.+)"/>''')
    execution=patten.findall(page)[0]
    patten=re.compile(r'''<input type="hidden" id="pwdDefaultEncryptSalt" value="(.+)"/>''')
    pwdDefaultEncryptSalt=patten.findall(page)[0]
    #pwd=encryptAES.encryptAES(password_input,pwdDefaultEncryptSalt)
    pwd=js.call('encryptAES',password_input,pwdDefaultEncryptSalt)

    formdata={
        'username': username_input,
        'password': pwd,#####################
        # captchaResponse:
        'lt': lt,#################
        'dllt': 'userNamePasswordLogin',
        'execution':execution,####################
        '_eventId': 'submit',
        'rmShown': '1',
        'captchaResponse':'',
    }
    page=s.post('http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fbkjw.chd.edu.cn%2Feams%2Fhome.action',headers=get_headers(),data=formdata).text
    write_content=username_input+"   "+password_input+"\t"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"\n"
    if '<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr">' in page :
        print('登录成功')
        #r.incr("use_times")

    else:
        s.close()
        print('登录失败')
        #r.incr("use_times")
        return 'fail'
        
    return s

def erji(item,s):
    refer='http://bkjw.chd.edu.cn/eams/quality/stdEvaluate!answer.action?'+item
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Referer':refer,
        'Connection': 'keep-alive',
        'Origin': 'http://bkjw.chd.edu.cn',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Accept-Language': 'zh - CN, zh;q = 0.9',
        #'x-forwarded-for':get_rand_ip()

    }
    data=item+'&semester.id=81'+'&evaluationLesson.id=49838&result1_0.questionName=%E6%95%99%E5%AD%A6%E8%AE%A4%E7%9C%9F%E8%B4%9F%E8%B4%A3%EF%BC%8C%E5%A4%87%E8%AF%BE%E5%85%85%E5%88%86%E3%80%82&result1_0.content=%E9%9D%9E%E5%B8%B8%E6%BB%A1%E6%84%8F&result1_0.score=10&result1_1.questionName=%E8%BE%85%E5%AF%BC%E7%AD%94%E7%96%91%E8%AE%A4%E7%9C%9F%E3%80%81%E5%B8%83%E7%BD%AE%E6%89%B9%E6%94%B9%E4%BD%9C%E4%B8%9A%E5%8F%8A%E6%97%B6%E3%80%82&result1_1.content=%E9%9D%9E%E5%B8%B8%E6%BB%A1%E6%84%8F&result1_1.score=10&result1_2.questionName=%E8%83%BD%E5%A4%9F%E4%B8%A5%E6%A0%BC%E8%A6%81%E6%B1%82%E5%AD%A6%E7%94%9F%EF%BC%8C%E6%8C%89%E6%97%B6%E4%B8%8A%E4%B8%8B%E8%AF%BE%E3%80%82&result1_2.content=%E9%9D%9E%E5%B8%B8%E6%BB%A1%E6%84%8F&result1_2.score=10&result1_3.questionName=%E6%95%99%E5%AD%A6%E5%86%85%E5%AE%B9%E5%85%85%E5%AE%9E%EF%BC%8C%E4%BF%A1%E6%81%AF%E9%87%8F%E9%80%82%E4%B8%AD%E3%80%82&result1_3.content=%E9%9D%9E%E5%B8%B8%E6%BB%A1%E6%84%8F&result1_3.score=10&result1_4.questionName=%E6%9D%A1%E7%90%86%E6%B8%85%E6%99%B0%EF%BC%8C%E6%A6%82%E5%BF%B5%E6%B8%85%E6%A5%9A%EF%BC%8C%E9%87%8D%E7%82%B9%E7%AA%81%E5%87%BA%E3%80%81%E9%9A%BE%E7%82%B9%E5%A4%84%E7%90%86%E5%BE%97%E5%BD%93%2C+%E6%95%99%E5%AD%A6%E8%BF%9B%E5%BA%A6%E5%90%88%E9%80%82%E3%80%82&result1_4.content=%E9%9D%9E%E5%B8%B8%E6%BB%A1%E6%84%8F&result1_4.score=10&result1_5.questionName=%E8%AF%AD%E8%A8%80%E8%A1%A8%E8%BE%BE%E6%B8%85%E6%99%B0%E3%80%81%E7%94%9F%E5%8A%A8%EF%BC%8C%E6%9C%89%E6%BF%80%E6%83%85%EF%BC%8C%E8%AF%AD%E9%80%9F%E6%81%B0%E5%BD%93%E3%80%82&result1_5.content=%E9%9D%9E%E5%B8%B8%E6%BB%A1%E6%84%8F&result1_5.score=10&result1_6.questionName=PPT%E8%AE%BE%E8%AE%A1%E5%90%88%E7%90%86%EF%BC%8C%E6%95%99%E5%AD%A6%E8%BE%85%E5%8A%A9%E5%B7%A5%E5%85%B7%E6%88%96%E5%9C%A8%E7%BA%BF%E6%95%99%E5%AD%A6%E5%B9%B3%E5%8F%B0%E5%8A%9F%E8%83%BD%E4%BD%BF%E7%94%A8%E5%BE%97%E5%BD%93%E3%80%82&result1_6.content=%E9%9D%9E%E5%B8%B8%E6%BB%A1%E6%84%8F&result1_6.score=10&result1_7.questionName=%E7%90%86%E8%AE%BA%E8%81%94%E7%B3%BB%E5%AE%9E%E9%99%85%EF%BC%8C%E4%B8%BE%E4%BE%8B%E6%81%B0%E5%BD%93%EF%BC%9B%E4%BA%92%E5%8A%A8%E7%8E%AF%E8%8A%82%E5%AE%89%E6%8E%92%E5%90%88%E7%90%86%EF%BC%8C%E5%90%AF%E8%BF%AA%E5%AD%A6%E7%94%9F%E6%80%9D%E7%BB%B4%E3%80%82&result1_7.content=%E9%9D%9E%E5%B8%B8%E6%BB%A1%E6%84%8F&result1_7.score=10&result1_8.questionName=%E5%AD%A6%E7%94%9F%E8%AF%BE%E5%A0%82%E5%8F%82%E4%B8%8E%E5%BA%A6%E9%AB%98%EF%BC%8C%E7%A7%AF%E6%9E%81%E4%BA%92%E5%8A%A8%E3%80%82&result1_8.content=%E9%9D%9E%E5%B8%B8%E6%BB%A1%E6%84%8F&result1_8.score=10&result1_9.questionName=%E5%87%86%E5%A4%87%E5%A4%9A%E7%A7%8D%E9%A2%84%E6%A1%88%E5%BA%94%E5%AF%B9%E7%AA%81%E5%8F%91%E7%8A%B6%E5%86%B5%EF%BC%8C%E4%BF%9D%E8%AF%81%E8%AF%BE%E5%A0%82%E6%95%99%E5%AD%A6%E6%AD%A3%E5%B8%B8%E8%BF%9B%E8%A1%8C%E3%80%82&result1_9.content=%E9%9D%9E%E5%B8%B8%E6%BB%A1%E6%84%8F&result1_9.score=10&result2_0.questionName=%E4%BD%A0%E5%AF%B9%E8%AF%A5%E6%8E%88%E8%AF%BE%E6%95%99%E5%B8%88%E7%9A%84%E6%84%8F%E8%A7%81%E5%92%8C%E5%BB%BA%E8%AE%AE&result2_0.content=1&result2_1.questionName=%E4%BD%A0%E8%AE%A4%E4%B8%BA%E6%9C%AC%E5%AD%A6%E6%9C%9F%E8%AF%BE%E5%A0%82%E6%95%99%E5%AD%A6%E5%85%B3%E9%94%AE%E5%AD%97%E6%98%AF%E4%BB%80%E4%B9%88&result2_1.content=1&result1Num=10&result2Num=2'
    content=s.post(url='http://bkjw.chd.edu.cn/eams/quality/stdEvaluate!finishAnswer.action',data=data,headers=headers).content.decode()
    if "评教成功" in content:
        return True



def pingjiao(s):
    '''评教的过程'''
    i=1
    data=s.get(url='http://bkjw.chd.edu.cn/eams/quality/stdEvaluate.action',headers=get_headers()).content.decode()
    patten=re.compile(r'evaluationLesson.id=\w+')
    #//table[@class="gridtable"]/tbody/tr/td[2]    #xpath的选择
    result = patten.findall(data)
    for item in result:
        erji(item,s)
        print('成功评教%d个老师...'%i)
        i=i+1
        time.sleep(0.15)
    s.close()#评价成功后关闭会话
    print('评教完成。。。退出')
    
    
def connect():
    """测试能否连接网络"""
    s = requests.Session()#建立一个回话
    if use_proxy==True:
        s.proxies = proxies#使用代理
    try:
        page=s.get('http://bkjw.chd.edu.cn/eams/home.action',headers=get_headers(),timeout=5).text#可以设置到上面
        s.close()
        return True
    except:
        return False

        
    
  