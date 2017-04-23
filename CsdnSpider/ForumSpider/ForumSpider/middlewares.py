import os,smtplib
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from email.mime.text import MIMEText
from email.header import Header
from scrapy import cmdline
from time import sleep

class SleepRetryMiddleware(RetryMiddleware):
	def __init__(self, settings):
		RetryMiddleware.__init__(self, settings)

	# http://bbs.csdn.net/human_validations/new
	def process_response(self, request, response, spider):
		if response.status in [403]:
			valideURL = "ValideURL http://bbs.csdn.net/human_validations/new"
			valideCodeInput = "Please input the right validecode!"
			print valideCodeInput
			print valideURL
			# cmdline.execute("python bbspage/valide/valide.py".split())
			sleep(60)  # 2 minutes
			#self.send_email()
			reason = response_status_message(response.status)
			return self._retry(request, reason, spider) or response

		return super(SleepRetryMiddleware, self).process_response(request, response, spider)

	def send_email(self):
		mail_host="mail.act.buaa.edu.cn"
		mail_user="zhouql"
		mail_pass="102815"

		sender = 'zhouql@act.buaa.edu.cn'
		receivers = ['zhouqilin@buaa.edu.cn']

		message = MIMEText('Scrapy spider valide auth Request!', 'plain', 'utf-8')
		message['From'] = Header("Scrapy Spider", 'utf-8')
		message['To'] =  Header("zhouqilin", 'utf-8')

		subject = 'CSDN Spider'
		message['Subject'] = Header(subject, 'utf-8')

		try:
			smtpObj = smtplib.SMTP()
			smtpObj.connect(mail_host, 25)
			smtpObj.login(mail_user,mail_pass)
			smtpObj.sendmail(sender, receivers, message.as_string())
			print "SUCCESS"
		except smtplib.SMTPException:
			print "Error: FAIL"
