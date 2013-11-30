Brand reminder of vip.com
===

## Introduction
The crawler is used to grab information in [www.vip.com/brand_date.php](http://www.vip.com/brand_date.php), and send an email to you if some brands you are interested appear. If you have enabled the SMS reminder of your email, you'll receive a SMS message.

## Requirements
```
pip install beautifulsoup
pip install requests
```

## Configuration
see cnofig.py  

## Usage
Making use of `cron`, grab the information every 9:30 in the morning.
```
echo "30 09 * * * python /path/to/the/project/main.py >>/path/to/the/log/vipshop.log 2>&1" >>crontab -e
```
