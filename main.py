# -*- coding: utf-8 -*-
from scan_lib import *
from payload import *
import os

URL = 'https://idt9.test.com.cn/'
notExistPath = ['https://idt9.test.com.cn/admin/']
existPath = []

resultFile = './result/'+URL.split('://')[1][0:4] + '.txt'

#删除历史扫描结果
def clearResult(resultFile):
	try:
		os.remove(resultFile)
		print '[i]remove old result success !'
	except :
		pass

#主函数
def main():
	setPayload()
	clearResult(resultFile)
	scan_main(URL,notExistPath,existPath,resultFile)

	try:
		os.system(r'open '+resultFile)
	except:
		pass

if __name__ == '__main__':
	main()