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


        url = 'https://m.weibo.cn/api/attitudes/show?id=' + str(id1) + '&page=1'
        print url, id1,type(name)
        urls.append([name, id1, time1, text, url])
    return urls





# urls =
Cookie = {
    'Cookie': '_T_WM=72827223218; H5_wentry=H5; backURL=https%3A%2F%2Fm.weibo.cn%2Fprofile%2F6052565946; WEIBOCN_FROM=1110006030; SUB=_2A25wRXTXDeRhGeVG6lQU8i7KyT2IHXVTxhyfrDV6PUJbkdAKLVngkW1NT6iwNH4oUK5xKUEA-CkEI3rDlg_6UPbL; SUHB=0RyqSjoxRCI3eC; MLOGIN=1; XSRF-TOKEN=d44e0f; M_WEIBOCN_PARAMS=oid%3D4299704088494921%26luicode%3D20000061%26lfid%3D4299704088494921%26uicode%3D20000061%26fid%3D4299704088494921'}
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
            total_pages = math.ceil(float(len1)/ 50)
            total_pages = int(total_pages)
            print 'len1:',len1,'page:', total_pages
            ii = 0
            while ii < total_pages:
                print 'ii=', ii
                ii = ii + 1
                if (ii > 100):
                   break
                url_1 = 'https://m.weibo.cn/api/attitudes/show?id=' + str(zhutie_id) + '&page=' + str(ii)
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
                       
                        cursor = connect.cursor()
                        sql = "INSERT IGNORE INTO toutiaoxinwen_zan(meiti,zhutie_id,zhutie_time, text,comment_id,`id1`,name) VALUES" \
                              " ( '%s','%s', '%s','%s','%s','%s','%s')"
                        data1 = (
                        meiti,zhutie_id,zhutie_time, text,comment_id,id1,name)
                        #sql = "INSERT IGNORE INTO RMW_ZF(meiti, zhutie_id,zhutie_time, text, comment_id,id1,name) VALUES" \
                          #    " ( '%s','%s','%s','%s','%s','%s' ,'%s')"
                        #data1 = (
                         #   meiti, zhutie_id, zhutie_time, text, comment_id, id1, name)
                        # print data
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


