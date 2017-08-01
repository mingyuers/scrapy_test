#coding=utf-8

import itchat
from itchat.content import *

@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    print msg
    print msg['FromUserName']
    print msg['Text']
    itchat.send('%s:%s'%(msg['Type'],msg['Text']),msg['FromUserName'])

itchat.auto_login(hotReload=True)
itchat.run()