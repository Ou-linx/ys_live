import mysql.connector
import yaml
import requests


class Tools:
    @staticmethod
    def read_config(filename='../config.yaml'):    # yaml配置文件读取
        with open(filename, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config

    @staticmethod       # 接口返回信息转json
    def get_json(url,cookie=''):
        if cookie == '':
            bda = requests.get(url, cookies=cookie, verify=False).json()
        else:
            bda = requests.get(url, verify=False).json()
        return bda

    @staticmethod       # 配置文件类别区分提取
    def get_config(key):
        config = Tools.read_config()
        return config[key]

    @staticmethod
    def cookie_set():       # cookie字段提取转换
        cookie_b = Tools.get_config('bilibili')['cookie'].encode("utf-8").decode("latin1")
        cookies = {}  # 初始化cookies字典变量
        for line in cookie_b.split(';'):  # 按照字符：进行划分读取
            # 其设置为1就会把字符串拆分成2份
            name, value = line.strip().split('=', 1)
            cookies[name] = value  # 为字典cookies添加内容
        return cookies

    @staticmethod
    def get_tables():
        table_list = {}
        tmp = Tools.get_config('tables')
        for a in tmp:
            if "table" in a:
                table_list[a] = tmp[a]
        return table_list


class DatabaseConnector:
    cnx = None
    cursor = None
    config = None


    @staticmethod
    def connect_to_database():  # 连接到数据库
        try:
            DatabaseConnector.cnx = mysql.connector.connect(**DatabaseConnector.config)
            DatabaseConnector.cursor = DatabaseConnector.cnx.cursor()
            # print("数据库连接成功！")
        except mysql.connector.Error as err:
            print(f"数据库连接错误: {err}")
            raise

    @staticmethod
    def initialize_database():
        if not DatabaseConnector.cnx or not DatabaseConnector.cursor:
            DatabaseConnector.config = Tools.get_config('database')
            DatabaseConnector.connect_to_database()

    @staticmethod
    def run_sql(sqlcmd, params=None):       # 执行sql语句
        DatabaseConnector.initialize_database()
        DatabaseConnector.cursor.execute(sqlcmd, params)
        if DatabaseConnector.cursor.with_rows:  # 查询语句
            rows = DatabaseConnector.cursor.fetchall()
            column_names = DatabaseConnector.cursor.column_names
            result = []
            for row in rows:
                result.append(dict(zip(column_names, row)))
            return result
        else:                                   # 增删改语句
            DatabaseConnector.cnx.commit()
            return DatabaseConnector.cursor.rowcount

    @staticmethod
    def data_results(sqlcmd, params=None):     # 执行并获取sql语句返回信息
        print(sqlcmd)
        result = DatabaseConnector.run_sql(sqlcmd, params)
        if isinstance(result, int):
            print(f"受影响的行数：{result}")
            return f"受影响的行数：{result}"
        else:
            return result

    @staticmethod
    def close_connection():
        if DatabaseConnector.cursor:
            DatabaseConnector.cursor.close()
        if DatabaseConnector.cnx:
            DatabaseConnector.cnx.close()

# a = Tools.cookie_set()
# print(a)