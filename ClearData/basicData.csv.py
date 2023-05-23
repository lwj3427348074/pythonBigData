import pandas as pd

# 读取csv文件
df = pd.read_csv(r'.././tempData.csv')
# data = pd.read_csv(r'data/basicData.csv')

# 选择需要的列并重命名
df = df[['directors', 'rate', 'title', 'year', 'types', 'country', 'lang', 'moveiTime', 'comment_len', 'starts']]
df = df.rename(columns={'directors': '作者', 'rate': '分数', 'title': '电影名', 'year': '年份', 'types': '类型', 'country': '地区', 'lang': '语言', 'moveiTime': '时长', 'comment_len': '评论人数', 'starts': '星级占比'})

# 拆分星级占比列并转换为小数
starts_df = df['星级占比'].str.split(',', expand=True).apply(lambda x: x.str.strip('%')).fillna(0).astype(float) / 100
starts_df.columns = ['五星占比', '四星占比', '三星占比', '二星占比', '一星占比']

# 将拆分后的占比列与原数据合并
df = pd.concat([df, starts_df], axis=1)

# 去除缺失数据的行
df = df.dropna()
df.to_csv('data/newData.csv', index=False, float_format='%.2f')
# 打乱数据
df = df.sample(frac=1, random_state=42)

# 将处理后的数据保存为csv文件
df.iloc[:100].to_csv('data/basicData.csv', index=False, float_format='%.2f')
df.iloc[100:].to_csv('data/test.csv', index=False, float_format='%.2f')