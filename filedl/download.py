#coding=utf-8
import requests
from contextlib import closing


class DL(object):
	"""docstring for DL"""
	def __init__(self, url,file_name):
		print url,file_name
		super(DL, self).__init__()
		self.url = url
		self.file_name = file_name

	def do(self):
		with closing(requests.get(self.url, stream=True)) as response:
		    chunk_size = 1024 # 单次请求最大值
		    content_size = int(response.headers['content-length']) # 内容体总大小
		    progress = ProgressBar(self.file_name, total=content_size,
		                                     unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
		    with open(self.file_name, "wb") as file:
		       for data in response.iter_content(chunk_size=chunk_size):
		           file.write(data)
		           progress.refresh(count=len(data))


class ProgressBar(object):

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end_str)



url= 'https://bbuseruploads.s3.amazonaws.com/fd96ed93-2b32-46a7-9d2b-ecbc0988516a/downloads/98d51451-997f-40e3-b9e6-a8e635dcdcb3/phantomjs-2.1.1-windows.zip?Signature=1IUCvjMiNA%2FBLomMkSTzWf5B4zw%3D&Expires=1501560386&AWSAccessKeyId=AKIAIQWXW6WLXMB5QZAQ&versionId=null&response-content-disposition=attachment%3B%20filename%3D%22phantomjs-2.1.1-windows.zip%22'
dl = DL(url)
dl.do()