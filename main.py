#!/usr/bin/env python
# coding=utf-8

from BeautifulSoup import BeautifulSoup
from email.mime.text import MIMEText
import logging , requests , time , smtplib , redis , re


LOG_FILENAME='/home/mashu/log/vipshop.log'
#INTERVAL=4 # 4个小时进行一次爬取
FROM_ADDR='user@126.com'
TO_ADDR='qqnum@qq.com'
MAIL_USER='user'
MAIL_PWD='pwd'
MAIL_HOST='smtp.126.com'
URL='http://www.vipshop.com/brand_date.php'
WANT_LIST=[u'阿迪达斯',u'耐克',u'nike',u'adidas']


class Crawler():

	def initLog(self):
		self.logger=logging.getLogger()
		self.logger.setLevel(logging.DEBUG)
		
		fh=logging.FileHandler(LOG_FILENAME,'a')
		fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

		self.logger.addHandler(fh)
		
	def sendEmail(self,text):
		# 不能是MIMEText(text),需要给它传递一个在互联网上使用的编码方式，比如utf-8
		msg=MIMEText(text.encode('utf-8'))
		msg['From']=FROM_ADDR
		msg['To']=TO_ADDR
		msg['Subject']='自制爬虫唯品会通知'
		try:
			smtp=smtplib.SMTP(MAIL_HOST) # 因为提供了host参数，自动connect
			smtp.login(MAIL_USER,MAIL_PWD)
			smtp.sendmail(FROM_ADDR,TO_ADDR,msg.as_string())
			print '成功'
		except Exception as e:
			print e
		finally:
			smtp.quit()


	def __init__(self):
		self.initLog()
		self.rs=redis.Redis()

	def run(self):
		headers={
				"Connection": "keep-alive",
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
				"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31",
				"Accept-Encoding": "gzip,deflate,sdch",
				"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
				"Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
				}
		req=requests.get(URL,headers=headers)
		soup=BeautifulSoup(req.text)
		print req.content
		text=''
		for div in soup.findAll('div',"dating_brand_content"):
			date=div.h2.findNext(text=re.compile(ur'\d{2}月\d{2}日')).string 
			# .string 返回的是unicode
			for dl in div.findAll('dl'):
				title=dl.dd.span.string
				info=date+u'----'+title
				if filter(lambda x:x in title,WANT_LIST) and not self.rs.sismember('vips',info):
					self.rs.sadd('vips',info)
					text+=info+u'\n'
		if text:
			self.sendEmail(text)


if __name__=='__main__':

	# 开机5min之后开始执行，等待网络正常使用
	time.sleep(60*5)
	crawler=Crawler()
	crawler.run()

#	sched=Scheduler()
#	sched.start()
#	sched.add_interval_job(crawler.run,hours=INTERVAL)

