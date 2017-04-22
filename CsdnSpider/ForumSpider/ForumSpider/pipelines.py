# ubuntu mysqldb install: sudo apt-get install python-mysql
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import codecs
import json
import logging
from logging import log
from scrapy.conf import settings
from ForumSpider.items import BbsComment,BbsAsk,Person,ForumItem,ForumVisit,TopicPage

class BbspageJsonPipeline(object):

	def __init__(self):
		self.file = codecs.open('./ForumSpider/output/csdnbbs.json','w',encoding='utf-8')

	def process_item(self, item, spider):
		line = json.dumps(dict(item))+'\n'
		self.file.write(line)  # JSON file Chinese not right
		# self.file.write(line.decode('unicode_escape')) # The JSON file is not fixed,but Chinese is right!
		return item

	def close_spider(self,spider):
		self.file.close()

class BbspageSqlPipeline(object):

	def __init__(self,dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls,settings):
		dbparams=dict(
			host=settings['MYSQL_HOST'],
			db=settings['MYSQL_DBNAME'],
			user=settings['MYSQL_USER'],
			passwd=settings['MYSQL_PASSWD'],
			charset='utf8',
			cursorclass=MySQLdb.cursors.DictCursor,
			use_unicode=False,
		)
		dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)
		return cls(dbpool)

	def process_item(self, item, spider):
		if isinstance(item,ForumVisit):
			V = self.dbpool.runInteraction(self._ForumVisit_insert, item)
			V.addErrback(self._handle_error, item, spider)
			return V
		elif isinstance(item,ForumItem):
			F = self.dbpool.runInteraction(self._forumList_insert, item)
			F.addErrback(self._handle_error, item, spider)
			return F
		elif isinstance(item,BbsComment):
			a = self.dbpool.runInteraction(self._bbsComment_insert, item)
			a.addErrback(self._handle_error, item, spider)
			return a
		elif isinstance(item,Person):
			b = self.dbpool.runInteraction(self._person_insert, item)
			b.addErrback(self._handle_error, item, spider)
			return b
		elif isinstance(item,BbsAsk):
			c = self.dbpool.runInteraction(self._bbsAsk_insert, item)
			c.addErrback(self._handle_error, item, spider)
			return c
		elif isinstance(item,TopicPage):
			d = self.dbpool.runInteraction(self._TopicPage_insert, item)
			d.addErrback(self._handle_error, item, spider)
			return d
		else:
			print ("Error: Wrong Item!")

	def _ForumVisit_insert(self, conn, item):
		sql = 'insert into visitlist (visit_topic, visit_type, visit_page) values(%s,%s,%s)'
		values_params = (item['visit_topic'],item['visit_type'],item['visit_page'])
		conn.execute(sql,values_params)

	def _TopicPage_insert(self, conn, item):
		sql = 'insert into topicmap (topic_id, topic_type, topic_name, topic_detail, page_num, forum_sum, spider_flag) values(%s,%s,%s,%s, %s,%s,%s)'
		values_params = (item['topic_id'],item['topic_type'],item['topic_name'],item['topic_detail'],item['page_num'],item['forum_sum'],"0")
		conn.execute(sql,values_params)

	def _forumList_insert(self, conn, item):
		sql = 'insert into forumlist (forum_id,forum_class,forum_type,forum_title, forum_url,forum_point,forum_answer_number,forum_question_user, forum_question_time,forum_update_user,forum_update_time,spider_flag) values(%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s)'
		values_params = (item['forum_id'],item['forum_class'],item['forum_type'],item['forum_title'], item['forum_url'],item['forum_point'],item['forum_answer_number'],item['forum_question_user'],item['forum_question_time'], item['forum_update_user'],item['forum_update_time'],"0")
		conn.execute(sql,values_params)

	def _bbsComment_insert(self, conn, item):
		sql = 'insert into bbscomment (comment_id,comment_floor,comment_person_url,comment_time,comment_context,comment_scores,comment_up,comment_down) values(%s,%s,%s,%s, %s,%s,%s,%s)'
		values_params = (item['comment_id'],item['comment_floor'],item['comment_person_url'],item['comment_time'], item['comment_context'],item['comment_scores'],item['comment_up'],item['comment_down'])
		conn.execute(sql,values_params)

	def _bbsAsk_insert(self, conn, item):
		sql = 'insert into bbsask(ask_id,ask_url,ask_person_url,ask_class,ask_tittle,ask_time,ask_context) values(%s,%s,%s,%s, %s,%s,%s)'
		values_params = (item['ask_id'],item['ask_url'],item['ask_person_url'],item['ask_class'], item['ask_tittle'],item['ask_time'],item['ask_context'])
		conn.execute(sql,values_params)

	def _person_insert(self, conn, item):
		sql = 'insert into person(user_url,person_nick_name,person_detail,person_sign, person_scores_label,person_field,person_skill,person_edu,person_job,person_email,person_mobile,person_qq, person_wexin,focus_num,person_focus,befocus_num, person_befocus) values(%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s, %s)'
		values_params = (item['user_url'],item['person_nick_name'],item['person_detail'],item['person_sign'], item['person_scores_label'],item['person_field'],item['person_skill'],item['person_edu'], item['person_job'],item['person_email'],item['person_mobile'],item['person_qq'], item['person_wexin'],item['focus_num'],item['person_focus'],item['befocus_num'],item['person_befocus'])
		conn.execute(sql,values_params)

	def _handle_error(self, failure, item, spider):
		print failure

		# logging.basicConfig(level=logging.DEBUG,
		# 		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		# 		datefmt='%a, %d %b %Y %H:%M:%S',
		# 		filename='myapp.log',
		# 		filemode='w')

		# logging.debug('This is debug message')
		# logging.info('This is info message')
		# logging.warning('This is warning message')
