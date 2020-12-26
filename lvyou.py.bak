import requests
from lxml import etree
import re
import time
import datetime
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Cookie':'SCF=AiEzkE_YiOfr6KZrN9gwbxIWh5at6dldihJhDB09hPdBjYHuEamKwBw2JwQSjWX9aXgqva3drt8n7CiUrr4Qb7I.; _T_WM=3bf40f8a8666b500aa89441474c0143c; SUB=_2A25y1oGZDeRhGeRP6FMV9ivJyT6IHXVuOC_RrDV6PUJbktANLXf2kW1NUCupxiEVVyN_kk7GliuVk-79aaTK0kkA; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5OGXIi5MM8SNSz6T4-N8pg5NHD95QEeKepShqfSKzEWs4DqcjexPSQIg4L-cL_Igxy; SSOLoginState=1607659978'}



import pymysql

connect = pymysql.Connect(
    host='rm-wz988to0p0a7js870o.mysql.rds.aliyuncs.com',
    port=3306,
    user='root',
    passwd='zd45+3=48',
    db='ctrip_gengxin',
    use_unicode=1,
    charset='utf8'
)
cursor = connect.cursor()
# 2013-08-17   2014-01-01
date_start = datetime.datetime.strptime("2020-11-12", '%Y-%m-%d')
# 搜索的结束日期，自行修改
date_end = datetime.datetime.strptime("2020-12-01", '%Y-%m-%d')

time_spread = datetime.timedelta(days=1)
url_format = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=旅游&advancedfilter=1&starttime={}&endtime={}&sort=time&page='
while date_start < date_end:
    next_time = date_start + time_spread
    url = url_format.format(date_start.strftime("%Y%m%d"), date_start.strftime("%Y%m%d"))
    date_start = next_time
    #print(url)


    for i in range(1,101):
        url1 = url + str(i)
        print(url1)
        time.sleep(2)
        html2 = requests.get(url=url1,headers=head)
        html3 = html2.content
        _element1 = etree.HTML(html3)
        # 通过xpath表达式获取h1标签中的文本
        tweet_nodes = _element1.xpath('//div[@class="c" and @id]')
        #print(tweet_nodes)
        for tweet_node in tweet_nodes:
            tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href')[0]
            user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
            weibo_url = 'https://weibo.com/{}/{}'.format(user_tweet_id.group(2), user_tweet_id.group(1))
            user_id = user_tweet_id.group(2)
            name = tweet_node.xpath('.//a[@class="nk"]/text()')
            href = tweet_node.xpath('.//a[@class="nk"]/@href')[0]
            requests.get(href, )
            if (name):
                name = name[0]
            else:
                name = 'none'
            ID = '{}_{}'.format(user_tweet_id.group(2), user_tweet_id.group(1))
            create_time_info = tweet_node.xpath('.//span[@class="ct"]/text()')[0]
            if "来自" in create_time_info:
                # 微博发表时间
                created_at = create_time_info.split('来自')[0].strip()
                laizi = create_time_info.split('来自')[1].strip()


            else:
                created_at = create_time_info.strip()
                laizi = 'none'

            like_num = tweet_node.xpath('.//a[contains(text(),"赞[")]/text()')[0]
            like_num = int(re.search('\d+', like_num).group())

            content = ''.join(tweet_node.xpath('./div[1]')[0].xpath('string(.)')
                              ).replace(u'\xa0', '').replace(u'\u3000', '').replace(' ', '').split('赞[', 1)[0]

            repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[0]
            repost_num = int(re.search('\d+', repost_num).group())

            comment_num = tweet_node.xpath(
                './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[0]
            comment_num = int(re.search('\d+', comment_num).group())
            time.sleep(1)
            html = requests.get(url=href, headers=head)
            #print(html.encoding)
            html1 = html.content
            # html.encoding = 'gbk'
            # print(html.text)

            _element = etree.HTML(html1)
            # 通过xpath表达式获取h1标签中的文本
            text = _element.xpath('//div[@class="ut"]/span[1]/text()')
            text = ''.join(text)
            print(text)
            if "/" in text:
                address = text.split('/')[1]
            else:
                address = 'none'
            print(address)

            sql = "INSERT IGNORE INTO zz_lvyou(ID, time, text, name,zhuanfa, pinglun, zan,laizi, city) VALUES ( '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s')"
            data1 = (ID, created_at, content, name, repost_num, comment_num, like_num, laizi, address)

            try:
                cursor.execute(sql % data1)
            except:
                print(ID)

            connect.commit()
            print(created_at)



            #print(name,user_id, created_at, laizi, like_num, content, repost_num,comment_num, href, address)