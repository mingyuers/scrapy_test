# coding=utf-8

import keyboard
import time


# keyboard.press_and_release('left')
# time.sleep(0.01)
# keyboard.press_and_release('c')
# time.sleep(2)
# keyboard.write('22222')

def test(e):
    print e


keyboard.hook(test)
keyboard.wait('=')
