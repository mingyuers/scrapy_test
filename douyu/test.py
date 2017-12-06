# coding=utf-8

# import socket
#
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.connect(('openbarrage.douyutv.com',8601))
# s.send('type@=loginreq/roomid@=2046501/')
# print s.recv(1024)
# from douyu.chat.room import ChatRoom
#
# def on_chat_msg(msg):
#     print '[%s]:%s'%(msg.attr('nn'),msg.attr('txt'))
#
# room = ChatRoom('48699')
# room.on('chatmsg',on_chat_msg)
# room.knock()

import win32gui
import keyboard
import time

k = win32gui.FindWindow(None, 'Foxmail')
win32gui.SetForegroundWindow(k)
keyboard.press_and_release('down')
time.sleep(0.5)
keyboard.press_and_release('down')
time.sleep(0.5)
keyboard.press_and_release('down')
time.sleep(0.5)
keyboard.press_and_release('down')
time.sleep(0.5)
keyboard.press_and_release('down')
time.sleep(0.5)
keyboard.press_and_release('down')
time.sleep(0.5)
keyboard.press_and_release('down')
