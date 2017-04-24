import MySQLdb
from settings import get_mysqldb_settings

class sqlexe():
	def __init__(self):
		self.settings = get_mysqldb_settings()
		self.host=self.settings.MYSQL_HOST
		self.port=self.settings.MYSQL_PORT
		self.user=self.settings.MYSQL_USER
		self.passwd=self.settings.MYSQL_PASSWD
		self.db=self.settings.MYSQL_DBNAME

	def sql_run(self,sql):
		conn=MySQLdb.connect(host=self.host, port=self.port, user=self.user,
				passwd=self.passwd, db=self.db, charset='utf8')
		cur=conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
		conn.close()
		return data
