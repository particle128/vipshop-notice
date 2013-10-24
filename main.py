#!/usr/bin/env python
# coding=utf-8

from BeautifulSoup import BeautifulSoup
from email.mime.text import MIMEText
from email.charset import Charset
import logging , requests , time , smtplib , re
from config import *



TO_ADDR=''
if PhoneType=='联通':
	TO_ADDR=PhoneNum+'@wo.com.cn'
elif PhoneType=='移动':
	TO_ADDR=PhoneNum+'@139.com'
elif PhoneType=='电信':
	TO_ADDR=PhoneNum+'@189.com'
else:
	print '输入的电话运营商类型有误'
	exit(1)

class Crawler():

	#因为可以用重定向，所以self.logger弃用
	def initLog(self):
		self.logger=logging.getLogger()
		self.logger.setLevel(logging.DEBUG)
		
		fh=logging.FileHandler(LOG_FILENAME,'a')
		fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

		self.logger.addHandler(fh)
		
	def sendEmail(self,text):
		# 不能是MIMEText(text),因为text是unicode类型，需要给它传递一个在互联网上传输使用的编码方式，比如utf-8,gbk,依据不同邮箱而不同
		msg=MIMEText(text,_charset='utf-8') #SMPT首部指定使用utf-8编码。如果text是unicode，自动encode然后发送
		msg['From']=FROM_ADDR
		msg['To']=TO_ADDR
		msg['Subject']=u'自制爬虫唯品会通知'
		try:
			smtp=smtplib.SMTP(MAIL_HOST) # 因为提供了host参数，自动connect
			smtp.login(MAIL_USER,MAIL_PWD)
			smtp.sendmail(FROM_ADDR,TO_ADDR,msg.as_string())
			print '邮件发送成功'
		except Exception as e:
			print e
		finally:
			smtp.quit()


	def __init__(self):
		self.initLog()

	def run(self):
		print 'crawler start...'
		headers={
				"Connection": "keep-alive",
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
				"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31",
				"Accept-Encoding": "gzip,deflate,sdch",
				"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
				"Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
				}

		try:
			req=requests.get(URL,headers=headers)
		except Exception as e:
			logger.error(e)
			return
		soup=BeautifulSoup(req.text)
		text=''
		ul=soup.find('ul','tomorrow_list')
		for ele in ul.findAll('li',"J_click_wrap"):
			if filter(lambda x:x in ele['data-name'],WANT_LIST):
				print (u'find demanded brands:'+ele['data-name']).encode('utf-8')
				text+=ele['data-name'] +u' '
		if text:
			print 'sending email begin...'
			self.sendEmail(text)
			print 'sending email end...'
		print 'crawler end...'


if __name__=='__main__':

	crawler=Crawler()
	crawler.run()


