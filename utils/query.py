import sys
from pymysql import *

conn = connect(host='localhost',port=3306,user='root',password='root',database='weiboarticles')
cursor = conn.cursor()

def query(sql,params,type="no_select"):
    params = tuple(params)
    cursor.execute(sql,params)
    conn.ping(reconnect=True)
    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()
