# coding:utf-8
import sys,os
url='https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/e35/20067171_107500479927442_1159351173728174080_n.jpg'
p = os.getcwd()+'/'+url.split('/')[-1]
open(p,'wb')
print sys.path