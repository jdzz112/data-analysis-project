# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
from IPython import get_ipython

#%% [markdown]
# ## 数据收集

#%%
#导入模块
import numpy as np
import pandas as pd
import requests
import json 
import csv
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


#%%
#查看tweet_json.txt信息，将json数据转换为pd.dataFrame
tweet_list=[]
with open('tweet_json.txt','r') as f:
    f_list=f.readlines()
    for f_l in f_list:
        js_line=json.loads(f_l)
        tweet_list.append(js_line)
columns=tweet_list[0].keys()
tweet_csv=pd.DataFrame(tweet_list,columns=columns)
tweet_csv.to_csv('tweet.csv',index=False)
tweet_csv.head(3)


#%%
#下载image-predictions数据
url='https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
re=requests.get(url)
file=re.content.decode('utf-8')
with open('image-predictions.txt','w') as f:
    f.write(file)


#%%
#查看image-predictions.tsv.txt信息
image_pre=pd.read_csv('image-predictions.txt',sep='\t')
image_pre.head(4)


#%%
#加载twitter-archive-enhanced.csv信息
tw_archive_raw=pd.read_csv('twitter-archive-enhanced.csv')

#%% [markdown]
# ## 数据评估

#%%
#截取所需id_str、retweet_count、favorite_count列组成新pd.dataframe
tweet_csv_clean=tweet_csv.loc[:,['id_str','retweet_count','favorite_count']].copy()
tweet_csv_clean.head(3)


#%%
#查看tweet_csv_clean信息
tweet_csv_clean.info()


#%%
#查看tweet_csv_clean是否重复
tweet_csv_clean.duplicated().value_counts()


#%%
#截取要的tweet_id、p1、p2、p3列组成新pd.dataframe
image_pre_clean=image_pre.loc[:,['tweet_id','p1','p2','p3']].copy()
image_pre_clean.head(3)


#%%
#查看image_pre_clean信息
image_pre_clean.info()


#%%
#查看image_pre_clean重复信息
image_pre_clean.duplicated().value_counts()


#%%
#查看twitter-archive-enhanced.csv信息
tw_archive_raw.sample(5)


#%%
tw_archive_raw.info()


#%%
#查看tw_archive重复信息
tw_archive_raw.duplicated().value_counts()


#%%
#查看狗狗rating_numerator信息
tw_archive_raw['rating_numerator'].value_counts()


#%%
#查看狗狗rating_denominator信息
tw_archive_raw['rating_denominator'].value_counts()


#%%
#查看狗狗等级doggo信息
tw_archive_raw['doggo'].value_counts()


#%%
#查看狗狗等级floofer信息
tw_archive_raw['floofer'].value_counts()


#%%
#查看狗狗等级pupper信息
tw_archive_raw['pupper'].value_counts()


#%%
#查看狗狗等级puppo信息
tw_archive_raw['puppo'].value_counts()


#%%
#查看狗狗等级重复记录信息
tw_archive_raw[(tw_archive_raw['doggo']!='None')][tw_archive_raw[(tw_archive_raw['doggo']!='None')].floofer!='None']


#%%
#拷贝数据
tw_archive=tw_archive_raw.copy()

#%% [markdown]
# #### 质量问题
# ##### image_pre_clean
# - tweet_id为non-null int64类型
# 
# ##### tw_archive
# - tweet_id为non-null int64类型
# - timestamp为non-null object类型
# - in_reply_to_status_id、in_reply_to_user_id为non-null float64类型
# - dog等级信息doggo、floofer、pupper、puppo记录有重复
# - 狗狗rating_numerator,rating_numerator数据不全
# - 有retweeted的记录
# - 包含没有狗狗图片的记录
# 
# #### 清洁度问题
# - 推特信息分布在不同的表
# - dog等级信息由doggo、floofer、pupper、puppo四列记录
#             
#%% [markdown]
# ## 清理
# 
# #### 质量问题
# - ##### image_pre_clean：tweet_id为non-null int64类型
# - ##### tw_archive：tweet_id为non-null int64类型；in_reply_to_status_id、in_reply_to_user_id为non-null float64类型
# 
# #### 解决方案
# - 通过pd.astype()转换pd.dataframe数据格式

#%%
#将image_pre_clean的tweet_id转换为str类型
image_pre_clean.tweet_id=image_pre_clean.tweet_id.astype(str)
image_pre_clean.info()


#%%
#将tw_archive的tweet_id、in_reply_to_status_id、in_reply_to_user_id、retweeted_status_id、retweeted_status_user_id转换为str类型
tw_archive[['tweet_id','in_reply_to_status_id','in_reply_to_user_id']]=tw_archive[['tweet_id','in_reply_to_status_id','in_reply_to_user_id']].astype(str)
tw_archive.info()

#%% [markdown]
# #### 质量问题
# - ##### tw_archive：timestamp为non-null object类型
# 
# #### 解决方案
# - 通过pd.to_datetime()将字符转换为日期格式

#%%
#将tw_archive的timestamp、retweeted_status_timestamp转换为datetime类型
tw_archive['timestamp']=pd.to_datetime(tw_archive['timestamp'],format='%Y-%m-%d %H:%M:%S')
tw_archive.info()

#%% [markdown]
# #### 质量问题
# - 狗狗rating_numerator,rating_numerator数据不全
# 
# #### 解决方案
# - 通过正则表达式提取评分信息，将新数据赋值给rating_numerator，通过正则表达式提取评分信息，将新数据赋值给rating_denominator

#%%
tw_archive['rating_numerator']=tw_archive.text.str.extract('((?:\d+\.)?\d+)\/', expand=True).astype(float)
tw_archive['rating_numerator'].value_counts()


