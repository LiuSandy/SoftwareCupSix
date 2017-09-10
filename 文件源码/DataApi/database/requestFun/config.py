# _*_coding:utf-8_*_

import pandas as pd


# 配置文件

class Config:
    def __init__(self):
        # 基础文件
        self.baseFile = "E:\MyFile\pythonFile\DataApi\database\csv_file\\base.csv"
        # 计算地位文件
        self.statusFile = "E:\MyFile\pythonFile\DataApi\database\csv_file\\all_check_base_algorithm.csv"
        # self.statusFile = "E:\MyFile\pythonFile\DataApi\database\csv_file\\allTarget.csv"
        # 按块读取数据
        self.chunkSize = 1000000
        self.loop = True
        self.baseLoop = True
        self.chunks = []
        self.baseChunks = []

    def readFile(self):
        """
        读取文件
        :param fileName: 要读取的文件名
        :return: 
        """
        reader = pd.read_csv(self.statusFile, iterator=True)
        while self.loop:
            try:
                chunk = reader.get_chunk(self.chunkSize)
                self.chunks.append(chunk)
            except StopIteration:
                self.loop = False
        df = pd.concat(self.chunks, ignore_index=True)
        return df

    def readBaseFile(self):
        """
        读取文件
        :return:
        """
        reader = pd.read_csv(self.baseFile, iterator=True)
        while self.baseLoop:
            try:
                chunks = reader.get_chunk(self.chunkSize)
                self.baseChunks.append(chunks)
            except StopIteration:
                self.baseLoop = False
        baseDf = pd.concat(self.baseChunks, ignore_index=True)
        return baseDf

    def getC(self):
        """
        获得文件中航空公司信息
        :return: 
        """
        sale_of_type = []
        # 全部文件
        df = self.readFile()
        sale_of = df.drop_duplicates(['sale_nbr'])
        for i in sale_of.sale_nbr:
            if "C" in i:
                sale_of_type.append(i)

        mask = df['sale_nbr'].isin(sale_of_type)
        return df[mask]

    def getO(self):
        """
        获得文件中代理人信息
        :return: 
        """
        sale_of_type = []
        # 全部文件
        df = self.readFile()
        sale_of = df.drop_duplicates(['sale_nbr'])
        for i in sale_of.sale_nbr:
            if "O" in i:
                sale_of_type.append(i)
        mask = df['sale_nbr'].isin(sale_of_type)
        return df[mask]

    def getSaleNbr(self, df):
        """
        根据传入的文件获得所有的代理人信息
        :param df: 传入的文件
        :return: 
        """
        sale_of_type = []
        # sale_of = df.index
        for i in df.index:
            sale_of_type.append(i)
        return sale_of_type


if __name__ == '__main__':
    cf = Config()
    df = cf.getO()
    print(len(cf.getSaleNbr(df)))
