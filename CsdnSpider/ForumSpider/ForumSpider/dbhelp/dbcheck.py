import MySQLdb
import os,sys,smtplib
import time
from time import sleep
from email.mime.text import MIMEText
from email.header import Header
from scrapy.utils.project import get_project_settings

class dbTest():

	def __init__(self):
		self.settings=get_project_settings()

		self.host=self.settings['MYSQL_HOST']
		self.port=self.settings['MYSQL_PORT']
		self.user=self.settings['MYSQL_USER']
		self.passwd=self.settings['MYSQL_PASSWD']
		self.db=self.settings['MYSQL_DBNAME']

	def testSelect(self):
		conn=MySQLdb.connect(host=self.host,
							 port=self.port,
							 user=self.user,
							 passwd=self.passwd,
							 db=self.db,
							 charset='utf8')
		cur=conn.cursor()

		sql1="select count(*) from bbsask"
		cur.execute(sql1)
		for data1 in cur.fetchall():
			num1 = data1[0]

		sql2="select count(*) from bbscomment"
		cur.execute(sql2)
		for data2 in cur.fetchall():
			num2 = data2[0]

		sql3="select count(*) from person"
		cur.execute(sql3)
		for data3 in cur.fetchall():
			num3 = data3[0]

		sql4="select count(*) from forumlist"
		cur.execute(sql4)
		for data4 in cur.fetchall():
			num4 = data4[0]

		sql5="select count(*) from topicmap"
		cur.execute(sql5)
		for data5 in cur.fetchall():
			num5 = data5[0]

		sql6="select count(*) from visitlist"
		cur.execute(sql6)
		for data6 in cur.fetchall():
			num6 = data6[0]

		cur.close()
		conn.close()
		print "> bbsask = " + str(num1)
		print "> comment= " + str(num2)
		print "> person = " + str(num3)
		print "> forumlist = " + str(num4)
		print "> topicmap= " + str(num5)
		print "> visitlist = " + str(num6)

		return num1+num2+num3

	def send_email(self):
		mail_host="mail.act.buaa.edu.cn"
		mail_user="zhouql"
		mail_pass="102815"

		sender = 'zhouql@act.buaa.edu.cn'
		receivers = ['zhouqilin@buaa.edu.cn']

		cur_time = "" + time.strftime("%Y-%m-%d  %H:%M:%S",time.localtime(time.time()))

		message = MIMEText('Scrapy spider valide auth Request!', 'plain', 'utf-8')
		message['From'] = Header("Scrapy Spider", 'utf-8')
		message['To'] =  Header("zhouqilin", 'utf-8')

		subject = 'ERROR from CSDN spider at: ' + cur_time
		message['Subject'] = Header(subject, 'utf-8')

		try:
			smtpObj = smtplib.SMTP()
			smtpObj.connect(mail_host, 25)
			smtpObj.login(mail_user,mail_pass)
			smtpObj.sendmail(sender, receivers, message.as_string())
			print "SUCCESS"
		except smtplib.SMTPException:
			print "Error: FAIL"

	def pic_str(self):
		chaojiying = Chaojiying_Client('kylin93', '102815', ' 893171')
		im = open('captcha.png', 'rb').read()
		picstr = chaojiying.PostPic(im, 3006)['pic_str']
		return picstr

if __name__=="__main__":
	dbtest = dbTest()
	while True:
		print ""
		num_old = dbtest.testSelect()
		print "#SUM OLD = " + str(num_old)
		sleep(5)
		num_new = dbtest.testSelect()
		print "#SUM NEW = " + str(num_new)
		print "DATA add (5s) = " + str(num_new - num_old)
		if num_new - num_old == 0:
			now_time = time.strftime("%Y-%m-%d  %H:%M:%S",time.localtime(time.time()))
			print "Checktime: "+now_time
			print "ERROR: Valid code!"
			# pic_str = dbtest.pic_str()
			# print pic_str
			#dbtest.send_email()
			sleep(100)

		else:
			sleep(5)
