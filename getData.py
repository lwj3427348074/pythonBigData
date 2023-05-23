import requests         #请求
import csv
import os               #文件操作
from pymysql import *   #连接mysql
from lxml import etree  #xpath
import re               # 正则
import json          #格式化
import random           #随机数
import pandas as pd     #数据清洗
from sqlalchemy import create_engine # 将数据导入数据库

engine = create_engine('mysql+pymysql://root:admin123@localhost:3306/dbm')

class spider(object):
    # 定义初始化方法
    def __init__(self):
        # 定义初始属性 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=20'
        self.spiderUtil= 'https://movie.douban.com/j/new_search_subjects?'
        self.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52"
        }

    # 定义初始函数
    def init(self):
        # 在初始化的时候，先创建一个csv文件，方便爬取之后将未过滤未处理的数据暂时的存放到csv文件
        # 如果这个路径不存在
        if not os.path.exists('./tempData.csv'):
            # 新建一个./tempData.csv 写入 ‘’
            with open('./tempData.csv','w',newline='') as writer_f:
                writer = csv.writer(writer_f)
                # 写入字段
                writer.writerow(['directors','rate','title','casts','detailLink','year','types','country','lang','time','moveiTime','comment_len','starts','summary','imgList','movieUrl'])

        if not os.path.exists('./getDataPage.txt'):
            with open('./getDataPage.txt','w',encoding='utf-8') as f:
                f.write('0\n')


        try:
            conn = connect(host='localhost', user='root', password='admin123', database='dbm', port=3306,
                           charset='utf8mb4')
            sql = '''
                                create table movie(
                                    id int primary key auto_increment,
                                    directors varchar(255),
                                    rate varchar(255),
                                    title varchar(255),
                                    casts varchar(255),
                                    detailLink varchar(255),
                                    year varchar(255),
                                    types varchar(255),
                                    country varchar(255),
                                    lang varchar(255),
                                    time varchar(255),
                                    moveiTime varchar(2555),
                                    comment_len varchar(2555),
                                    starts varchar(2555),
                                    summary varchar(2555),
                                    imgList varchar(2555),
                                    movieUrl varchar(255)
                            )
                            '''
            # 初始化一个游标
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except:
            pass

    # 查询现在页码
    def get_page(self):
        with open('./getDataPage.txt','r') as r_f:
            return r_f.readlines()[-1].strip()

    # 记录新页码
    def set_page(self,newPage):
        with open('./getDataPage.txt', 'a') as w_f:
            w_f.write(str(newPage) + '\n')

    # 定义爬虫主函数
    def spiderMain(self):
        page = self.get_page()
        params = {
            'start':int(page) * 20
        }
        print('正在爬取第{}页'.format(int(page) + 1))
        respJson = requests.get(self.spiderUtil,headers=self.headers,params=params).json()
        #print(respJson)                 # 200请求成功
        respJson = respJson['data']
        resultList = []

        try:
            for index, movieData in enumerate(respJson):
                print('正在爬取第%d条' % (index + 1))
                # print(movieData)
                resultData = []
                # 电影导演 directors
                resultData.append(','.join(movieData['directors']))
                # 电影评分 rate
                resultData.append(movieData['rate'])
                # 电影名字 title
                resultData.append(movieData['title'])
                # print('title:',movieData['title'])
                # 电影演员 casts
                resultData.append(','.join(movieData['casts']))
                # 电影详情链接 url
                resultData.append(movieData['url'])

                respDetailHTML = requests.get(movieData['url'], headers=self.headers)
                respDetailHTMLXpath = etree.HTML(respDetailHTML.text)

                # 电影年份 year
                year = re.search('\d+', respDetailHTMLXpath.xpath('//*[@id="content"]/h1/span[2]/text()')[
                    0]).group()  # 用xpath语法查询目的标签  /text():获取该标签内的文本
                resultData.append(year)
                # 电影类型 types
                types = []
                for i in respDetailHTMLXpath.xpath('//*[@id="info"]/span[@property="v:genre"]'):
                    types.append(i.text)
                resultData.append(','.join(types))
                # 电影制片国家 country
                textInfo = respDetailHTMLXpath.xpath('//*[@id="info"]/text()')
                texts = []
                for i in textInfo:
                    if i.strip() and not i.strip() == '/':  # .strip()：去掉两边空格
                        texts.append(i)
                resultData.append(','.join(texts[0].split(sep='/')))
                # 语言 lang
                resultData.append(','.join(texts[1].split(sep='/')))
                # 上映时间 time
                time = respDetailHTMLXpath.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/@content')[0][:10]
                resultData.append(time)
                # print('time:',time)
                # 片长 moveiTime
                try:
                    moveiTime = respDetailHTMLXpath.xpath('//*[@id="info"]/span[@property="v:runtime"]/@content')[0]
                    resultData.append(moveiTime)
                except:
                    try:
                        resultData.append(re.search('\d+', texts[4]).group())
                    except:
                        resultData.append(random.randint(31, 69))  # random.randint(31,69) 给随机数
                # 短评个数 comment_len
                comment_len = re.search('\d+', respDetailHTMLXpath.xpath(
                    '//*[@id="comments-section"]/div[@class="mod-hd"][1]/h2//a/text()')[0]).group()
                resultData.append(comment_len)
                # print(comment_len)
                # 电影星级占比 starts
                starts = []
                for i in respDetailHTMLXpath.xpath(
                        '//div[@id="interest_sectl"]//div[@class="ratings-on-weight"]/div[@class="item"]'):
                    starts.append(i.xpath('./span[@class="rating_per"]/text()')[0])
                resultData.append(','.join(starts))
                # 电影简介 summary
                summary = respDetailHTMLXpath.xpath('//span[@property="v:summary"]/text()')[0].strip()
                resultData.append(summary)
                # print('简介',summary)
                # 图片列表 imgList
                imgList = respDetailHTMLXpath.xpath('//ul[contains(@class,"related-pic-bd  ")]//img/@src')
                resultData.append(','.join(imgList))
                # print(resultData[-1])
                # 电影预告片链接 movieUrl
                try:
                    movieUrl = respDetailHTMLXpath.xpath(
                        '//ul[contains(@class,"related-pic-bd  ")]/li[@class="label-trailer"]/a/@href')[0]
                    movieHTML = requests.get(movieUrl, headers=self.headers)
                    movieHTMLXpath = etree.HTML(movieHTML.text)
                    resultData.append(movieHTMLXpath.xpath('//video/source/@src')[0])
                except:
                    resultData.append(0)

                # print(resultData)
                resultList.append(resultData)
        except:
            pass

        self.save_to_csv(resultList)
        self.set_page(int(page) + 1)
        self.clear_csv()
        self.spiderMain()

    # 数据存储
    def save_to_csv(self,resultList):
        with open('./tempData.csv','a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            for rowData in resultList:
                writer.writerow(rowData)

    # 数据清洗
    def clear_csv(self):
        df = pd.read_csv('./tempData.csv')
        # print(df.shape)       # 查看有几行几列
        # print(df.isnull())      # 查看是否有缺失值
        df.dropna(inplace=True)   # 丢弃空值
        df.drop_duplicates      #删除重复值

        self.save_to_sql(df)

    def save_to_sql(self,df):
        pd.read_csv('./tempData.csv')
        # 表名 连接驱动 不要索引 如果存在
        df.to_sql('movie',engine,index=False,if_exists='append')

if __name__ == '__main__':
    # 实例化对象
    spiderObj = spider()
    spiderObj.init()
    spiderObj.spiderMain()
    # spiderObj.clear_csv()