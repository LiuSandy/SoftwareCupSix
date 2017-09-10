# _*_coding:utf8_*_

from .settings import Settings
from .config import Config
from . import base_sale as bs
import pandas as pd
import networkx as nx
import time, scipy

set = Settings()
"""
写入图形对象文件，为进一步图论计算做准备
生成有向图。
"""


def format_file(file_name):
    """
    初始化文件，
    由于在处理代理人之间的关系过程中没有完全说明代理关系
    :param file_name: 代理关系文件名
    :return: 返回pandas.dataframes 数据结构
    """
    # 实例化对象
    set = Settings()
    # 读文件
    df = set.reader_file(file_name)
    # 筛选出关系列
    df = df[["day_id", "sale_nbr", "buy_nbr"]]
    return df


def create_DisGraph(df, day_id=''):
    """
    根据传入的数据，按照day_id把数据进行关系模型建立
    :param df: 源数据
    :param day_id: 传入的日期[1-91],默认不传入
    :return: 返回图形对象
    """
    if day_id:
        df = df[df.day_id == day_id]
    else:
        df = df
    G = nx.from_pandas_dataframe(df, 'sale_nbr', 'buy_nbr', create_using=nx.DiGraph())
    return G, day_id


def count_degree(dict):
    """
    根据传入的图，计算每个节点的度（出度、入度）
    :param G:要计算的图
    :return: 返回每个节点的度
    """
    G = dict[0]
    day_id = dict[1]
    # 计算各个节点的出度
    out_degree = G.out_degree()
    # 计算各个节点的入度
    in_degree = G.in_degree()
    # 计算各个节点的度
    degree = G.degree()
    return {
               'out_degree': out_degree,
               'in_degree': in_degree,
               'degree': degree
           }, day_id


def count_PageRank(dict):
    """
    根据传入的图，计算每个节点的PageRank
    :param G: 要计算的图
    :return: 返回各个节点的PageRank值
    """
    G = dict[0]
    day_id = dict[1]
    PageRank = nx.pagerank(G)
    return PageRank, day_id


def get_key_node(dict):
    """
    根据传入的图，计算图的节的度中心性
    :param G: 要计算的图
    :return: 
    """
    G = dict[0]
    day_id = dict[1]
    key_node = nx.degree_centrality(G)
    print(key_node)


def dic_to_csv(dict, file_name):
    """
    主要处理一些字典类型的数据结构，便于插入数据库
    :param dict: 字典数据结构
    :param file_name: 要写入的文件名
    :return: 返回文件名
    """
    # ---------------计算PageRank---------------#
    PageRank = count_PageRank(dict)
    # print(PageRank)
    # 计算的pageRank值转化pandas Dataframe数据结构
    df_PageRank = pd.DataFrame([
        [dict[1], col1, col2] for col1, col2 in PageRank[0].items()
    ], columns=['day_id', 'sale_nbr', 'page_rank'])

    # -----------------计算度-------------------#
    degree = count_degree(dict)
    # print(degree)
    ##计算的InDegree值转化pandas Dataframe数据结构
    df_InDegree = pd.DataFrame([
        [dict[1], col1, col2] for col1, col2 in degree[0]['in_degree'].items()
    ], columns=['day_id', 'sale_nbr', 'in_degree'])

    # 计算的InDegree值转化pandas Dataframe数据结构
    df_OutDegree = pd.DataFrame([
        [dict[1], col1, col2] for col1, col2 in degree[0]['out_degree'].items()
    ], columns=['day_id', 'sale_nbr', 'out_degree'])

    # 计算的InDegree值转化pandas Dataframe数据结构
    df_Degree = pd.DataFrame([
        [dict[1], col1, col2] for col1, col2 in degree[0]['degree'].items()
    ], columns=['day_id', 'sale_nbr', 'degree'])

    df = df_InDegree.combine_first(df_OutDegree)
    df_degree = df.combine_first(df_Degree)
    All_Degree = df_degree.combine_first(df_PageRank)
    set.write_csv_data(All_Degree, file_name)
    return All_Degree


def serialize_file(sale_name, file_name):
    """
    将代理人的销售数据合并生成新的文件，
    并且序列化此生成的文件
    :param sale_name: 销售记录文件
    :param file_name: 其他指标文件
    :return: 返回新的文件
    """
    # 读出销售数据
    base_sale = Settings().reader_file(sale_name)
    # 读出其他指标数据
    df = Settings().reader_file(file_name)
    # 合并数据
    result = pd.merge(df, base_sale, how='inner', on=['sale_nbr', 'day_id'])
    # 对列名重新排列
    columns = ['day_id', 'sale_nbr', 'cnt', 'round', 'in_degree', 'out_degree', 'degree', 'page_rank']
    # 写入文件
    # Settings().write_csv_data(result, 'check_base_algorithm.csv', boolean=False)
    result.to_csv(Config().path + 'check_base_algorithm.csv', columns=columns, index=False)


def main(fileName):
    """
    执行顺序
    # 文件操作
    # 清洗数据
    # 统计销售信息
    # 计算指标
    # 地位文件生成
    :return: 
    """

    # 样本数据-------->数据清洗-------> base.csv
    # fileName = "sales_sample_20170310.csv"
    temp = set.reader_file(fileName)
    base = set.clean_the_data(temp)
    baseFileName = set.write_csv_data(base, "newBase.csv")

    sale_sum = set.reader_file(baseFileName)
    sale_name = bs.count_cnt_round(sale_sum, "sale_num.csv")
    # 计算代理人之间的关系信息
    df = format_file(baseFileName)
    # 定义存储pandas.Dataframes 的列表对象
    frames = []
    day_ids = df.drop_duplicates(['day_id'])
    for day_id in day_ids.day_id:
        dict = create_DisGraph(df, day_id)
        frames.append(dic_to_csv(dict, "all_degree.csv"))
    # 将列表内的文件合并写入文件并序列化文件
    file_name = set.write_csv_data(pd.concat(frames), 'base_algorithm.csv')
    serialize_file(sale_name, file_name)
    return "check_base_algorithm.csv"

