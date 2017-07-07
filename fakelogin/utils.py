#coding=utf-8
import threading
from PIL import Image

class ThreadImg(threading.Thread):

    def __init__(self,path):
        self.path = path

    def run(self):
        im = Image.open(self.path)
        im.show()