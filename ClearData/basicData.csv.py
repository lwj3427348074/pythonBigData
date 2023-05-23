import pandas as pd

# 读取csv文件
df = pd.read_csv(r'.././tempData.csv')
# data = pd.read_csv(r'data/basicData.csv')

# 选择需要的列并重命名
df = df[['directors', 'rate', 'title', 'year', 'types', 'country', 'lang', 'moveiTime', 'comment_len', 'starts']]
df = df.rename(columns={'directors': '作者', 'rate': '分数', 'title': '电影名', 'year': '年份', 'types': '类型', 'country': '地区', 'lang': '语言', 'moveiTime': '时长', 'comment_len': '评论人数', 'starts': '星级占比'})

# 去除缺失数据的行
df = df.dropna()

# 将处理后的数据保存为csv文件
df.to_csv('data/basicData.csv', index=False)
