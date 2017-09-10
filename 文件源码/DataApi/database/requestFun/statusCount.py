# _*_coding:utf-8_*_

import pandas as pd
import numpy as np
import networkx as nx
from .config import Config

# 计算各种地位排名
cf = Config()


class Status:
    def __init__(self):
        self.df = cf.getO()
        self.baseDf = cf.readBaseFile()

    def getAllCount(self):
        """
        获得每一列的和
        :return: 
        """
        dict = {}
        columns = self.df.columns
        for i in columns:
            if i != "sale_nbr":
                dict[i] = self.df[i].sum()
        return dict

    def outDegree(self):
        """
        根据出度入度，筛选出排名前十
        :return: 返回排名数据[数组]
        """
        # 筛选度
        dfOutDegree = self.df[['sale_nbr', 'degree']]
        # 按照代理人分组统计
        countOutDegree = dfOutDegree.groupby('sale_nbr').sum()
        # 进行排序
        sortOutDegree = countOutDegree.sort_values('out_degree', ascending=False)
        dfTop = sortOutDegree.head(10)
        # 筛选出全部代理人
        allSaleNbr = dfTop.index.tolist()
        # sortDegree = dfTop['degree'].tolist()

        # sortOutDegree['sale_nbr'] = sortOutDegree.index
        return allSaleNbr

    def inDegree(self):
        """
        根据出度入度，筛选出排名前十
        :return: 返回排名数据[数组]
        """
        # 筛选度
        dfOutDegree = self.df[['sale_nbr', 'degree']]
        # 按照代理人分组统计
        countOutDegree = dfOutDegree.groupby('sale_nbr').sum()
        # 进行排序
        sortOutDegree = countOutDegree.sort_values('in_degree', ascending=False)
        dfTop = sortOutDegree.head(10)
        # 筛选出全部代理人
        allSaleNbr = dfTop.index.tolist()
        # sortDegree = dfTop['degree'].tolist()

        # sortOutDegree['sale_nbr'] = sortOutDegree.index
        return allSaleNbr

    def saleCnt(self):
        """
        根据销售量信息，筛选出排名前十
        :return: 返回排名数据[数组]
        """
        dfCnt = self.df[['sale_nbr', 'cnt']]
        countCnt = dfCnt.groupby('sale_nbr').sum()
        sortCnt = countCnt.sort_values('cnt', ascending=False)
        dfTop = sortCnt.head(10)
        allSaleNbr = dfTop.index.tolist()
        return allSaleNbr

    def saleRound(self):
        """
        根据销售额信息，筛选出排名前十
        :return: 返回排名数据[数组]
        """
        dfRound = self.df[['sale_nbr', 'round']]
        countRound = dfRound.groupby('sale_nbr').sum()
        sortRound = countRound.sort_values('round', ascending=False)
        dfTop = sortRound.head(10)
        allSaleNbr = dfTop.index.tolist()
        return allSaleNbr

    def salePageRank(self):
        """
        根据销售额信息，筛选出排名前十
        :return: 返回排名数据[数组]
        """
        dfPageRank = self.df[['sale_nbr', 'page_rank']]
        countPageRank = dfPageRank.groupby('sale_nbr').sum()
        sortPageRank = countPageRank.sort_values('page_rank', ascending=False)
        dfTop = sortPageRank.head(10)
        allSaleNbr = dfTop.index.tolist()
        return allSaleNbr

    def countSale(self, saleNbrList):
        """
        传入代理人列表，计算他们的各个指标的值
        :param saleNbrList: 
        :return: 
        """

        saleDict = {}
        columns = self.df.columns
        for saleNbr in saleNbrList:
            dict = {}
            df = self.df[self.df.sale_nbr == saleNbr]
            for i in columns:
                if i != "sale_nbr":
                    dict[i] = df[i].sum()

            saleDict[saleNbr] = dict
        return saleDict

    def getTrend(self, saleNbr, dayRange):
        """
        根据日期范围筛选这个代理人的指标趋势----日走势图
        :param saleNbr: 代理人代码
        :param dayRange: 日期范围
        :return: 
        """
        dict = {}
        # 筛选这个代理人的信息
        dfSaleNbr = self.df[self.df.sale_nbr == saleNbr]
        # 日期内趋势
        rangeSaleNbr = dfSaleNbr[(dfSaleNbr.day_id >= dayRange[0]) & (dfSaleNbr.day_id <= dayRange[1])]
        # 获得头
        columns = rangeSaleNbr.columns
        for i in columns:
            if i != "sale_nbr":
                dict[i] = np.array(rangeSaleNbr[i]).tolist()
        sumTarget = rangeSaleNbr.sum()
        avgTarget = rangeSaleNbr.mean()
        dict['cntSum'] = sumTarget.cnt
        dict['roundSum'] = sumTarget['round']
        dict['cntAvg'] = avgTarget.cnt
        dict['roundAvg'] = avgTarget['round']
        dict['inDegreeSum'] = sumTarget.cnt
        dict['outDegreeSum'] = sumTarget['round']
        dict['inDegreeAvg'] = avgTarget.cnt
        dict['outDegreeAvg'] = avgTarget['round']
        return dict

    def getWeekTrend(self, saleNbr):
        """
        根据代理人代码筛选他的周走势图
        :param sale_nbr: 
        :return: 
        """
        dict = {}

        # 筛选这个代理人的信息
        dfSaleNbr = self.df[self.df.sale_nbr == saleNbr]
        columns = dfSaleNbr.columns
        for i in columns:
            if i != "sale_nbr":
                list = []
                for a in range(1, 92, 7):
                    rangeSaleNbr = dfSaleNbr[(dfSaleNbr.day_id >= a) & (dfSaleNbr.day_id < a + 7)]
                    list.append(rangeSaleNbr[i].sum())
                dict[i] = list

        return dict

    def featDay(self, feat):
        """
        计算不同指标在不同day_id的值
        :param feat:指标字段
        :return: 
        """
        dayValue = []
        df = self.df[['day_id', feat]]
        dfCount = df.groupby('day_id').sum()
        num = 0
        for i in dfCount[feat]:
            num += 1
            data = [str(num), float(i)]
            dayValue.append(data)
        return dayValue

    def countAllFeat(self, feat):
        countCnt = self.df.groupby('sale_nbr').sum()
        sort = countCnt.sort_values(feat, ascending=False)
        resetDf = sort.reset_index()
        dict = {}
        columns = resetDf.columns
        for column in columns:
            dict[column] = np.array(resetDf[column]).tolist()
        return dict

    def history_info(self, saleNbr, dayId):
        """
        历史销售信息，
        ---------------------------
        传入代理人以及day_id数值，返回历史上与他有销售关系的代理人情况
        :return: 
        """
        output_sample_file = self.baseDf[(self.baseDf.sale_nbr == saleNbr) | (self.baseDf.buy_nbr == saleNbr)]
        output_sample = output_sample_file[(output_sample_file.day_id == dayId)]
        dict = {}
        columns = output_sample.columns
        for column in columns:
            dict[column] = np.array(output_sample[column]).tolist()
        return dict

    def saleRoute(self, cSale):
        """
        航空公司的销售路线
        :param cSale:航空公司代码
        :return: 
        """
        df = self.baseDf.groupby([self.baseDf.day_id, self.baseDf.sale_nbr, self.baseDf.buy_nbr]).sum()
        indexDf = pd.DataFrame(list(df.index), columns=df.index.names)
        # print(df.cnt)
        print(indexDf)
        G = nx.from_pandas_dataframe(indexDf, 'sale_nbr', 'buy_nbr', create_using=nx.DiGraph())
        # print(list(nx.edge_dfs(G)))

#
# if __name__ == "__main__":
#     import time
#
#     start = time.time()
#     status = Status()
#     status.saleRoute('C1')
#     print(time.time() - start)
