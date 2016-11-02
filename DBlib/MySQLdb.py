#coding:utf-8
import MySQLdb

class MySql():
    def __init__(self,host,user,password,db):
        self.conn = MySQLdb.connect(host=host,user=user,passwd=password,db=db,charset="utf8")
        self.cursor = self.conn.cursor()
    def insert_tieba(self,dic):
        self.cursor.execute("""INSERT INTO tieba(cat_fir,cat_sec,title,attention_num,article_num,)
         VALUES ('%s', '%s', '%s','%s','%s','%s')""" % (
        dic['cat_fir'], dic['cat_sec'], dic['title'], dic['attention_num'], dic['article_num'],
        dic['flag']))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = MySql('localhost','root','1111','jdjr_data')
    db.close()