import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# 图片显示中文
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

# 读取csv文件
df = pd.read_csv('data/newData.csv')

# 获取类型列数据并转换为字符串
text = ' '.join(df['类型'].values)

# 统计词频
word_counts = Counter(text.split())

# 获取词频最高的前10个词
top_words = word_counts.most_common(10)

# 绘制扇形图
labels, values = zip(*top_words)
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.axis('equal')
plt.show()