#%%
tw_archive['rating_denominator']=tw_archive.text.str.extract('\/(\d+)', expand=True).astype(float)
tw_archive['rating_denominator'].value_counts()


#%%
tw_archive.info()

#%% [markdown]
# #### 质量问题
# - ##### 有retweeted的记录
# 
# #### 解决方案
# - 通过pd.drop()删除retweeted_status_id非空值的行，再将'retweeted_status_id', 'retweeted_status_user_id', 'retweeted_status_timestamp'列删除

#%%
tw_archive.drop(tw_archive[tw_archive['retweeted_status_id'].isnull()==False].index,axis=0,inplace=True)
tw_archive.drop(['retweeted_status_id', 'retweeted_status_user_id', 'retweeted_status_timestamp'],axis=1,inplace=True)
tw_archive.info()

#%% [markdown]
# #### 质量问题
# - dog等级信息doggo、floofer、pupper、puppo记录有重复
# 
# #### 清洁度问题
# - dog等级信息由doggo、floofer、pupper、puppo四列记录
# 
# #### 解决方案
# - 构建新列rank，将doggo、floofer、pupper、puppo四列非空值写入，如果记录有重复，保留等级高的记录，去除doggo、floofer、pupper、puppo四列     

#%%
#将tw_archive中狗狗等级信息拼为一列
tw_archive['rank']=tw_archive[tw_archive['doggo']!='None']['doggo']
tw_archive.loc[tw_archive['rank'].isnull(),'rank']=tw_archive[tw_archive['floofer']!='None']['floofer']
tw_archive.loc[tw_archive['rank'].isnull(),'rank']=tw_archive[tw_archive['pupper']!='None']['pupper']
tw_archive.loc[tw_archive['rank'].isnull(),'rank']=tw_archive[tw_archive['puppo']!='None']['puppo']
tw_archive.drop(['doggo','floofer','pupper','puppo'],axis=1,inplace=True)
tw_archive.info()

#%% [markdown]
# #### 质量问题
# - tw_archive表包含没有狗狗图片的记录
# 
# #### 清洁度
# - 推特信息分布在不同的表
# 
# #### 解决方案
# - 通过pd.merge()函数，以weet_id为键，进行inner join连接表信息,不将没有狗狗图片的记录保留

#%%
#将数据连接为一张表
df_clean=pd.merge(tw_archive,tweet_csv_clean,left_on='tweet_id',right_on='id_str')
df_clean=pd.merge(df_clean,image_pre_clean,on='tweet_id')
df_clean.drop(['id_str'],axis=1,inplace=True)

#%% [markdown]
# ## 评估整合后的数据

#%%
df_clean.sample(20)


#%%
df_clean.info()


#%%
df_clean.describe()


#%%
df_clean[df_clean['rating_numerator']>20]


#%%
df_clean.sort_values(['rating_numerator'],ascending=False)


#%%
df_clean[df_clean['rating_denominator']>10]


#%%
df_clean[df_clean['rating_denominator']>10].tweet_id.count()

#%% [markdown]
# #### 质量问题
# - rating_numerator有大于20的值
# - rating_denominator有大于10的值
# 
# ## 清理
# #### 质量问题
# - rating_numerator有大于20的值
# - rating_denominator有大于10的值
# 
# #### 解决方案
# - rating_denominator理论上值均为10，数据有1994条记录，推主评分rating_denominator理论值为10，异常数据仅仅16条，数量极少，故将异常数据删除；rating_numerator是推主给的评分，主观性强，故不予处理

#%%
#rating_denominator理论上值均为10，需要将异常数据删除去除rating_denominator异常数据
df_clean.drop(df_clean[df_clean['rating_denominator']!=float(10)].index,axis=0,inplace=True)
df_clean.describe()

#%% [markdown]
# ## 初步清理数据，保存数据

#%%
#保存数据
df_clean.to_csv('twitter_archive_master.csv',index=False)

#%% [markdown]
# ## 数据探索
# #### 狗狗评分分布

#%%
# 将rating_numerator分组统计
level_list= [ 0,10 ,11,12,13,14,1776 ] 
level= [str(i) for i in range(10,14)]
level.insert(0,'<10')
level.append('>13')
df_clean['favour_levels'] = pd.cut(df_clean['rating_numerator'],level_list,labels=level,right = False)
favour=df_clean.groupby(['favour_levels']).favour_levels.count()
favour


#%%
#计算比例
ratio_favour=favour/df_clean.favour_levels.count()
ratio_favour


#%%
#作饼图
plt.pie(x=ratio_favour, labels=ratio_favour.index,autopct='%.2f')
plt.title('percentage of rating_numerator(%)');

#%% [markdown]
# #### tweet 点赞转发比

#%%
#计算favorite与retweet的比例
f_r_ratio=df_clean['favorite_count']/df_clean['retweet_count']
f_r_ratio.describe()


#%%
# 将f_r_ratio分组统计
level_list=range(14)
level=[str(x) for x in range(1,14)]
f_r_level= pd.cut(f_r_ratio,level_list,labels=level,right = False)
f_r_count=f_r_level.value_counts()
f_r_count


#%%
#作直方图
plt.hist(f_r_ratio,bins=np.arange(1,13,1))
plt.xlabel('ratio')
plt.ylabel('counts')
plt.title('ratio of favorite and retweet');

#%% [markdown]
# #### 预测的狗狗品种

#%%
#预测的狗狗种类
df_clean.p1.value_counts().iloc[0:3,]


#%%



#%%


