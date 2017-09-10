#_*_coding:utf8_*_
import os

class Config:
    def __init__(self):
        """
        csv文件读写配置
        """
        #文件读写地址
        # self.path = "E:/MyFile/pythonFile/my_db/pandascsv/csv_file/"
        self.path = "E:/MyFile/pythonFile/DataApi/database/csv_file/upload/"
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