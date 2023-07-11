import mysql.connector
from Utils import Tools
import json


class DatabaseConnector:
    cnx = None
    cursor = None
    config = None


    @staticmethod
    def connect_to_database():
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
    def run_sql(sqlcmd, params=None):
        DatabaseConnector.initialize_database()
        DatabaseConnector.cursor.execute(sqlcmd, params)
        if DatabaseConnector.cursor.with_rows:
            rows = DatabaseConnector.cursor.fetchall()
            column_names = DatabaseConnector.cursor.column_names
            result = []
            for row in rows:
                result.append(dict(zip(column_names, row)))
            return result
        else:
            return DatabaseConnector.cursor.rowcount

    @staticmethod
    def print_results(sqlcmd, params=None):
        result = DatabaseConnector.run_sql(sqlcmd, params)
        if isinstance(result, int):
            print(f"受影响的行数：{result}")
        else:
            json_result = json.dumps(result, indent=4, ensure_ascii=False)
            print(json_result)

    @staticmethod
    def close_connection():
        if DatabaseConnector.cursor:
            DatabaseConnector.cursor.close()
        if DatabaseConnector.cnx:
            DatabaseConnector.cnx.close()


# 执行查询并打印结果
DatabaseConnector.print_results("SELECT * FROM biliuser")
# DatabaseConnector.print_results("SELECT * FROM biliuser")

# 关闭连接
DatabaseConnector.close_connection()
