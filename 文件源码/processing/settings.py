#_*_coding: utf8_*_
import pandas as pd
import time
from config import Config

"""
对源数据进行清洗形成自己的源数据base.csv
"""

class Settings:
    def __init__(self):
        self.chunkSize = 1000000
        self.loop = True
        self.chunks = []
        self.time_week = [] #定义周标识符
        self.time_month = [30,61,91] #定义月标识符

#-------------数据的基本处理（读、写、清洗）------------------#
    def reader_file(self,file_name):
        """
        对本地数据进行读取,
        :return: 读取后的数据
        """
        file_name = Config().path + file_name
        reader = pd.read_csv(file_name, iterator=True)
        while self.loop:
            try:
                chunk =reader.get_chunk(self.chunkSize)
                self.chunks.append(chunk)
            except StopIteration:
                self.loop = False
                print("Iteration is stopped.")
        df = pd.concat(self.chunks, ignore_index=True)
        return df


    def clean_the_data(self,df):
        """
        对传入的数据进行清洗，取出buy_nbr为空，cnt和round为0的数据
        :param df: 传入源数据df
        :return: 返回清理后输的数据
        """
        # 标记并删除buy_nbr为空的数据
        is_null = df.dropna()
        #标记并删除cnt或者round为0的数据
        is_zero = is_null.loc[(is_null["cnt"] != 0) & (is_null["round"] !=0)]
        return is_zero

    def write_csv_data(self,df,new_name,boolean=False):
        """
        将清洗过的数据，重新写入到新的csv文件中
        :param df: 清洗完的数据
        :param new_name:写入的文件名
        :param boolean: 是否写入index,默认不写入index
        :return: 返回文件名
        """
        if boolean:
            index = True
        else:
            index = False

        df.to_csv(Config().path+new_name,sep=',',index=index,mode="a+")
        return new_name


#--------------------数据的筛选---------------------------#
    def get_all_sale(self,df):
        """
        获得所有销售商的代码
        :param df: 要处理的文件
        :return: 返回所有的销售商的代码
        """
        sale_O = df.drop_duplicates(['sale_nbr'])
        buy_O = df.drop_duplicates(['buy_nbr'])
        sale = pd.concat([sale_O['sale_nbr'], buy_O['buy_nbr']])
        sale_agg = sale.drop_duplicates()
        return sale_agg

    def get_time_block(self,df,day_range):
        """
        获得时间块：按周、按月
        :param df: 原文件
        :param day_range: 日期查找范围
        :return: 划分完的文件
        """
        if day_range[1] < 30:
            df_of_week = df.loc[(df["day_id"] >= day_range[0]) & (df["day_id"] <= day_range[1])]
            return df_of_week
        elif day_range[1] >= 30:
            df_of_month = df.loc[(df["day_id"] >= day_range[0]) & (df["day_id"] <= day_range[1] )]
            return df_of_month

    def get_type_sale(self,df,type):
        """
        根据传入的数据进行分类查找，即查找出当前时间段内sale_nbr字段的售出者
        例如：day_id在1-7之内所有的代理人（sale_nbr)
        :param df: 待处理文件
        :param type: 查找的类型（航空公司/代理人/消费者） 
        :return: 分类完文件
        """
        sale_of_type = []
        if type == 'C':
            sale_of = df.drop_duplicates(['sale_nbr'])
            for i in sale_of.sale_nbr:
                if "C" in i:
                    # print(i)
                    sale_of_type.append(i)
            return sale_of_type
        elif type == 'O':
            sale_of = df.drop_duplicates(['sale_nbr'])
            for i in sale_of.sale_nbr:
                if "O" in i:
                    sale_of_type.append(i)
            return sale_of_type

    def get_type_buy(self,df):
        """
        根据传入的数据进行分类查找，即查找出当前时间段内buy_nbr字段的消费者
        例如：day_id在1-7之内所有的代理人（buy_nbr)
        :param df: 待处理文件 
        :return: 当前时间段内消费者的代码
        """
        buy_of = df.drop_duplicates(['buy_nbr'])
        return buy_of

    def get_C_O(self,df):
        """
        筛选出代理人与航空公司的交易信息
        :param df: 传入原文件
        :return: 返回筛选后的Pandas.Dataframes数据类型
        """
        sale_of_type = []
        sale_of = df.drop_duplicates(['sale_nbr'])
        for i in sale_of.sale_nbr:
            if "C" in i:
                sale_of_type.append(i)

        mask =  df['sale_nbr'].isin(sale_of_type)
        return df[mask]
