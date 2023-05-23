import pandas as pd
#数据导入
df = pd.read_csv(r'./data.csv',names=['作者','分数','电影名','年份','类型','地区','语言','时长','评论人数','星级占比'],sep=',')

import pandas as pd

# 读取csv文件
df = pd.read_csv(r'./data.csv')

# 选择需要的列
df = df[['directors', 'rate', 'title', 'year', 'types', 'country', 'lang', 'moveiTime','comment_len','starts']]

# 重命名列
df = df.rename(columns={'directors':'作者', 'rate':'分数', 'title':'电影名', 'year':'年份', 'types':'类型', 'country':'地区', 'lang':'语言', 'moveiTime':'时长','comment_len':'评论人数','starts':'星级占比'})

# 提取电影信息
df['作者'] = df['电影名'].apply(lambda x: x.split('(')[-1].replace(')', '').split(',')[0].strip())
df['年份'] = df['电影名'].apply(lambda x: x.split('(')[-1].replace(')', '').split(',')[-1].strip())
df['电影名'] = df['电影名'].apply(lambda x: x.split('(')[0].strip())
df['演员'] = df['电影名'].apply(lambda x: x.split(') ')[-1].strip())
df['类型'] = df['电影名'].apply(lambda x: x.split(') ')[0].split(' (')[1].strip())
df['地区'] = df['电影名'].apply(lambda x: x.split(') ')[0].split(' (')[0].strip())
df['语言'] = df['电影名'].apply(lambda x: x.split(') ')[-2].strip())
df['时长'] = df['电影名'].apply(lambda x: x.split(') ')[-3].strip())

# 选择需要的列
df = df[['作者', '分数', '电影名', '演员', '年份', '类型', '地区', '语言', '时长', '评论人数', '星级']]

# 去除缺失数据的行
df = df.dropna()

# 将处理后的数据保存为csv文件
df.to_csv('processed_data.csv', index=False)