# author: xiaobei
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
# local import
from draw_tree import createPlot
from rough_set import rough_set


# 计算信息熵
def cal_information_entropy(data):
    data_label = data.iloc[:, -1]
    label_class = data_label.value_counts()  # 总共有多少类
    Ent = 0
    for k in label_class.keys():
        p_k = label_class[k] / len(data_label)
        Ent += -p_k * np.log2(p_k)
    return Ent


# 计算给定数据属性a的信息增益
def cal_information_gain(data, a):
    Ent = cal_information_entropy(data)
    feature_class = data[a].value_counts()  # 特征有多少种可能
    gain = 0
    for v in feature_class.keys():
        weight = feature_class[v] / data.shape[0]
        Ent_v = cal_information_entropy(data.loc[data[a] == v])
        gain += weight * Ent_v
    return (Ent - gain)


# 获取标签最多的那一类
def get_most_label(data):
    data_label = data.iloc[:, -1]
    label_sort = data_label.value_counts(sort=True)
    return label_sort.keys()[0]


# 挑选最优特征，即信息增益最大的特征
def get_best_feature(data):
    features = data.columns[:-1]
    res = {}
    for a in features:
        temp = cal_information_gain(data, a)
        res[a] = temp
    res = sorted(res.items(), key=lambda x: x[1], reverse=True)
    # print('当前最大信息增益：', res[0][0], res[0][1], end='\n')
    return res[0][0]


##将数据转化为（属性值：数据）的元组形式返回，并删除之前的特征列
def drop_exist_feature(data, best_feature):
    attr = pd.unique(data[best_feature])
    new_data = [(nd, data[data[best_feature] == nd]) for nd in attr]
    new_data = [(n[0], n[1].drop([best_feature], axis=1)) for n in new_data]
    return new_data


# 创建决策树
def create_tree(data):
    data_label = data.iloc[:, -1]
    if len(data_label.value_counts()) == 1:  # 只有一类
        return data_label.values[0]
    if all(len(data[i].value_counts()) == 1 for i in data.iloc[:, :-1].columns):  # 所有数据的特征值一样，选样本最多的类作为分类结果
        return get_most_label(data)
    best_feature = get_best_feature(data)  # 根据信息增益得到的最优划分特征
    Tree = {best_feature: {}}  # 用字典形式存储决策树
    exist_vals = pd.unique(data[best_feature])  # 当前数据下最佳特征的取值
    if len(exist_vals) != len(column_count[best_feature]):  # 如果特征的取值相比于原来的少了
        no_exist_attr = set(column_count[best_feature]) - set(exist_vals)  # 少的那些特征
        for no_feat in no_exist_attr:
            Tree[best_feature][no_feat] = get_most_label(data)  # 缺失的特征分类为当前类别最多的

    for item in drop_exist_feature(data, best_feature):  # 根据特征值的不同递归创建决策树
        Tree[best_feature][item[0]] = create_tree(item[1])
    return Tree


def predict(Tree, test_data):
    first_feature = list(Tree.keys())[0]
    second_dict = Tree[first_feature]
    input_first = test_data.get(first_feature)
    input_value = second_dict[input_first]
    if isinstance(input_value, dict):  # 判断分支还是不是字典
        class_label = predict(input_value, test_data)
    else:
        class_label = input_value
    return class_label


def give_dict(title, vaulelist):
    dic = dict(zip(title, vaulelist))
    return dic


# 计算精度和混淆矩阵
def test_acc_confu(dicision_Tree, test_data):
    total_test = test_data.shape[0]
    labels = test_data['Outcome']
    values = test_data[select_col[:-1]]
    TN = 0
    TP = 0
    FP = 0
    FN = 0
    right = 0
    i = 0
    for ins in values.values:
        dic = give_dict(select_col, ins)
        # print(dic)
        result = predict(dicision_Tree, dic)
        if result == labels.values[i]:
            right += 1
            if labels.values[i] == '1':
                TP += 1
            else:
                TN += 1
        else:
            if labels.values[i] == '0' and result == '1':
                FN += 1
            else:
                FP += 1
        i += 1
    acc = right / total_test
    return acc, TN, TP, FN, FP


if __name__ == '__main__':
    # 计算属性依赖度
    raw_data = pd.read_csv(r'D:\PyCharm 2020.1.1\project\roughset\dataset\archive\news_data.csv')
    dependency = rough_set(raw_data)
    select_col = ['Pregnancies', 'Glucose', 'Insulin', 'BMI',
                  'Outcome']
    # select_col = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI',
    #                'DiabetesPedigreeFunction', 'Age',
    #                'Outcome']
    # 读取数据
    data = pd.read_csv(r'D:\PyCharm 2020.1.1\project\roughset\dataset\archive\train_data.csv')
    data = data[select_col]
    # 统计每个特征的取值情况作为全局变量
    column_count = dict([(ds, list(pd.unique(data[ds]))) for ds in data.iloc[:, :-1].columns])

    # 创建决策树
    dicision_Tree = create_tree(data)
    print(dicision_Tree)
    # 测试数据
    # test_data_2 = {'Glucose': 'high', 'BloodPressure': 'norm', 'Insulin': 'low', 'BMI': 'obesity'}
    # result = predict(dicision_Tree, test_data_2)
    # print('分类结果为' + '不患病' if result == 1 else '患病')
    # 绘制决策树
    createPlot(dicision_Tree)
    test_data = pd.read_csv(r'D:\PyCharm 2020.1.1\project\roughset\dataset\archive\test_data.csv')
    test_data = test_data[select_col]
    acc, TN, TP, FN, FP = test_acc_confu(dicision_Tree, test_data)
    print('acc:', acc)
    print([[TN, FP], [FN, TP]])
