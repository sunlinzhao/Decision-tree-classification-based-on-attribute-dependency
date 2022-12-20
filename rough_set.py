# author: xiaobei
# _*_coding:utf-8 _*_

import pandas as pd
import time


def basic_set(df):
    basic = {}
    for i in df.drop_duplicates().values.tolist():
        basic[str(i)] = []
        for j, k in enumerate(df.values.tolist()):
            if k == i:
                basic[str(i)].append(j)

    return basic


def rough_set(data):
    data = data.dropna(axis=0, how='any')  # 去空值
    x_data = data.drop(['Outcome'], axis=1)
    y_data = data.loc[:, 'Outcome']
    # 决策属性基本集
    y_basic_set = sorted([v for k, v in basic_set(y_data).items()])
    # 条件属性基本集
    x_basic_set = sorted([v for k, v in basic_set(x_data).items()])
    pos = []
    for i in x_basic_set:
        for j in y_basic_set:
            if set(i).issubset(j):
                pos.append(i)
    pos.sort()
    print("x_basic_set", x_basic_set)
    print("y_basic_set", y_basic_set)
    print('y的x正域Pos_x(y): ', pos)
    r_x_y = len([k for i in pos for k in i]) / (len(data))
    print('依赖度r_x_(y):', r_x_y)

    # 探索条件属性中不可省关系
    u = locals()
    pos_va = locals()
    r = locals()
    columns_num = list(range(len(x_data.columns)))
    # 收集核
    imp_core = []
    # 收集属性重要性
    imp_attr = []
    for i in columns_num:
        c = columns_num.copy()
        c.remove(i)
        u = data.iloc[:, c]
        u = sorted([v for k, v in basic_set(u).items()])
        pos_va = []
        for k in u:
            for j in y_basic_set:
                if set(k).issubset(j):
                    pos_va.append(k)
        if sorted(pos_va) != pos:
            imp_core.append(i)
        r = len(sorted(pos_va)) / len(data)
        r_diff = round(r_x_y - r, 4)

        imp_attr.append(r_diff)

    dict_imp = {}
    for o, p in enumerate(imp_attr):
        dict_imp[data.columns[o]] = p

    result = dict_imp
    sorted_dict_imp = sorted(dict_imp, key=lambda x: dict_imp[x], reverse=True)
    sorted_dict_imp = list(map(lambda x: {x: dict_imp[x]}, sorted_dict_imp))
    imp_core = [data.columns[i] for i in imp_core]

    print('属性重要度为:', sorted_dict_imp)
    print('核属性为：', imp_core)#核属性仅供参考

    return result


def deal(data):
    # 获取数据长度
    len = data.iloc[:, 0].size
    # 将数据划分
    if len % 500 != 0:
        if len > 500:
            num = len // 500 + 1
        else:
            num = 1
    else:
        if len > 500:
            num = int(len / 500)
        else:
            num = 1
    arr = [[]] * num

    count = 0
    for i in arr:
        # 如果数少于500或者最后一部分数少于500，则放入一个由数长决定的数组
        if num == 1:
            arr[count] = data.iloc[0:len]  # 取500开始，取
        elif count == num - 1:
            arr[count] = data.iloc[500 * count:len]
        else:
            arr[count] = data.iloc[500 * count:(count + 1) * 500]
        count = count + 1
    sorted_dict_imp = [[]] * num
    total = [0] * 8
    title = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction',
             'Age']
    count = 0
    for i in arr:
        print('-------------------------------------第%d个数据集数据-----------------------------------------' % (count + 1))
        sorted_dict_imp[count] = rough_set(i)
        count = count + 1
    count1 = 0
    # 将dict的key为C1-Cn的value存入total中保存,并且相加
    for i in sorted_dict_imp:
        count = 0
        if count1 == 0:
            for j in title:
                total[count] = i.get(j)
                count = count + 1
        else:
            for z in title:
                total[count] = i.get(z) + total[count]
                count = count + 1
        count1 = count1 + 1
    # 输出最终C1-Cn的结果
    count = 0
    for i in title:
        print(i, ':', round(total[count], 4))
        count = count + 1


def main():
    time1 = time.time()
    # 读取文件数据
    data = pd.read_csv(filepath_or_buffer=r'D:\PyCharm 2020.1.1\project\roughset\dataset\archive\news_data.csv', encoding='utf-8')
    deal(data)
    time2 = time.time()
    # print(time2 - time1)


if __name__ == '__main__':
    main()
