# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:52:50 2021

@author: lenovo
"""

# 导入必要的包
import requests
import json
import time



import pymysql

connect = pymysql.Connect(
    host='',
    port=3306,
    user='root',
    passwd='',
    db='ctrip_gengxin',
    use_unicode=1,
    charset='utf8'
)
cursor = connect.cursor()
# header这个的作用在于伪装成浏览器进行操作，有些网页识别到不是浏览器就不能访问，User-Agent能伪装
# User-Agent可以用不同个，一般在刚刚找网页网址url的Headers的下面就有，当然也可以使用手机的，可网页搜索找到不同的User-Agent，都能进行相应操作
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}

url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=5225346&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1'
# 我们可以简单的解析这个网址，前面不动，后面的我们点击下一页，看会出现什么改变
#https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=5225346&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1
# 我们发现只有page在变化，根据这个我们可以进行翻页爬取，我们先进行第一页的操作





for page in range(0,100+1):
    url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100008348542&score=0&sortType=6&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(page) 
    time.sleep(2)
    response = requests.get(url, headers=header) 
    data = response.text  
    jd = json.loads(data.lstrip('fetchJSON_comment98vv12345(').rstrip(');')) 
    data_list = jd['comments'] 
    for data in data_list:      
        buyer_id = data['id']      
        content = data['content']  
        name = data['nickname']
        time1 = data['creationTime']
        phone = data['referenceName']
        print(buyer_id, content, time1)
        sql = "INSERT IGNORE INTO zz_jd(ID,  name, comment,time,phone) VALUES ( '%s', '%s', '%s','%s','%s')"
        data1 = (buyer_id, name, content, time1,phone)

        try:
            cursor.execute(sql % data1)
        except:
            print(ID)

        connect.commit()


