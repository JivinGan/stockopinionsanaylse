import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='',
        user='',
        password='',
        database='',
        charset='utf8mb4'
    )
    return connection


