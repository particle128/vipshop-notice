# !/usr/bin/env python
# coding=utf-8

#暂时弃用,不用配置
LOG_FILENAME='/path/to/log/file'

#发送邮件的邮箱
FROM_ADDR='[username]@126.com'
#126邮箱的用户名
MAIL_USER='[username]'
#126邮箱的密码
MAIL_PWD='[passwd]'
#126邮箱smtp服务器地址
MAIL_HOST='smtp.126.com'

#接受邮件的手机号
PhoneNum='[phonenumber]'
#手机号类型，保留一个
PhoneType='[联通|移动|电信]'

#爬虫访问的页面
URL='http://www.vip.com/brand_date.php'

#关注的品牌列表，自行增减，记得在字符串前面加u
WANT_LIST=[u'李维斯',u'Lee',u'阿迪达斯',u'耐克',u'卡帕']

