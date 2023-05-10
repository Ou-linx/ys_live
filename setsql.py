import pymysql


# 连接数据库函数
def sqlconnect():
    db = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root',
        db='live',
        charset='utf8'
    )
    return db