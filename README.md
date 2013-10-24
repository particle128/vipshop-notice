# vipshop关注品牌提醒软件

##软件说明
本软件是抓取vipshop上商品预告信息的爬虫，一旦抓到的数据和用户满足用户的要求，会发送邮件到用户配置的手机邮箱里，如果邮箱开启了“免费短信功能”，手机会接受到短信提醒。

##使用方法

###所需库
* beautifulsoup
```sh
pip install beautifulsoup
```
###使用
1. 配置config.py，添加自己的邮箱信息和手机号码，还有需要提醒的商品信息。
2. 执行如下命令，添加该爬虫到crontab
```sh
echo "30 09 * * * python /path/to/the/project/main.py >>/path/to/the/log/vipshop.log 2>&1" >>crontab -e
```
