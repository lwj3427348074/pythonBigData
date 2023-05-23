import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取csv文件
df = pd.read_csv('data/newData.csv')

# 获取类型列数据并转换为字符串
text = ' '.join(df['类型'].values)

# 生成词云
# wordcloud = WordCloud(width=800, height=600).generate(text)

wordcloud = WordCloud(width=800, height=600, font_path='控制面板/外观和个性化/字体/SIMYOU.TTF').generate(text)

# 显示词云
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
