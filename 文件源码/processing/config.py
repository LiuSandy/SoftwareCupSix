#_*_coding:utf8_*_
import os

class Config:
    def __init__(self):
        """
        数据库配置
        """
        #配置数据库地址
        self.databases_url = "localhost"
        #数据库用户名
        self.user = "root"
        #数据库密码：
        self.password = "rootlius"
        #要使用的数据库
        self.database = "test_db"
        self.prefix = "a20170310_"

        """
        csv文件读写配置
        """
        #文件读写地址
        self.path = "E:/MyFile/pythonFile/my_db/pandascsv/csv_file/"

    def check_file(self,file_name):

        """
        检测是否存在文件，
        :param file_name: 要检测文件名
        :return: True：存在； False：不存在
        """
        if os.path.isfile(Config().path+file_name):
            return True
        else:
            return False