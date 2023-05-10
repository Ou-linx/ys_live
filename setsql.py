import mysql.connector
import yaml


# 读取配置文件
def read_config(filename = 'config.yaml'):
    with open(filename, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


# 连接数据库，并返回连接对象和游标对象
def connect_to_database(config):
    try:
        # 创建连接对象
        cnx = mysql.connector.connect(**config['database'])
        # 创建游标对象
        cursor = cnx.cursor()
        print("数据库连接成功！")
        # 返回连接对象和游标对象
        return cnx, cursor

    except mysql.connector.Error as err:
        print(f"数据库连接错误: {err}")


# 执行sql语句并返回结果
def run_sql(sqlcmd):
    # 从YAML配置文件中读取连接数据库所需的配置信息
    config = read_config()
    # 连接到数据库
    cnx, cursor = connect_to_database(config)
    # 从YAML配置文件中读取内容
    # query = config['queries']['select_all']
    # 执行查询
    cursor.execute(sqlcmd)
    # 获取查询结果
    result = cursor.fetchall()
    # 关闭连接
    cursor.close()
    cnx.close()
    return result

# 打印结果
for row in run_sql("select * from biliuser"):
    print(row)