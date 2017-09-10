#_*_coding: utf8_*_

"""计算每天每个代理人的交易信息记录，两个代理人之间的交易往来"""
import pandas as pd
from settings import Settings
from config import Config
import os


def output_sample(df,all_sale,file_name,set):
    """
    输出全部文件：预测的day_id为10，对于O100，输出历史上与O100有交易关系的全部实体
    :param df: 原文件
    :param all_sale:所有的代理人代码 
    :param file_name: 写入的文件名
    :param set: Settings类，用于操作csv文件
    :return: 不返回数据，
    """
    if Config().check_file(file_name):
        print("已经存在这个文件了，拿去用吧！！！！")
        return file_name
    else:
        print("还不存在这个文件了，现在正在写！！！！")
        for sale in all_sale:
            print("正在写入%s代理人的交易记录"% (sale))
            output_sample_file = df[(df.sale_nbr == sale) | (df.buy_nbr == sale)]
            set.write_csv_data(output_sample_file,file_name)
        return file_name

def output_sample_one(df,sale_nbr,day,file_name,set):
    """
    根据用户选择的代理人进行，与她有交易记录的代理人
    :param df: 原文件
    :param sale_nbr:选择的代理人 
    :param file_name: 写入文件名
    :param set: set类，操作csv文件对象
    :return: 返回文件名
    """
    if check_file(file_name):
        print("已经存在这个文件了，拿去用吧！！！！")
        return "output_sample.csv"
    else:
        print("还不存在这个文件了，现在正在写！！！！")
        output_sample_file = df[(df.sale_nbr == sale_nbr) | (df.buy_nbr == sale_nbr)]
        output_sample = output_sample_file[(output_sample_file.day_id == day)]
        set.write_csv_data(output_sample, file_name)
        return file_name


"""
大赛指定的输出数据结构，可以不返回数据直接写入在csv文件中。返回文件名
返回文件名: 是为了以后处理（添加数据库）

由于这个文件处理的内容特殊(文件名已知)，所以需要特殊对待
-------在处理之前先要检查是否已经存在文件，
-------如果存在直接拿来使用
-------如果不存在需要重新写入                                                                   
"""