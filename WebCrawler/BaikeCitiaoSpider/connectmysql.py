import pymysql


class ConnectMysql(object):
    def __init__(self):
        self.word_datas = []

    def mysql_collect_data(self, data):
        if data is None:
            return
        self.word_datas.append(data)

    def mysqlConnect(self):
        conn = pymysql.connect(host='123.207.232.222', user='root', passwd='123456', db='baike', port=3306, charset='utf8')
        return conn
    
    def saveData(self):
        self.conn = self.mysqlConnect()
        self.cur = self.conn.cursor()
        
        self.selectsql = "SELECT * FROM words_baike"

        temp_datas = []
        try:
            self.cur.execute(self.selectsql)
            self.results = self.cur.fetchall()
            for row in self.results:
                temp_datas.append(row[2])
        except:
            print("select sql fail")

        for data in self.word_datas:
            if data['title'] not in temp_datas:
                self.insertsql = "INSERT INTO words_baike(word_url, word_title, word_summary) values('%s','%s','%s')" % (data['url'], data['title'], data['summary'])
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
        

