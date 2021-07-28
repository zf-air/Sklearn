import pymysql

#打开数据库连接
conn=pymysql.connect(host = "localhost" # 连接名称，默认127.0.0.1 
,user = "root" # 用户名
,passwd = "zhangfan789.." # 密码
,port = 3306 # 端口，默认为3306
,db = "test" # 数据库名称
)

cur = conn.cursor() # 生成游标对象

sql="select * from customers" # SQL语句

cur.execute(sql) # 执行SQL语句

data = cur.fetchall() # 通过fetchall方法获得数据

for i in data[:]: # 打印输出前2条数据
    print("\n",i)

cur.close() # 关闭游标
conn.close() # 关闭连接