# author: xiaobei
from math import ceil, floor
import pandas as pd
from sklearn.model_selection import train_test_split
import os

# names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
# [怀孕 葡萄糖 血压 表皮厚度 胰岛素 体重指数 糖尿病谱系功能 年龄 结果]

# 读取数据
data = pd.read_csv(r'D:\PyCharm 2020.1.1\project\roughset\dataset\archive\diabetes.csv', header=0,
                   encoding='utf-8')
# 选取数据
select_col = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI',
              'DiabetesPedigreeFunction', 'Age',
              'Outcome']
data = data[select_col]

names = data.columns.tolist()[:-1]


def devide_Glucose(x):
    if x == 0:
        return None
    elif x < 60:
        return 'low'
    elif 60 <= x < 111:
        return 'norm'
    else:
        return 'high'


def devide_BloodPressure(x):
    if x == 0:
        return None
    elif x < 60:
        return 'low'
    elif 60 <= x < 90:
        return 'norm'
    else:
        return 'high'


def devide_Insulin(x):
    if x == 0:
        return None
    elif x < 25:
        return 'low'
    elif 25 <= x < 140:
        return 'norm'
    else:
        return 'high'


def devide_BMI(x):
    if x == 0:
        return None
    elif x < 20:
        return 'thin'
    elif 20 <= x < 25:
        return 'norm'
    elif 25 <= x < 30:
        return 'heavy'
    else:
        return 'obesity'


def devide_SkinThickness(x):
    if x == 0:
        return None
    elif x < 15:
        return 'low'
    elif 15 <= x < 45:
        return 'norm'
    else:
        return 'high'


def devide_DiabetesPedigreeFunction(x):
    if x == 0:
        return None
    elif x < 15:
        return 'low'
    elif 15 <= x < 20:
        return 'norm'
    else:
        return 'high'


def devide_Age(x):
    if x == 0:
        return None
    elif x < 35:
        return 'youth'
    elif 35 <= x < 50:
        return 'middle'
    else:
        return 'old'


def devide_Pregnancies(x):
    if x == 0:
        return 'never'
    elif x < 5:
        return 'less'
    else:
        return 'more'


for col in names:
    if col == 'Glucose':
        data[col] = data[col].map(devide_Glucose)
    elif col == 'BloodPressure':
        data[col] = data[col].map(devide_BloodPressure)
    elif col == 'Insulin':
        data[col] = data[col].map(devide_Insulin)
    elif col == 'BMI':
        data[col] = data[col].map(devide_BMI)
    elif col == 'SkinThickness':
        data[col] = data[col].map(devide_SkinThickness)
    elif col == 'DiabetesPedigreeFunction':
        data[col] = data[col].map(devide_DiabetesPedigreeFunction)
    elif col == 'Age':
        data[col] = data[col].map(devide_Age)
    elif col == 'Pregnancies':
        data[col] = data[col].map(devide_Pregnancies)
# 删除含有空值的行
data = data.dropna(axis=0, how="any")
# 删除重复数据
# data = data.drop_duplicates()
# a = floor(min(data[col].values))
# b = ceil(max(data[col].values))
# print(a, b)
# num_bin = x % 2 + 1
# x = x + 1
# bins = [x for x in range(a - 1, b + 1, (b - a + 1) // num_bin)]
# print(bins)
# labels = [y for y in range(1, len(bins))]
# # 利用pd.cut进行数据离散化切分 左开右闭
# col = 'rong'
# data[col] = pd.cut(data[col], bins=[1, 800], labels=['a'],
#                    include_lowest=False)

# 选取数据
# select_col = ['Glucose', 'Insulin', 'BMI', 'Outcome']
# data = data[select_col]
# 数据打乱
data = data.sample(frac=1.0)
# 划分训练集 为了数据均衡 分层抽样
df_train, df_test = train_test_split(data, test_size=0.25, stratify=data['Outcome'])

# 添加标识列
# data.insert(0, 'ID', range(0, 0 + len(data)))

# 写入数据到csv
# 获取表头
titles = data.columns.tolist()
print(titles)
data.to_csv(r'D:\PyCharm 2020.1.1\project\roughset\dataset\archive\news_data.csv', index=False, sep=',')
df_train.to_csv(r'D:\PyCharm 2020.1.1\project\roughset\dataset\archive\train_data.csv', index=False, sep=',')
df_test.to_csv(r'D:\PyCharm 2020.1.1\project\roughset\dataset\archive\test_data.csv', index=False, sep=',')

# 随机取0.1倍的数据
# data = data.sample(frac=0.02)
# select_col = ['ID', 'BloodPressure', 'Insulin', 'BMI', 'Outcome']
# data = data[select_col]

# with open(r'D:\PyCharm 2020.1.1\project\roughset\dataset\archive\news_data.csv', 'w+',
#           encoding='gbk') as f:
#     # 写入表头
#     for t in select_col:
#         f.write(t)
#         f.write(' ')
#     f.write('\n')
#
#     for line in data.values:
#         # print(line)
#         for elment in line:
#             f.write(str(elment))
#             f.write(' ')
#         f.write('\n')

# converters={'Pregnancies': int,
#                                'Glucose': int,
#                                'BloodPressure': int,
#                                'SkinThickness': int,
#                                'Insulin': int,
#                                'BMI': float,
#                                'DiabetesPedigreeFunction': float,
#                                'Age': int,
#                                'Outcome': int}
