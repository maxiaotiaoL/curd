import numpy as np
import pandas as pd


# arr = np.array(range(5))
# sr1 = pd.Series(arr,index=range(10,15))
# # print(arr)
# # print(sr1+sr1*2)
#
#
# print(sr1)
# # print(sr1[[10,11,13]])
# # print(sr1[1:2])
# print(np.power(sr1,2))
# print(sr1[sr1>=3])


"""
从字典创建Series：Series(dic), 
in运算：’a’ in sr、for x in sr
键索引：sr['a'], sr[['a', 'b', 'd']]
键切片：sr['a':'c']
其他函数：get('a', default=0)等
"""

import random
# dic = {'a':1,'b':2,'c':3,'d':4}
# print(dic)
# sr = pd.Series(dic)
# print(sr)
# print('a' in sr)
# print(sr['a'])
# print(sr[['a','b','d']])
#
# print(sr['b':'c'])
# print(sr.get('x',100))

# sr = pd.Series(np.arange(1,6))
# print(sr)
# print(dir(sr.loc))
# print(sr.loc.__dict__)
# print(sr.loc.axis)
# print(sr.loc.name)
# print(sr.loc.ndim)
# print(sr.loc.obj)

# sr1 = pd.Series([12,23,34,1], index=['c','a','d','e'])
# sr2 = pd.Series([11,20,10], index=['d','c','a',])
# print(sr1)
# # print(sr2)
# # print(sr1+sr2)
# sr3 = pd.Series([11,20,10,14], index=['d','c','a','b'])
# print(sr3)
# print(sr1.add(sr3,fill_value=0))
# print(sr1)

"""
dropna()		过滤掉值为NaN的行
fillna()		填充缺失数据
isnull()		返回布尔数组，缺失值对应为True
notnull()		返回布尔数组，缺失值对应为False
"""

# sr1 = pd.Series([1,2,3],index=['a','b','c'])
# sr2 = pd.Series([1,3,4],index=['a','c','d'])
#
# sr3 = sr1 + sr2
#
# print(sr3)
# print(sr3.dropna())
# print(sr3.fillna(100))
# print(sr3.isnull())
# print(sr3.notnull())

# df1 = pd.DataFrame({
#   'one':[1,2,3,4],
#   'two':[4,3,2,1]
# },index=['a','b','c','d'])
#
# print(df1.T)

# df2 = pd.DataFrame({
#     'one':pd.Series([1,2,3],index=['a','b','c']),
#     'two':pd.Series([1,2,3,4],index=['b','a','c','d'])
# })
#
# print(df2)

"""
index					获取索引
T						转置
columns					获取列索引
values					获取值数组
describe()				获取快速统计
"""

# df = pd.DataFrame({1:[1,2,3,4],2:[5,6,7,8]},)
# print(df)
#
# print(df.index)
#
# print(df[1:3])


# class Foo(object):
#     def __init__(self, age):
#         self.age = age
#
#     def __add__(self, other):
#         return self.age + other.age
#
# obj1 = Foo(18)
# obj2 = Foo(20)
#
# print(obj1 + obj2)  # 38


arr = np.array([[1,2], [3, 4], [5, 6]])
# print(arr)
# print(arr[[0, 1, 2], [0, 1, 0]])  # [1 4 5]
# print(arr[[0, 0], [1, 1]])  # [2 2]
# print(np.array([arr[0, 1], arr[0, 1]]))  # [2 2]


# a = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]])
# b = np.array([0, 2, 0, 1])
#
# print(a[[0,1,2,3], [0, 2, 0, 1]])

# a = np.array([[1,2], [3, 4], [5, 6]])
# bool_idx = a > 2
#
# print(a)
# print(bool_idx)
# print(a[bool_idx])

# print(np.float32(65))

a = np.arange(10)**3
