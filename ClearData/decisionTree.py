import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = pd.read_csv(r'data/basicData.csv')

# 将星级占比列中的百分比字符串转换为浮点数
data['星级占比'] = data['星级占比'].apply(lambda x: [float(i.strip('%'))/100 for i in x.split(',')])

# 删除缺失值
data.dropna(inplace=True)

# 将非数值特征转换为数值特征
data = pd.get_dummies(data, columns=['作者', '电影名', '类型', '地区', '语言'])

# 划分数据集
X = data.drop('分数', axis=1)
y = data['分数']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 构建决策树模型
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# 模型评估
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

