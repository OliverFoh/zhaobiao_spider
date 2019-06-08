import pymysql
class SaveToMysql():
    def __init__(self,info_queue):
        self.HOST='127.0.0.1'
        self.USER='root'
        self.PASSWORD='Fswmysql'
        self.PORT='3306'
        self.DATABASE='zhaobiao'
        self.TABLE='zhaobiao_data'
        self.info_queue=info_queue

        #存储语句
        self.sql='insert into zhaobiao_data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        # 建立连接
        self.db= pymysql.connect(self.HOST, self.USER, self.PASSWORD, self.DATABASE)
        print('连接成功')
        self.cursor =self.db.cursor()
    def connectDatabase(self):
        try:

            while True:
                if self.info_queue.full()!=True and self.info_queue.empty()!=True:
                    print(000)
                tuple_list=tuple(self.info_queue.get().values())
                cursor.execute(self.sql,tuple_list)
                db.commit()
                print('写入成功')
        except Exception as e:
            db.rollback()
            print('插入数据错误')
            print(e)
        finally:
            db.close()