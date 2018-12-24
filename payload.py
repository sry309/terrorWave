# -*- coding: utf-8 -*-
#0_common.txt  	:	通用常见的一些字符串
#1_keyword.txt 	:	临时添加的针对性字符串
#2_filetype.txt :	文件格式字符串
#tempPath.txt 	:	存放用以扫描的目录payload
#tempFile.txt 	:	存放用以扫描的文件payload

#通过0、1、2...来生成tempPath.txt和tempFile.txt
import os

#读文件
def readFile(FILE):
	with open(FILE, 'r') as f:
		return f.readlines()

#写文件
def writeFile(FILE,STR):
	with open(FILE, 'a') as f:
		f.write(STR)

#添加0_common字典到扫描payload（tempPath.txt,tempFile.txt）中
def add0ToTemp():
	for i in readFile('./dict/0_common.txt'):
		writeFile('./dict/tempPath.txt',i.strip()+'\n')
		for j in readFile('./dict/2_filetype.txt'):
			writeFile('./dict/tempFile.txt',i.strip()+'.'+j.strip()+'\n')


#添加1_keyword字典到扫描payload（tempPath.txt,tempFile.txt）中
def add1ToTemp():
	for i in readFile('./dict/1_keyword.txt'):
		writeFile('./dict/tempPath.txt',i.strip()+'\n')
		for j in readFile('./dict/2_filetype.txt'):
			writeFile('./dict/tempFile.txt',i.strip()+'.'+j.strip()+'\n')

#添加3_superUrl字典到扫描payload（tempFile.txt）中
def add3ToTemp():
	for i in readFile('./dict/3_superUrl.txt'):
		if i.strip()[0] != '/':
			j = '/'+i.strip()
		else:
			j = i
		writeFile('./dict/tempFile.txt',j+'\n')


#通过0、1、2...来生成tempPath.txt和tempFile.txt
def setPayload():
	try:
		os.remove('./dict/tempPath.txt')
		os.remove('./dict/tempFile.txt')
	except :
		pass
	print '[i]remove old temp files success !'

	#先把keyword添加进payload，再添加common
	add1ToTemp()
	add0ToTemp()
	add3ToTemp()	
	print '[i]creat payload (tempPath.txt,tempFile.txt) success !'

if __name__ == '__main__':
	setPayload()

