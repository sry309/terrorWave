# -*- coding: utf-8 -*-
import requests
import hashlib
from payload import *
import os

black_list = [] #反例，用以存放确认不存在的响应demo
white_list = [] #正例，用以存放确认存在的响应demo

#规范目录型url以/结尾
def formatPATH(url_input):
	if url_input[-1] == '/':
		return url_input
	else:
		return url_input+'/'

#取响应码和内容的前N字节，创建签名
def creatSign(status_code,content):
	status_code = str(status_code)
	content = content[0:2000] #使用响应内容的0到2000字节来创建签名
	src = status_code + content
	m2 = hashlib.md5()   
	m2.update(src)  
	return m2.hexdigest()


#url探测，待完善（如添加多种探测方式）
def reqUrl(URL):
	session = requests.Session()
	headers = {"Cache-Control":"max-age=0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36","Connection":"close","X-Forwarded-For":"127.0.0.1","Accept-Language":"zh-CN,zh;q=0.9"}
	try:
		response = session.get(URL, headers=headers)
	except Exception as e:
		if e == KeyboardInterrupt:
			os.exit()
		else:
			return ('exception','exception')
			pass
	return response.status_code,response.content

#判断reqUrl是否发生异常
def isReqException(status_code):
	if str(status_code) == 'exception':
		return True
	else:
		return False

#如果响应码为20x，则返回true
def status_codeIsExit(status_code):
	pre_status_code = str(status_code)[0:2]
	if pre_status_code == '20' or str(status_code) == '403':
		return True
	else:
		return False

#使用一个确认不存在的路径，创造一个响应demo，反例
def creatNotExistDemo(notExistPath):
	if len(notExistPath) > 0:
		for PATH in notExistPath:
			status_code,content = reqUrl(PATH)
			if not isReqException(status_code) :
				sign = creatSign(status_code,content)
				black_list.append(sign)
			else:
				pass
	else:
		pass


#使用一个确认存在的路径，创造一个响应demo，正例
def creatExistDemo(existPath):
	if len(existPath) > 0:
		for PATH in existPath:
			status_code,content = reqUrl(PATH)
			if not isReqException(status_code) :
				sign = creatSign(status_code,content)
				white_list.append(sign)
			else:
				pass
	else:
		pass

#判断响应是否在黑名单内
def respIsInBlack_list(status_code,content):
	if len(black_list)>0 :
		if creatSign(status_code,content) in black_list:
			return True
		else:
			return False
	else:
		return False

#判断响应是否在白名单内
def respIsInWhite_list(status_code,content):
	if len(white_list)>0 :
		if creatSign(status_code,content) in white_list:
			return True
		else:
			return False
	else:
		return False


#断言主函数:先判断是否在黑名单、再判断是否在白名单、最后采用响应码来进行不准确判断。
def urlIsExist(status_code,content):
	if isReqException(status_code):
		return False
	elif respIsInBlack_list(status_code,content):
		return False
	elif respIsInWhite_list(status_code,content):
		return True
	elif status_codeIsExit(status_code):
		return True
	else:
		return False

#扫描url，如果存在，则返回此url，不存在则返回noFound
def scan(URL):
	status_code,content = reqUrl(URL)
	print '[i]'+URL+'('+str(status_code)+')'
	if urlIsExist(status_code,content):
		return URL
	else :
		return 'this URL:' +URL

#扫描目录
def scan_path(URL,resultFile):
	for url_path in readFile('./dict/tempPath.txt'):
		exist_url = scan(URL+formatPATH(url_path.strip()))
		if exist_url[0:4] == 'this' :
			print '[NotExist]'+exist_url
			pass
		else:
			print '[Exist]'+exist_url
			writeFile(resultFile,exist_url+'\n')

#扫描文件
def scan_File(URL,resultFile):
	for url_path in readFile('./dict/tempFile.txt'):
		exist_url = scan(URL+url_path.strip())
		if exist_url == 'noFound' :
			print '[NotExist]'+exist_url
			pass
		else:
			print '[Exist]'+exist_url
			writeFile(resultFile,exist_url+'\n')
		
def scan_main(URL,notExistPath,existPath,resultFile):
	URL = formatPATH(URL)

	#设置扫描配置文件，如生成正例、反例
	creatNotExistDemo(notExistPath)
	print '[i]black_list is :'
	print black_list
	creatExistDemo(existPath)
	print '[i]white_list is :'
	print white_list
	
	scan_path(URL,resultFile) #扫描路径
	scan_File(URL,resultFile) #扫描文件


