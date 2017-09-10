# _*_coding:utf-8_*_
"""
# 
#对代理人的指标数据进行预测
#
"""
import time
import pandas as pd
import numpy as np
from .config import Config
from sklearn import cross_validation, cross_validation
from sklearn import linear_model
from sklearn import preprocessing

con = Config()


class Prdt:
    def __init__(self):
        self.df = con.getO()
        # 创建lr模型
        self.lr = linear_model.LogisticRegression()
        # self.reg = linear_model.Ridge()

    def zeroFill(self, saleNbr=None):
        """
        初始化代理人指标数值，
        对于没有数值的天数进行补零
        :return: 
        """
        # 定义day_id范围
        day_id_index = range(1, 92)
        # 对数据进行重新整理
        # df = self.df.drop('sale_nbr', axis=1)
        if saleNbr is None:
            df = self.df.drop('sale_nbr', axis=1)
        else:
            df = self.df[self.df.sale_nbr == saleNbr]
            df = df.drop('sale_nbr', axis=1)
        # 筛选出来表中存在的数据
        day_id = df.day_id.drop_duplicates()
        # 比较两个不同的数据
        diff = set(day_id_index) ^ set(list(day_id))
        # 对源数据没有的day_id进行补零处理
        for i in diff:
            insertRow = pd.DataFrame([[i, 0, 0, 0, 0, 0, 0]], columns=list(df.columns))
            df = df.append(insertRow)
        df = df.sort(["day_id"])
        return df

    def prdtModel(self, dfRaw, yType, day, step):
        """
        获得一个代理人的信息，根据day_id，设置步长为10，筛选出训练集
        :param dfRaw: 要处理的代理人信息
        :param yType: 要处理的标签
        :param day: 预测的天数
        :param step: 数据步长
        :return: 返回训练集
        """
        # dfRaw = self.zeroFill()
        dayId = range(1, 92)

        X_train = []
        Y_train = []
        # 要预测的day_id
        dayStep = step - 1 + day
        for i in dayId:
            if dayStep + i in dayId:
                # print(i,dayStep+i-day,"------->",dayStep+i)
                X = dfRaw.loc[(dfRaw.day_id >= i) & (dfRaw.day_id <= dayStep + i - day)].as_matrix()
                X = X.reshape(1, len(X) * 7)
                X_train.append(X.tolist()[0])

                Y_df = dfRaw.loc[dfRaw.day_id == dayStep + i]
                y = Y_df[yType].as_matrix()
                Y_train.append(y.tolist())

        X_train = np.array(X_train, dtype=np.float64)
        Y_train = np.array(Y_train, dtype=np.float64)

        train_X, test_X, train_y, test_y = cross_validation.train_test_split(X_train, Y_train,
                                                                             test_size=0.2,
                                                                             random_state=0)
        return train_X, test_X, train_y, test_y

    def prdtData(self, saleNbr, yType, day, step):
        """
        根据要预测的字段，选择模型进行训练
        :param saleNbr:要预测的代理人
        :param yType: 要预测的字段
        :param day: 要预测第几天的数据
        :param step: 训练模型的步长
        :return: 
        """

        x_Test = []
        dfRaw = self.zeroFill(saleNbr)
        dataSet = self.prdtModel(dfRaw, yType, day, step)
        lab_enc = preprocessing.LabelEncoder()
        # encoded = lab_enc.fit_transform(dataSet[2])
        # encode = lab_enc.fit_transform(dataSet[3])
        if yType == 'page_rank':
            encoded = lab_enc.fit_transform(dataSet[2])
            encode = lab_enc.fit_transform(dataSet[3])
            model = self.lr.fit(dataSet[0], encoded)
        else:
            model = self.lr.fit(dataSet[0], dataSet[2])

        X = dfRaw.loc[(dfRaw.day_id > 91 - step) & (dfRaw.day_id <= 91)].as_matrix()
        X = X.reshape(1, len(X) * 7)
        x_Test.append(X.tolist()[0])
        x_Test = np.array(x_Test, dtype=np.float64)
        prdtFra = model.predict(x_Test)
        if yType == 'page_rank':
            prdtRel = model.score(dataSet[1], encode)
        else:
            prdtRel = np.round(model.score(dataSet[1], dataSet[3]), 2)
        return [prdtFra[0], prdtRel]

if __name__ == '__main__':
    start = time.time()
    prdt = Prdt()
    zb = ['cnt','round','in_degree','out_degree','page_rank']
    for i in range(1,31):
        print(i)
        for j in zb:
            print(j)
            print(prdt.prdtData("O510",j,i,30))
            print("********************************")
    print(time.time()-start)
