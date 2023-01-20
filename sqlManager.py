import pymysql


class SQLManager:
    def __init__(self, dbhost, dbuser, password, database):
        self.db = pymysql.connect(host=dbhost,
                                  user=dbuser,
                                  password=password,
                                  database=database,
                                  cursorclass=pymysql.cursors.DictCursor)

    def request(self, sql):
        try:
            # 2.创建游标对象
            cursor = self.db.cursor()
            # 3.执行sql语句
            res = cursor.execute(sql)
            self.db.commit()  # 在执行sql语句时，注意进行提交
            # 4.提取结果
            data = cursor.fetchall()

            return res, data
        except:
            self.db.rollback()  # 当代码出现错误时，进行回滚
            # print(pymysql.Error.args[0], pymysql.Error.args[1])

