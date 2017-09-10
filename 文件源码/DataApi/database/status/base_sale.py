# _*_coding: utf8_*_

"""计算每天每个代理人的销售量和销售额，并写到新的文件中"""
import pandas as pd
from .settings import Settings
from .config import Config


# ---------------计算在全市场的销售信息-------------#
def count_cnt_round(df, file_name):
    """
    计算每天每个代理人的销售量和销售额,并写入文件
    :param df: 传入源数据
    :param file_name: 要写入的文件名
    :return: 返回写入的文件
    """
    # file_path = Config().path + file_name
    # 检测是否已经写入
    if Config().check_file(file_name):
        print("文件已经存在了，拿去用吧！！！")
        return file_name
    else:
        print("还没有这个文件，努力创作中。。。。。")
        all_sale_num = df.groupby([df.day_id, df.sale_nbr]).sum()
        Settings().write_csv_data(all_sale_num, file_name, boolean=True)
        return file_name


def screen_one(df, sale_nbr, file_name):
    """
    根据sale_nbr在源数据中筛选出这个代理人的每天销售信息
    :param df: 传入的源数据
    :param sale_nbr: 代理人信息
    :param file_name: 写入的文件
    :return: 返回文件名
    """
    if Config().check_file(file_name):
        print("文件已经存在了，拿去用吧！！！")
        return file_name
    else:
        print("还没有这个文件，努力创作中。。。。。")
        df = df[df.sale_nbr == sale_nbr]
        one_sale_num = df.groupby([df.day_id, df.sale_nbr]).sum()
        Settings().write_csv_data(one_sale_num, file_name)
        return file_name


"""
计算代理人的销售信息，并且可以根据当代理人筛选出单个的销售信息
"""
