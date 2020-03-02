# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 11:42:58 2019

@author: lenovo
"""

import requests
import re
import time

import pandas as pd
# import requests
import csv
import numpy as np
import math
import pymysql
import json

connect = pymysql.Connect(
    host='****',
    port=3306,
    user='root',
    passwd='*****',
    db='meiti',
    use_unicode=1,
    charset='utf8'
)


# from urllib.parse import urlencode
def get_url():
    np.set_printoptions(suppress=True)
    csv_file = csv.reader(open('xinlangcaijing_sub.txt', 'r'))
    urls = []
    for stu in csv_file:
       
        name = stu[2]
        id1 = stu[6]
        time1 = stu[8]
        text = stu[7]
        #name = name.encode('utf-8')
        name = name.decode('gbk').encode('utf-8')
        text = text.decode('gbk').encode('utf-8')


        url = 'https://m.weibo.cn/comments/hotflow?id=' + str(id1) + '&mid=' + str(id1) + '&max_id_type=0'
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
    urls1 = urls[336:]
    # x = []
    m = 0
    for url in urls1:
        m = m + 1
        print 'm=',m
        url1 = url[4]
        meiti = url[0]
        zhutie_id = url[1]
        zhutie_time = url[2]
        text = url[3]

        # zhutie = url
        # url1 = urls[0][4]
        try:
            html = requests.get(url1, headers=head)
            len1 = html.json()['data']['total_number']
            total_pages = math.ceil(float(len1) / 10)
            total_pages = int(total_pages)
            print 'len1:',len1,'page:', total_pages
            ii = 0
            while ii < total_pages:
                print 'ii=', ii
                ii = ii + 1
                if (ii > 100):
                    break
                url_1 = 'https://m.weibo.cn/api/comments/show?id=' + str(zhutie_id) + '&page=' + str(ii)
                # 'https://m.weibo.cn/api/comments/show?id=4374854079489348&page='
                time.sleep(3)

                try:
                    html = requests.get(url_1, headers=head, cookies=Cookie)
                    print html,url_1
                    for jj in range(len(html.json()['data']['data'])):
                        data = html.json()['data']['data'][jj]['text']
                        time1 = html.json()['data']['data'][jj]['created_at']
                        comment_id = html.json()['data']['data'][jj]['id']
                        id1 = html.json()['data']['data'][jj]['user']['id']
                        name = html.json()['data']['data'][jj]['user']['screen_name']
                        # sex = html.json()['data']['data'][jj]['user']['gender']
                        followers = html.json()['data']['data'][jj]['user']['followers_count']
                        # follow = html.json()['data']['data'][jj]['user']['follow_count']
                        hanzi = ''.join(re.findall(u'[\u4e00-\u9fa5]', data))
                        #print hanzi

                        url_info = 'https://m.weibo.cn/api/container/getIndex?containerid=230283' + str(id1) + '_-_INFO'
                        time.sleep(3)
                        r = requests.get(url_info, headers=head,cookies = Cookie)
                        infojson = json.loads(r.text)
                        infodata = infojson.get('data')
                        cards = infodata.get('cards')
                        sex = ''
                        loc = ''
                        zhuce_time = ''
                        renzheng = ''
                        xingyong = ''
                        birthday = ''

                        for l in range(0, len(cards)):
                            temp = cards[l]
                            card_group = temp.get('card_group')
                            for m in range(0, len(card_group)):
                                s = card_group[m]
                                #print s
                                if s.get('item_name') == u'性别':
                                    sex = s.get('item_content')

                                if s.get('item_name') == u'所在地':
                                    loc = s.get('item_content')

                                if s.get('item_name') == u'注册时间':
                                    zhuce_time = s.get('item_content')
                                if s.get('item_type') == u'verify_yellow':
                                    renzheng = s.get('item_content')
                                if s.get('item_name') == u'阳光信用':
                                    xingyong = s.get('item_content')
                                if s.get('item_name') == u'生日':
                                    birthday = s.get('item_content')

                        if sex is None:
                            sex = '未知'
                        if loc is None:
                            loc = '未知'

                        if zhuce_time is None:
                            zhuce_time = '未知'
                        if renzheng is None:
                            renzheng = '未知'
                        if xingyong is None:
                            xingyong = '未知'

                        user_url = 'https://m.weibo.cn/profile/info?uid=' + str(id1)
                        time.sleep(3)
                        ru = requests.get(user_url, headers=head, cookies=Cookie)
                        infojson1 = json.loads(ru.text)
                        infodata1 = infojson1.get('data')
                        user = infodata1.get('user')
                        weibo_num = user['statuses_count']
                        followers_count = user['followers_count']
                        follow_count = user['follow_count']


                            # print(meiti,zhutie_id,zhutie_time,text,id1,name,sex,time1,hanzi,followers,follow)
                        print meiti,zhutie_id, zhutie_time, name, comment_id, loc,type(time1), type(hanzi), type(followers)
                        name = name.encode('utf-8')
                        sex = sex.encode('utf-8')
                        loc = loc.encode('utf-8')
                        time1 = time1.encode('utf-8')
                        hanzi = hanzi.encode('utf-8')
                        zhuce_time = zhuce_time.encode('utf-8')
                        renzheng = renzheng.encode('utf-8')
                        xingyong = xingyong.encode('utf-8')
                        birthday = birthday.encode('utf-8')
                      
                        cursor = connect.cursor()
                        sql = "INSERT IGNORE INTO xinlangcaijing_comment(`meiti`, zhutie_id,zhutie_time, `text`, comment_id,id1,`name`,sex,loc,time1, hanzi, followers," \
                              "zhuce_time,renzheng,xingyong,weibo_num,follow, birthday) VALUES ( '%s','%s','%s','%s','%s','%s' ,'%s','%s' ,'%s','%s','%s' ,'%s','%s' ,'%s','%s','%s' ,'%s','%s')"
                        data1 = (
                        meiti, zhutie_id,zhutie_time, text, comment_id,id1,name,sex,loc,time1, hanzi, followers,zhuce_time,renzheng,xingyong,weibo_num,follow_count, birthday)
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


