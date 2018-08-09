import pymysql

# print("------------------------- 方法一: 静态更新数据库 -------------------------------")
# nid = '20120001'
# name = 'Bob'
# age = 20

# conn = pymysql.connect(host='123.207.232.222', user='root', passwd='123456', db='baike', port=3306, charset='utf8')
# cursor = conn.cursor()

# sql = "INSERT INTO students(nid, name, age) values('%s', '%s', '%d')" % (nid, name, age)
# try:
#     cursor.execute(sql)
#     conn.commit()
# except:
#     print("Inert data fail!!!")
# cursor.close()
# conn.close()

print("------------------------- 方法二：动态更新数据库 -----------------------------------")
'''
在实际的数据抓取过程中，大部分情况下需要插入数据，但是我们关心的是会不会出现重复数据，如果出现了，我们希望更新数据而不是重复保存一次。另外，就像前面所说的动态构造SQL的问题，所以这里可以再实现一种去重的方法，如果数据存在，则更新数据；如果数据不存在，则插入数据。另外，这种做法支持灵活的字典传值。示例如下：
'''
conn = pymysql.connect(host='123.207.232.222', user='root', passwd='123456', db='baike', port=3306, charset='utf8')
cursor = conn.cursor()

data = {
    'nid': '20120003',
    'name': 'Bob',
    'age': 21
}
 
table = 'students'
keys = ', '.join(data.keys())
values = ', '.join(['%s'] * len(data))
 
sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
update = ','.join([" {key} = %s".format(key=key) for key in data])
sql += update
try:
    if cursor.execute(sql, tuple(data.values())*2):
        print('Successful')
        conn.commit()
except:
    print('Failed')
    conn.rollback()
conn.close()

