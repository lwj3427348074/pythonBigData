import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# 读取CSV文件
data = pd.read_csv(r'data/basicData.csv')

# 数据预处理
data = data.drop(['作者','电影名', '地区','星级占比','四星占比', '三星占比', '二星占比', '一星占比'], axis=1)
data = pd.get_dummies(data, columns=['年份','类型' ,'语言', '时长', '评论人数', '五星占比' ], drop_first=True)
X = data.drop('分数', axis=1)
y = data['分数']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 模型训练
model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
model.fit(X_train, y_train)

# 模型评估
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("均方误差（MSE）：", mse)

# 导入新数据并进行预测
new_data = pd.read_csv(r'data/test.csv')
da = new_data
new_data = pd.get_dummies(new_data, columns=['年份','类型' ,'语言', '时长', '评论人数', '五星占比' ], drop_first=True)

# 确保新数据集包含与训练数据集相同的特征列
missing_cols = set(X.columns) - set(new_data.columns)
if len(missing_cols) > 0:
    new_data = new_data.reindex(columns=new_data.columns.union(missing_cols))
    new_data[list(missing_cols)] = 0
new_data = new_data[X.columns]

new_y_pred = model.predict(new_data)
new_y_pred = np.round(new_y_pred, 1) # 将预测结果保留一位小数
print("新数据预测分数：", new_y_pred)

# 将电影名作为x轴，电影评分作为y轴
x = da['电影名']
y_true = da['分数']
y_pred = new_y_pred

# 图片显示中文
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
# 画出折线图
# plt.figure(figsize=(9, 6))#3:2
# 底部边距
plt.subplots_adjust(bottom=0.25)
# 旋转45度
plt.xticks(rotation=60)
# 蓝色
plt.plot(x, y_true, label='实际分数')
plt.plot(x, y_pred, label='预测分数')
plt.xlabel('电影名')
plt.ylabel('分数')
plt.title('电影评分预测结果')
plt.legend()
plt.show()