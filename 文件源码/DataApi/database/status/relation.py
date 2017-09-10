#_*_coding: utf8_*_

"""计算代理人的交易往来
    1、作为售出者下面有多少消费者
    2、作为买入者上面有多少提供者
    3、输出全部的关系信息
"""
from settings import Settings
import pandas as pd
import time



class Relation:
    def __init__(self):
        self.set = Settings()

    def get_every_sale(self,df,file_name):
        """
        以天为单位
        根据传入的处理文件，找到所有的代理人卖出到多少其他代理人
        :param df: 要处理的文件
        :param file_name: 要写入的文件
        :return: 写入文件，返回存着每天每个代理人的销售人的文件名
        """
        df = df.groupby([df.day_id,df.sale_nbr,df.buy_nbr]).count()
        self.set.write_csv_data(df,file_name,boolean=True)
        return file_name

    def get_every_buy(self,df,file_name):
        """
        以天为单位
        根据传入的处理文件，找到这个代理人上面有多少供货商
        :param df: 要处理的文件
        :param file_name: 要写人的文件
        :return: 写入文件，并返回文件名
        """
        df = df.groupby([df.day_id,df.buy_nbr,df.sale_nbr]).count()
        self.set.write_csv_data(df, file_name, boolean=True)
        return file_name

