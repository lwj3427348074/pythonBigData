# -*- codeing = utf-8 -*-
# @Time : 2022/11/1 12:41
# @Author : ggboy
# @File : crawler.py
# @Software : PyCharm

import requests
from lxml import etree
from pandas import DataFrame
import csv

# #配置代理池
# def get_proxy():
#     return requests.get("http://127.0.0.1:5010/get/").json()
#
# def delete_proxy(proxy):
#     requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
#
def getHtml(url,headers):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    print(proxy)
    while retry_count > 0:
        try:
            html = requests.get(url=url,headers=headers ,proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None


url1 = 'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&page_limit=50&page_start=0'

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
}

resp = getHtml(url1,headers)
dic = resp.json()


#从json中提取电影信息
for movie in dic['subjects']:
    mvUrl = movie['url']
    mvName = movie['title']

    print(mvName)
#每个电影页面爬取
    newRes = getHtml(mvUrl,headers=headers)
    tree = etree.HTML(newRes.text)

    block = tree.xpath('//*[@id="interest_sectl"]')
    for b in block:
        #分数
        score = b.xpath('./div[1]/div[2]/strong/text()')
        score = ''.join(score).strip()
        #评论人数
        commentPeople = b.xpath('./div[1]/div[2]/div[1]/div[2]/a/span/text()')
        commentPeople = ''.join(commentPeople).strip()
        #星级
        rate_five = b.xpath('./div[1]/div[3]/div[1]/span/text()')
        rate_four = b.xpath('./div[1]/div[3]/div[2]/span/text()')
        rate_five = ''.join(rate_five).strip()
        rate_four = ''.join(rate_four).strip()
        #同类比对
        betterThan = b.xpath('./div[2]/a/text()')
        betterThan = ''.join(betterThan).strip()

        print(rate_five)
        print(rate_four)
        print(betterThan)

        #数据存到列表
        list = [mvName,score,commentPeople,rate_five,rate_four,betterThan]

        #将爬取数据存放到csv文件中
        with open("data.csv", mode="a+", newline="", encoding="utf-8") as f:  # 文件对象 指定newline为空，否则每插入一行就有一个空行
            csvwriter = csv.writer(f)  # 基于文件对象构建csv写入对象
            csvwriter.writerow(list)