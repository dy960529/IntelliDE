import MySQLdb
import os,sys,smtplib
import time
from time import sleep
from scrapy.utils.project import get_project_settings

class sqlselect():
	def __init__(self):
		self.settings=get_project_settings()
		self.host=self.settings['MYSQL_HOST']
		self.port=self.settings['MYSQL_PORT']
		self.user=self.settings['MYSQL_USER']
		self.passwd=self.settings['MYSQL_PASSWD']
		self.db=self.settings['MYSQL_DBNAME']

	def select_forum_id(self):
		conn=MySQLdb.connect(host=self.host, port=self.port, user=self.user,
				passwd=self.passwd, db=self.db, charset='utf8')
		cur=conn.cursor()

		sql_select="select forum_id from forumlist where spider_flag = 0"
		cur.execute(sql_select)
		data_select = cur.fetchall()

		cur.close()
		conn.close()

		return data_select

if __name__=="__main__":
	dbtest = sqlselect()
	T_list = dbtest.select_forum_id()
	for data in T_list:
		print (data[0])
