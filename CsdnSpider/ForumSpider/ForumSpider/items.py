# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TopicPage(scrapy.Item):
	topic_id = scrapy.Field()
	topic_type = scrapy.Field()
	topic_name = scrapy.Field()
	topic_detail = scrapy.Field()
	page_num = scrapy.Field()
	forum_sum = scrapy.Field()
	pass

class ForumVisit(scrapy.Item):
	visit_topic = scrapy.Field()
	visit_type = scrapy.Field()
	visit_page = scrapy.Field()
	pass

class ForumItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	forum_id = scrapy.Field() #key topic id
	forum_class = scrapy.Field() # 话题分类
	forum_type = scrapy.Field() # 话题性质
	forum_title = scrapy.Field()

	forum_url = scrapy.Field() #foreign key
	forum_point = scrapy.Field() #int
	forum_answer_number = scrapy.Field() #int
	forum_question_user = scrapy.Field() #user id

	forum_question_time = scrapy.Field()
	forum_update_user = scrapy.Field() #user id
	forum_update_time = scrapy.Field()

	pass
# bbscomment table
class BbsComment(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	comment_id = scrapy.Field() #(id,floor) is key,int
	comment_floor = scrapy.Field() #int
	comment_person = scrapy.Field() #user id
	comment_time = scrapy.Field()

	comment_context = scrapy.Field() #text
	comment_scores = scrapy.Field() #int
	comment_up = scrapy.Field() #int
	comment_down = scrapy.Field() #int

	pass

# bbsask table
class BbsAsk(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	ask_id = scrapy.Field() #id is key,id is the url end number,int
	ask_url = scrapy.Field()
	ask_person = scrapy.Field() #user id
	ask_flag = scrapy.Field()
	ask_tittle = scrapy.Field()
	ask_time = scrapy.Field()
	ask_context = scrapy.Field() #html text

	pass

# person table
class Person(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	user_id = scrapy.Field() #key user name
	user_url = scrapy.Field()
	person_nick_name = scrapy.Field()
	person_detail = scrapy.Field()
	person_sign = scrapy.Field()

	person_scores_label = scrapy.Field()
	person_field = scrapy.Field()
	person_skill = scrapy.Field()
	person_edu = scrapy.Field()

	person_job = scrapy.Field()
	person_email = scrapy.Field()
	person_mobile = scrapy.Field()
	person_qq = scrapy.Field()
	person_wexin = scrapy.Field()

	focus_num = scrapy.Field() #int
	person_focus = scrapy.Field() #use space to splite users' name
	befocus_num = scrapy.Field() #int

	person_befocus = scrapy.Field() #use space key to splite users' name

	pass
