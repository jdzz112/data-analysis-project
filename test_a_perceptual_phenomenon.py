# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
from IPython import get_ipython


#%%
# 在这里执行你的分析
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
df=pd.read_csv('stroopdata.csv')
df.head()


#%%
df.isnull().sum()


#%%
df.describe()

#%% [markdown]
# 数据集中没有空值，一共24位参与者。Congruent组均值为14.0511，标准差为3.5594，最小值为8.6300，中位数为14.3565，最大值为22.3280；
# Incongruent组均值为22.0159，标准差为4.7971，最小值为15.6870，中位数为21.0175，最大值为35.2550。Congruent组各项指标均小于Incongruent组。
#%% [markdown]
# (4) 提供显示样本数据分布的一个或两个可视化。用一两句话说明你从图中观察到的结果。

#%%
# 在这里创建可视化图表
df.plot(kind='box',title='Time to describe color')
plt.ylabel('time')
plt.xlabel('Is congruent');

#%% [markdown]
# 用参与者在一致文字条件，和不一致文字条件条件下说出墨色时间作箱线图，可以看到在不一致文字条件条件下说出墨色时间有偏大的离群值，其用时四分位数位数大于在一致文字条件条件下说出墨色时间，暗示参与者在一致文字条件比不一致文字条件条件下说出墨色平均时间更短。
#%% [markdown]
# (5) 现在，执行统计测试并报告你的结果。你的置信水平和关键统计值是多少？你是否成功拒绝零假设？对试验任务得出一个结论。结果是否与你的期望一致？

#%%
# 在这里执行统计检验
con=df['Congruent'].values.tolist()
incon=df['Incongruent'].values.tolist()
stats.ttest_rel(con,incon)


#%%
stats.t.isf(0.95, df=23)

#%% [markdown]
#  由于样本数据是参与者在不同受试条件下的反应数据，两组数据间存在对应关系，且样本容量为24，不够大，所以进行配对样本 t 检验。H0：μ1=μ2，H1：μ1<>μ2，需要进行双尾检验。
#  
# 经计算在自由度为23下，p-value=4.1030005857111781e-08<α=0.05,所以拒绝H0，接受H1，认为人在一致文字条件，和不一致文字条件条件下说出墨色时间不同。由于参与者在一致文字条件比不一致文字条件条件下说出墨色平均时间更短，所以可以做出推论：人在一致文字条件比不一致文字条件条件下说出墨色用时更短。
# 计算可知在95%置信水平下自由度为23时， t 临界值为-1.7138715277470473大于样本 t 临界值-8.020706944109957。
