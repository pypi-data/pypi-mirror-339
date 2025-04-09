from multiprocessing import connection

import pymysql, config, re
import cleaner_util



def update_mysql(id, title):
    update_sql = "update bid_keywords set title = %s where id = %s"
    cursor.execute(update_sql, (title, id))
    connect.commit()

connect = pymysql.Connect(
    host="140.210.91.215",
    port=63306,
    user="root",
    passwd="ojH2QnNaMM36Dt2dNHt7",
    db="morning_boss",
    charset=config.charset,
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connect.cursor()
cursor.execute("select infoId,infoTitle from bid_keywords where infoTitle like '%&%' or infoTitle like '%<%' ")
connect.commit()
res = cursor.fetchall()
for d in res:
    id = d["infoId"]
    title = d["infoTitle"]
    title = deal_title(title)
    print(title)
print(res)
