# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 16:46:19 2017

@author: dell
"""
#动态加载
import requests
import re
import time

ii = 10
while ii <= 20:
    ii = ii + 1
    url = 'https://m.weibo.cn/api/comments/show?id=4188633986790962&page=' + str(ii)
    time.sleep(3)
    html = requests.get(url)
    try:
        for jj in range(len(html.json()['data']['data'])):
            data = html.json()['data']['data'][jj]['text']
            with open('weibo.txt', 'a') as ff:
                hanzi = ''.join(re.findall('[\u4e00-\u9fa5]', data))
                #print(hanzi)
                ff.write(hanzi + '\n')
    except:
        None
            
        
