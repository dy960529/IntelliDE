#!/usr/bin/env python
# encoding: utf-8
import MySQLdb
import os
import re
import scrapy
from scrapy.loader import ItemLoader
from ForumSpider.items import BbsComment,BbsAsk,Person,ForumItem,ForumVisit,TopicPage
from scrapy.spiders import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

class BbsSpider(scrapy.Spider):
	handle_httpstatus_list = [403]
	name = 'forum_list_spider'
	allowed_domains = ['bbs.csdn.net','my.csdn.net']
	start_urls = ['http://bbs.csdn.net/map']

	def parse(self, response):

		cur_url = response._url
		sels = Selector(response)
		forums_list_urls_end = sels.xpath('//div[@class="map"]/descendant::a/@href').extract()
		for forums_url_end in forums_list_urls_end:
			forums_list_url = 'http://bbs.csdn.net' + forums_url_end
			forum_class = forums_url_end[8:]
			#print (forums_list_url,forum_class)
			yield Request(forums_list_url + '/recommend', meta = {'forum_class': forum_class ,
					'forum_type': 'recommend' }, callback = self.parse_forums_list)
			yield Request(forums_list_url+'/closed', meta = {'forum_class': forum_class ,
					'forum_type': 'closed' }, callback = self.parse_forums_list)
			yield Request(forums_list_url, meta = {'forum_class': forum_class ,
					'forum_type': 'follow' }, callback = self.parse_forums_list)


	def parse_forums_list(self,response):
		for sel in response.xpath('//tr'):
			forum_item = ForumItem()
			forum_item['forum_class'] = response.meta['forum_class']
			forum_item['forum_type'] = response.meta['forum_type']

			forum_item['forum_title'] = sel.xpath('td[1]/a/@title').extract()
			forum_item['forum_id'] = re.sub(r'\D', "", ''.join(sel.xpath('td[1]/a/@href').extract()))
			forum_item['forum_url'] = "http://bbs.csdn.net/topics/" + forum_item['forum_id']
			forum_item['forum_point'] = re.sub(r'\D', "", ''.join(sel.xpath('td[2]/text()').extract()))
			forum_item['forum_question_user'] = re.sub('http://my.csdn.net/', "", ''.join(sel.xpath('td[3]/a/@href').extract()))
			forum_item['forum_question_time'] = sel.xpath('td[3]/span[@class = "time"]/text()').extract()
			forum_item['forum_answer_number'] = re.sub(r'\D', "", ''.join(sel.xpath('td[4]/text()').extract()))
			forum_item['forum_update_user'] = re.sub('http://my.csdn.net/', "", ''.join(sel.xpath('td[5]/a/@href').extract()))
			forum_item['forum_update_time'] = sel.xpath('td[5]/span[@class = "time"]/text()').extract()
			yield forum_item

		visit_item = ForumVisit()
		visit_item['visit_topic'] = re.findall(r'/forums/(\w+)',response.url)
		T_type = re.findall(r'(closed)|(recommend)',response.url)
		if not T_type:
			visit_item['visit_type'] = "follow"
		elif T_type[0][0] == "closed":
			visit_item['visit_type'] = "closed"
		elif T_type[0][1] == "recommend":
			visit_item['visit_type'] = "recommend"
		else:
			print ("Error: Visit Type Wrong!")
		visit_item['visit_page'] = re.findall(r'page=(\d+)',response.url)
		yield visit_item

		# there is a bug,can not right request!
		next_page = sel.xpath('//a[@class="next"]/@href').extract()
		if next_page:
			next_url = 'http://bbs.csdn.net' + next_page[0]
			yield Request(next_url, callback = self.parse_forums_list)
