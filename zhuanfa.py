# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 11:42:58 2019

@author: lenovo
"""

import requests
import re
import time

#import pandas as pd
# import requests
import csv
import numpy as np
import math
import pymysql
import json

connect = pymysql.Connect(
    host='***',
    port=3306,
    user='root',
    passwd='****',
    db='meiti',
    use_unicode=1,
    charset='utf8'
)


# from urllib.parse import urlencode
def get_url():
    np.set_printoptions(suppress=True)
    csv_file = csv.reader(open('toutiaoxinwen_sub.txt', 'r'))
    urls = []
    for stu in csv_file:
        
        name = stu[2]
        id1 = stu[6]
        time1 = stu[8]
        text = stu[7]
        #name = name.encode('utf-8')
        name = name.decode('gbk').encode('utf-8')
        text = text.decode('gbk').encode('utf-8')


        url = 'https://m.weibo.cn/api/statuses/repostTimeline?id=' + str(id1) + '&page=1'
        print url, id1,type(name)
        urls.append([name, id1, time1, text, url])
    return urls


# print csv_file


# urls =
Cookie = {
    'Cookie': '_T_WM=47854944278; WEIBOCN_FROM=1110006030; ALF=1565015112; SCF=ApI7HxidQxU5v8irMXxaTGdQW3FI_s9n_4gfl1xjFie9RcQ9DRxhMM1CmDNh6di_CJeq4G4NUiD12ExyTOpLje8.; SUB=_2A25wJN8ZDeRhGeRP6FMV9ivJyT6IHXVT5uFRrDV6PUNbktAKLWOgkW1NUCupxnHOYXZ2Ofwp24p10cUXdHxRfmK-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5OGXIi5MM8SNSz6T4-N8pg5JpX5KzhUgL.Fozpe02XSo-feoz2dJLoI7p8McyDdJHKIgfD9s2t; SUHB=0cS23jbLSu6jWn; SSOLoginState=1562423113; MLOGIN=1; XSRF-TOKEN=0ebe45; M_WEIBOCN_PARAMS=oid%3D4391182375041100%26luicode%3D20000061%26lfid%3D4391182375041100%26uicode%3D20000061%26fid%3D4391182375041100'}
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}





def process():
    urls = get_url()
    urls1 = urls[1:]
    # x = []
    m = 0
    for url in urls1:
        m = m + 1
        print 'm=', m
        url1 = url[4]
        meiti = url[0]
        zhutie_id = url[1]
        zhutie_time = url[2]
        text = url[3]

        print url1

        # zhutie = url
        # url1 = urls[0][4]
        try:
            html = requests.get(url1, headers=head)
            len1 = html.json()['data']['total_number']
            total_pages = math.ceil(float(len1)/ 10)
            total_pages = int(total_pages)
            print 'len1:',len1,'page:', total_pages
            ii = 0
            while ii < total_pages:
                print 'ii=', ii
                ii = ii + 1
                if (ii > 100):
                   break
                url_1 = 'https://m.weibo.cn/api/statuses/repostTimeline?id=' + str(zhutie_id) + '&page=' + str(ii)
                print url_1
                # 'https://m.weibo.cn/api/comments/show?id=4374854079489348&page='
                time.sleep(5)

                try:
                    html = requests.get(url_1, headers=head, cookies=Cookie)
                    print html
                    for jj in range(len(html.json()['data']['data'])):
                        #data = html.json()['data']['data'][jj]['text']
                        #time1 = html.json()['data']['data'][jj]['created_at']
                        comment_id = html.json()['data']['data'][jj]['id']
                        id1 = html.json()['data']['data'][jj]['user']['id']
                        name = html.json()['data']['data'][jj]['user']['screen_name']

                            # print(meiti,zhutie_id,zhutie_time,text,id1,name,sex,time1,hanzi,followers,follow)
                        print meiti,zhutie_id, zhutie_time, name, comment_id,id1
                        name = name.encode('utf-8')
                       
                        comment_id = comment_id.encode('utf-8')






                        cursor = connect.cursor()
                        sql = "INSERT IGNORE INTO toutiaoxinwen_zhuanfa(meiti,zhutie_id,zhutie_time, text,comment_id,`id1`,name) VALUES" \
                              " ( '%s','%s', '%s','%s','%s','%s','%s')"
                        data1 = (
                        meiti,zhutie_id,zhutie_time, text,comment_id,id1,name)
                      
                        try:
                            cursor.execute(sql % data1)
                        except:
                            print(comment_id)

                        connect.commit()

                except:
                    None
        except:
            None

            # return x


if __name__ == '__main__':
    process()


