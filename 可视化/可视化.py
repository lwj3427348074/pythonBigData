import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv(r'./newData.csv',nrows =10)
x=df['电影名']

y1=df['分数']
y2=df['评论人数']
y3=df['五星占比']

plt.rcParams['font.sans-serif']=['SimHei']
#设置画布大小
plt.figure(figsize=(10,9))
input_str = input('请输入：1、查看分数折线图，2、查看评论人数柱形图，3、查看五星占比直方图')
if input_str == '1':
    plt.plot(x,y1,label='分数',color='r',marker='o')
    #设置网格线
    plt.grid(axis='y')
    #设置坐标轴标题
    plt.xlabel('电影名')
    plt.ylabel('分数')
    #设置X轴坐标字体大小
    plt.xticks(fontsize=5)
    plt.title('影视网站数据化可视分析')
    plt.show()
elif input_str == '2':
    #设置网格线
    plt.grid(axis='y',linestyle='--')
    #设置坐标轴标题
    plt.xlabel('电影名')
    plt.ylabel('评论人数')
    #设置图表标题
    plt.title('影视网站数据化可视分析')
    #设置文本标签
    for a,b in zip(x,y2):
        plt.text(a,b,format(b,','),ha='center',va='center',fontsize=12,color='b',alpha=0.9)
    #设置X轴坐标字体大小
    plt.xticks(fontsize=5)
    plt.bar(x,y2,width=0.5,alpha=0.5)
    plt.show()
elif input_str == '3':
    #设置坐标轴标题
    plt.xlabel('电影名')
    plt.ylabel('五星占比')
    #设置图表标题
    plt.title('影视网站数据化可视分析')
    #设置数据的区间
    bins=[0,10,20,30,40,50]
    plt.hist(y3,bins,facecolor='b',edgecolor='k')
    plt.show()
else:
    print('请按照规则进行输入！')
