# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 20:25:50 2019

@author: a4546
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 09:35:12 2019

@author: Administrator
"""

#动态加载
import requests
import re
import time

import pandas as pd
import requests
import csv
import numpy as np
import pymysql
from urllib.parse import urlencode

connect = pymysql.Connect(
        host='rm-wz988to0p0a7js870o.mysql.rds.aliyuncs.com',
        port=3306,
        user='root',
        passwd='zd45+3=48',
        db='meiti',
        use_unicode=1,
        charset='utf8'
    )
#base_url = 'https://m.weibo.cn/api/container/getIndex?'
#base_url = 'https://m.weibo.cn/api/container/getIndex?uid=1267454277&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%87%A4%E5%87%B0%E5%91%A8%E5%88%8A&type=uid&value=1267454277&'
#url = 'https://m.weibo.cn/api/container/getIndex?uid=1267454277&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%87%A4%E5%87%B0%E5%91%A8%E5%88%8A&type=uid&value=1267454277&containerid=1076031267454277&page=2'
#requests.get(url, headers = head).json()
#
#Cookie = {'Cookie':'_T_WM=47854944278; SSOLoginState=1561903263; ALF=1564495263; SCF=ApI7HxidQxU5v8irMXxaTGdQW3FI_s9n_4gfl1xjFie98yHjfNgjHrBD3f0crwRNbkz1S5R2lAJpLDcrCxq3W3E.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5OGXIi5MM8SNSz6T4-N8pg5JpX5KMhUgL.Fozpe02XSo-feoz2dJLoI7p8McyDdJHKIgfD9s2t; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fm.weibo.cn%2Fcomments%2Fhotflow%3Fid%3D4184261000821994%26mid%3D4184261000821994%26max_id_type%3D0%26page%3D10; SUB=_2A25wHLFLDeRhGeBG7lsV9S3Kwz-IHXVT_t8DrDV6PUJbkdAKLWrDkW1NRhnyJ4GxIA5PbirJLGZHMyrAHW948R17; SUHB=0LcSCKV8neiHXj; MLOGIN=1; XSRF-TOKEN=e5521b; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D20000174%26lfid%3D231093_-_selffollowed%26uicode%3D20000174'}
head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
def get_page(con_id,page):
    parames = {
                "containerid" : con_id,
                
                "page" : page
                
                }
        #print(base_url + urlencode(parames))
    time.sleep(2)
    response = requests.get(base_url + urlencode(parames), headers = head)
        #print(response.json())
    return response.json()




########36032803301701
#x = []6032803301701
m = 0
cursor = connect.cursor()
for page in range(2500, 3500):
    try:
        m =  m+1
        print(m)
        #con_id = '1005051267454277'
        url = 'https://m.weibo.cn/api/container/getIndex?uid=1651428902&luicode=10000011&lfid=100103type%3D1%26q%3D21%E4%B8%96%E7%BA%AA%E7%BB%8F%E6%B5%8E%E6%8A%A5%E9%81%93&type=uid&value=1651428902&containerid=1076031618051664&page=' + str(page)
        time.sleep(2)
        res_json = requests.get(url, headers = head).json()
        #res_json = get_page(con_id,page)
        weibo_num = res_json['data']['cardlistInfo']['total']
        id1 = res_json['data']['cards'][0]['mblog']['user']['id']
        name = res_json['data']['cards'][0]['mblog']['user']['screen_name']
        
        follow = res_json['data']['cards'][0]['mblog']['user']['follow_count']
        follower = res_json['data']['cards'][0]['mblog']['user']['followers_count']
        len1 = len(res_json['data']['cards'])
        for i in range(len1):
            
            id_tiezi = res_json['data']['cards'][i]['mblog']['id']
            time1 = res_json['data']['cards'][i]['mblog']['created_at']
            data = res_json['data']['cards'][i]['mblog']['text']
            hanzi = ''.join(re.findall('[\u4e00-\u9fa5]', data))
            
            comment_num = res_json['data']['cards'][i]['mblog']['comments_count']
            zan = res_json['data']['cards'][i]['mblog']['attitudes_count'] 
            zhuanfa = res_json['data']['cards'][i]['mblog']['reposts_count']
            #print(id1, name, id_tiezi,time,hanzi, comment_num,zan, zhuanfa)
            print(name,time1)
            #x.append([id1, name,weibo_num,follow,follower, id_tiezi,time1,hanzi, comment_num,zan, zhuanfa])
            cursor = connect.cursor()
            sql = "INSERT IGNORE INTO toutiaoxinwen(id1, name,weibo_num,follow,follower, id_tiezi,time1,hanzi, comment_num,zan, zhuanfa) VALUES ( '%s','%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s' ,'%s')"
            data = (id1, name,weibo_num,follow,follower, id_tiezi,time1,hanzi, comment_num,zan, zhuanfa)
            #print data
            try:
                cursor.execute(sql % data)
            except:
                print(id_tiezi)

            connect.commit()
            # with open('weibo.txt', 'a') as ff:
              # ff.write(id1 + '\t' + name +'\t'+id_tiezi+'\t'+time+'\t'+hanzi+'\t'+c)
    except:
        None
    #c = pd.DataFrame(x)
    #c.columns = ['id1', 'name','weibo_num','follow','follower', 'id_tiezi', 'time','hanzi','comment_num','zan','zhuanfa']
    #c.to_csv('meiri2.csv')

#ALF
