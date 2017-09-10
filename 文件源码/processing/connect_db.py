#_*_coding: utf8_*_
import pymysql,re
import pandas as pd
from settings import Settings
from config import Config

"""
主要的数据库操作，
"""
class Connect:
    def __init__(self):
        #创建连接
        self.db = pymysql.connect(Config().databases_url,Config().user,Config().password,Config().database,local_infile=True)
        # print(self.db)
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

#------------检测数据表是否存在------------#
    def exist_of_table(self,db_name):
        """
        用于检测数据表是否存在？
        :param db_name: 要检测的数据表
        :return: 如果存在返回True,不存在返回False
        """
        sql_show_table = "show tables"
        self.cursor.execute(sql_show_table)
        tables = [self.cursor.fetchall()]

        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]
        if Config().prefix+db_name in table_list:
            return True
        else:
            return False

#--------------csv 文件插入数据库-----------------#
    """
    这类函数主要处理pandas 模块处理的csv文件
    """
    def creat_db(self,csv_file,db_name):
        """
        根据csv文件检测并创建合适的数据库表
        :param csv_file: 要创建数据库的csv文件
        :param db_name: 数据库名称
        :return: 真假，是否创建成功数据表
        """
        db_name =Config().prefix + db_name
        df = set.reader_file() #转换pandas数据格式
        if self.exist_of_table(db_name):
            return True
        else:
            print("是不是还没有数据表呢？赶紧去创建吧！(*^__^*) ")
            print("别着急，正在创建数据库.....")
            columns = df.columns           #字段
            types = df.dtypes              #字段类型
            sql = "CREATE table %s (" % (db_name)
            for i in range(len(columns)):
                if types[i] == "int64" or types[i] == "float64":
                    sql = sql + columns[i] + " INT(11) NULL,"
                else:
                    sql = sql + columns[i] + " VARCHAR(11) NULL,"
            sql = sql[:-1]+")"
            print(sql)
            try:
                self.cursor.execute(sql)
                return True
            except Exception as e:
                print("创建数据库失败！！！")
                print(" sorry！管理员又写错了！赶紧联系他吧！！！")
                print(e)
                return False

    def csv_to_db(self,csv_file,sep,db_name):
        """
        将csv文件导入到数据库中
        :param csv_file: 要导入数据库的csv文件
        :param sep: 字段分隔符
        :param db_name: 数据库名称
        :return: 没有返回值
        """
        print('正在将csv数据导入数据库......')
        if self.creat_db(csv_file,db_name):
            sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY '%s'" % (csv_file,Config().prefix+db_name,sep)
            print(sql)
            try:
                self.cursor.execute(sql)
                print("写入成功")
                self.delect_exception_data(db_name)
            except Exception as e:
                print("导入数据失败~~~~(>_<)~~~~")
                print(" sorry！管理员又写错了！赶紧联系他吧！！！")
                print(e)

    def delect_exception_data(self,db_name):
        """
        删除day_id不正常的数据
        :param db_name: 数据表名称
        :return: 没有返回值
        """
        print("正在清洗可疑数据")
        sql = "delete from %s where day_id = 0 or day_id is NULL " % (Config().prefix+db_name)
        print(sql)
        try:
            self.cursor.execute(sql)
            print("清洗完成啦")
        except Exception as e:
            print(e)
            print("清洗失败，尴尬")

#-------------Python 字典类型插入数据库------------#
    """
    这类函数主要处理networkx返回的字典数据类型
    """
    def dict_to_db(self,table_name,dict):
        """
        把字典按照格式插入到数据库
        :param table_name: 要操作的数据表
        :param dict: 要插入数据的字典数据
        :return: 不返回
        """
        #检测是否存在数据表
        if self.exist_of_table(table_name):
            #插入数据库
            for key,value in dict.items():
                insert_sql = "INSERT INTO %s ()"

        else:
            create_sql ="""create table %s(week_id INT(11) NOT NULL,sale_nbr VARCHAR(11) NOT NULL,in_degree INT(11) NOT NULL,out_degree INT(11) NOT NULL,degree INT(11) NOT NULL,page_rank DOUBLE NOT NULL)""" % (Config().prefix+table_name)
            self.cursor.execute(create_sql)
            self.dict_to_db(table_name,dict)





if __name__ == "__main__":
    connect = Connect()
    # set = Settings("base.csv")
    # # connect.clean_csv_file('base.csv')
    # connect.csv_to_db(set.file_name,",","base")
    dict = {"a": "1", "c": "2"}
    # connect.dict_to_db(dic)
    print(connect.dict_to_db("algorithm",dict))