import MySQLdb
from scrapy.utils.project import get_project_settings
class DBHelper():

	def __init__(self):
		self.settings=get_project_settings()

		self.host=self.settings['MYSQL_HOST']
		self.port=self.settings['MYSQL_PORT']
		self.user=self.settings['MYSQL_USER']
		self.passwd=self.settings['MYSQL_PASSWD']
		self.db=self.settings['MYSQL_DBNAME']

	# connect to mysql, not to database
	def connectMysql(self):
		conn=MySQLdb.connect(host=self.host,
							 port=self.port,
							 user=self.user,
							 passwd=self.passwd,
							 charset='utf8')
		return conn

	# connect database
	def connectDatabase(self):
		conn=MySQLdb.connect(host=self.host,
							 port=self.port,
							 user=self.user,
							 passwd=self.passwd,
							 db=self.db,
							 charset='utf8')
		return conn

	# create database
	def createDatabase(self):
		conn=self.connectMysql()

		sql="create database if not exists "+self.db
		cur=conn.cursor()
		cur.execute(sql)
		cur.close()
		conn.close()

	# create table
	def createTable(self,sql):
		conn=self.connectDatabase()

		cur=conn.cursor()
		cur.execute(sql)
		cur.close()
		conn.close()

	# create table
	def select(self,sql):
		conn=self.connectDatabase()

		cur=conn.cursor()
		cur.execute(sql)
		cur.close()
		conn.close()

	# insert data
	def insert(self,sql,*params):
		conn=self.connectDatabase()

		cur=conn.cursor();
		cur.execute(sql,params)
		conn.commit()
		cur.close()
		conn.close()
	# update data
	def update(self,sql,*params):
		conn=self.connectDatabase()

		cur=conn.cursor()
		cur.execute(sql,params)
		conn.commit()
		cur.close()
		conn.close()
	# delete data
	def delete(self,sql,*params):
		conn=self.connectDatabase()

		cur=conn.cursor()
		cur.execute(sql,params)
		conn.commit()
		cur.close()
		conn.close()



# This is a test class for DBHelper
class TestDBHelper():
	def __init__(self):
		self.dbHelper=DBHelper()

	# Test createDatabas mathod (database name is in settings.py MYSQL_DBNAME)
	def testCreateDatabase(self):
		self.dbHelper.createDatabase()
	# test CrateTable
	def testCreateTable(self):

		visitlist_table_sql = ("create table visitlist("
								"visit_topic VARCHAR(20) NOT NULL,"
								"visit_type VARCHAR(10) NOT NULL,"
								"visit_page INT,"
								"PRIMARY KEY (visit_topic,visit_type)) default charset = utf8")

		topicmap_table_sql = ("create table topicmap("
								"topic_id VARCHAR(20) NOT NULL,"
								"topic_type VARCHAR(10) NOT NULL,"
								"topic_name VARCHAR(50),"
								"topic_detail LONGTEXT,"
								"page_num INT,"
								"forum_sum INT,"
								"spider_flag INT,"
                                "PRIMARY KEY (topic_id,topic_type)) default charset = utf8")

		forumlist_table_sql = ("create table forumlist("
								"forum_id INT NOT NULL,"
								"forum_class VARCHAR(20) NOT NULL,"
								"forum_type VARCHAR(10) NOT NULL,"
								"forum_title VARCHAR(1000),"

								"forum_url VARCHAR(50),"
								"forum_point INT,"
								"forum_answer_number INT,"
								"forum_question_user VARCHAR(30),"

								"forum_question_time VARCHAR(20),"
								"forum_update_user VARCHAR(30),"
								"forum_update_time VARCHAR(20),"
								"spider_flag INT,"
                                "PRIMARY KEY (forum_id)) default charset = utf8")

		bbscomment_table_sql = ("create table bbscomment("
								"comment_id INT NOT NULL,"
								"comment_floor INT NOT NULL,"
								"comment_person VARCHAR(30),"
								"comment_time VARCHAR(20),"
								"comment_context LONGTEXT,"
								"comment_scores INT,"
								"comment_up INT,"
								"comment_down INT,"
                                "PRIMARY KEY (comment_id,comment_floor)) default charset = utf8")

		bbsask_table_sql = ("create table bbsask ( "
								"ask_id INT NOT NULL,"
								"ask_url VARCHAR(50),"
								"ask_person VARCHAR(30),"
								"ask_flag VARCHAR(500),"
								"ask_tittle VARCHAR(1000),"
								"ask_time VARCHAR(20),"
								"ask_context LONGTEXT,"
                                "PRIMARY KEY (ask_id)) default charset = utf8")

		person_table_sql = ("create table person ( "
								"user_id VARCHAR(30) NOT NULL,"
								"user_url VARCHAR(50) NOT NULL,"
								"person_nick_name VARCHAR(100),"
								"person_detail VARCHAR(1000),"
								"person_sign VARCHAR(1000),"
								"person_scores_label VARCHAR(1000),"
								"person_field VARCHAR(3000),"
								"person_skill VARCHAR(3000),"
								"person_edu VARCHAR(1000),"
								"person_job VARCHAR(1000),"
								"person_email VARCHAR(100),"
								"person_mobile VARCHAR(30),"
								"person_qq VARCHAR(30),"
								"person_wexin VARCHAR(30),"
								"focus_num INT,"
								"person_focus VARCHAR(500),"
								"befocus_num INT,"
								"person_befocus VARCHAR(500),"
                                "PRIMARY KEY (user_id)) default charset = utf8")

		self.dbHelper.createTable(visitlist_table_sql)
		self.dbHelper.createTable(topicmap_table_sql)
		self.dbHelper.createTable(forumlist_table_sql)
		self.dbHelper.createTable(bbscomment_table_sql)
		self.dbHelper.createTable(bbsask_table_sql)
		self.dbHelper.createTable(person_table_sql)



	# test insert data
	def testSelect(self):
		sql="select count(*) from bbscomment"
		sql2= ("select TABLE_NAME, concat(truncate(data_length/1024/1024,2),' MB') as data_size,"
    			"concat(truncate(index_length/1024/1024,2),' MB') as index_size"
    			"from information_schema.tables where TABLE_SCHEMA ='csdnbbs'"
    			"group by TABLE_NAME"
    			"order by data_length desc;")
		self.dbHelper.select(sql)

if __name__=="__main__":
	testDBHelper=TestDBHelper()

	testDBHelper.testCreateDatabase()
	testDBHelper.testCreateTable()
	# testDBHelper.testSelect()
