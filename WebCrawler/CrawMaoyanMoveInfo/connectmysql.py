import pymysql


class ConnectMysql(object):
    def __init__(self):
        self.word_datas = []

    def mysql_collect_data(self, data):
        if data is None:
            return
        self.word_datas.append(data)
        # print(self.word_datas)

    def mysqlConnect(self):
        conn = pymysql.connect(host='123.207.232.222', user='root', passwd='123456', db='baike', port=3306, charset='utf8')
        return conn
    
    def saveData(self):
        self.conn = self.mysqlConnect()
        self.cur = self.conn.cursor()
        
        self.selectsql = "SELECT * FROM maoyan_move_info"

        temp_datas = []
        try:
            self.cur.execute(self.selectsql)
            self.results = self.cur.fetchall()
            for row in self.results:
                temp_datas.append(row[1])
            # print(temp_datas)
        except:
            print("select sql fail")

        for data in self.word_datas:
            # print(data, type(data))
            if data['index'] not in temp_datas:
                # print(data['index'], data['image'], data['title'], data['actor'], data['time'], data['score'])
                self.insertsql = "INSERT INTO maoyan_move_info(top_index, image_url, title, actor, time, score) values('%s','%s','%s','%s','%s','%s')" % (data['index'], data['image'], data['title'], data['actor'], data['time'], data['score'])
                try:
                    self.cur.execute(self.insertsql)
                    self.conn.commit()
                except:
                    print("insert data fail!!!")
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    conmysql = ConnectMysql()
    conmysql.saveData()
        

