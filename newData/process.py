# -*- codeing = utf-8 -*-
# @Time : 2022/11/13 11:07
# @Author : ggboy
# @File : process.py
# @Software : PyCharm

import pandas as pd
import re
from pandas import DataFrame

#数据处理
#数据导入
df = pd.read_csv(r'./data.csv',names=['电影名','分数','评论人数','五星占比','四星占比','同类对比',],sep=',')

#数据清洗
#去重
df = df.drop_duplicates('电影名')
#去空 以0填充
df = df.fillna(0)
#处理数据中的空格与字符
df0 = df.copy()
df0['四星占比'] = df['四星占比'].str.replace(' ','')
df0['四星占比'] = df0['四星占比'].str.replace(r'\n','')
df0['四星占比'] = df0['四星占比'].str.replace(r'4星','')
df0['四星占比'] = df0['四星占比'].str.replace(r'%','')
df0['五星占比'] = df['五星占比'].str.replace(' ','')
df0['五星占比'] = df0['五星占比'].str.replace(r'\n','')
df0['五星占比'] = df0['五星占比'].str.replace(r'5星','')
df0['五星占比'] = df0['五星占比'].str.replace(r'%','')


#查看列数据类型并转换
for i in list(df0.columns):
    if df0[i].dtype=='O':
        print(i)
df0['五星占比'] = df0['五星占比'].astype(float)
df0['四星占比'] = df0['四星占比'].astype(float)


#数据分析
#计算电影评分与其他数据的相关系数
for i in list(df0.columns):
    if df0[i].dtype != 'O' and i != '分数':
        x = df0['分数'].corr(df0[i])
        print(x)


#将清洗后的数据导出
df0.to_csv(r'./newData.csv')


