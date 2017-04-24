import MySQLdb
import os,sys,smtplib
import time
from time import sleep
from sqlexec import sqlexe

class user():
	def __init__(self):
		self.user_id = ""
		self.user_url = ""
		self.nick_name = ""
		self.user_detail = ""
		self.user_sign = ""
		self.focus_num = ""
		self.befocus_num = ""
		self.person_focus = ""
		self.person_befocus = ""

	def user_card(self,user_id):
		sql_exe_call = sqlexe()
		data = sql_exe_call.sql_run("select  user_id,user_url,person_nick_name,person_detail,"
				"person_sign,focus_num,befocus_num,person_focus,person_befocus "
				"from person where user_id = '"+ str(user_id)+"'")
		self.user_id = data[0][0]
		self.user_url = data[0][1]
		self.nick_name = data[0][2]
		self.user_detail = data[0][3]
		self.user_sign = data[0][4]
		self.focus_num = data[0][5]
		self.befocus_num = data[0][6]
		self.person_focus = data[0][7]
		self.person_befocus = data[0][8]
		return data

	def print_user(self):
		print ("user_id    : " + self.user_id)
		print ("user_url   : " + self.user_url)
		print ("nick_name  : " + self.nick_name)
		print ("user_detail: " + self.user_detail)
		print ("user_sign  : " + self.user_sign)
		print ("focus_num  : " + str(self.focus_num))
		print ("befocus_num: " + str(self.befocus_num))
		print ("user_focus : " + self.person_focus)
		print ("user_befocus : " + self.person_befocus)

		return


if __name__=="__main__":
	T_user = user()
	T_card = T_user.user_card("zhao4zhong1")

	T_user.print_user()
