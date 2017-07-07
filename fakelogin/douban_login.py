#coding=utf-8
import  requests
from bs4 import BeautifulSoup
from PIL import Image
from utils import ThreadImg
import threading

session = requests.Session()

url = 'https://accounts.douban.com/login'
data = {
    'source':'index_nav',
    'redir':'https%3A%2F%2Fwww.douban.com%2F',
    'form_email':'18321179923',
    'form_password':'199358fgm',
    'login':'%E7%99%BB%E5%BD%95'
}


# req = requests.post(url,data)
# print req.text
# print req.url
# print req.headers

def get_captcha(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'lxml')
    link = soup.select('#captcha_image')[0]['src']
    id = soup.select('div.captcha_block > input')[1]['value']
    return id , link

def showImg(path):
    im = Image.open(path)
    im.show()

id , link = get_captcha(url)
if id:
    print id
    img_html = requests.get(link)
    with open('caprcha.png','wb') as f:
        f.write(img_html.content)
    # try:
    #     im = Image.open('caprcha.png')
    #     im.show()
    #     # im.close()
    # except :
    #     print '打开错误'
    # ti = ThreadImg('caprcha.png')
    # ti.start()


    th = threading.Thread(target = showImg,args = ('caprcha.png',))
    th.start()

    caprcha = raw_input('请输入验证码：')

    data = {                    #需要传去的数据
        'source':'index_nav',
        'redir':'https://www.douban.com/',
        'form_email':'18321179923',
        'form_password':'199358fgm',
        'login':'登陆'
    }
    if id:
        data['captcha-id'] = id
        data['captcha-solution'] = caprcha
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
             'referer':'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001'
             }
    html = session.post(url ,data=data,headers=headers)
    # print html.text,'\n',session.cookies

    html_my = session.get('https://www.douban.com/people/143487885/')
    # print html_my.text
    print session.cookies