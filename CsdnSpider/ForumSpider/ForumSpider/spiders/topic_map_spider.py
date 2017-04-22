#!/usr/bin/env python
# encoding: utf-8

import os
import re
import scrapy
from scrapy.loader import ItemLoader
from ForumSpider.items import TopicPage
from scrapy.spiders import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

class MapSpider(scrapy.Spider):
	handle_httpstatus_list = [403]
	name = 'topic_map_spider'
	allowed_domains = ['bbs.csdn.net','my.csdn.net']
	start_urls = ["http://bbs.csdn.net/map"]

	def parse(self, response):
		cur_url = response._url
		sels = Selector(response)
		forums_list_urls_end = sels.xpath('//div[@class="map"]/descendant::a/@href').extract()
		for forums_url_end in forums_list_urls_end:
			forums_list_url = 'http://bbs.csdn.net' + forums_url_end
			forum_class = forums_url_end[8:]
			yield Request(forums_list_url + '/recommend', meta = {'forum_class': forum_class ,
				'forum_type': 'recommend' }, callback = self.parse_topic)
			yield Request(forums_list_url+'/closed', meta = {'forum_class': forum_class ,
				'forum_type': 'closed' }, callback = self.parse_topic)
			yield Request(forums_list_url, meta = {'forum_class': forum_class ,
				'forum_type': 'follow' }, callback = self.parse_topic)

	def parse_topic(self, response):
	 	topic_item = TopicPage()
	 	sel = Selector(response)
	 	topic_item['topic_id'] = response.meta['forum_class']
		topic_item['topic_type'] = response.meta['forum_type']
		topic_item['topic_name'] = sel.xpath('//div[@class="conts"]/dl[1]/dt[1]/h1/text()').extract()
		topic_item['topic_detail'] = sel.xpath('//div[@class="conts"]/dl[1]/dd[2]/text()').extract()
		page_num_str = re.findall(r'\d+',"".join(response.xpath('//div[@class="page_nav"]/ul[1]/li[last()]/span[2]/text()').extract()))
		forum_sum_str = re.findall(r'\d+',"".join(response.xpath('//div[@class="page_nav"]/ul[1]/li[last()]/span[1]/text()').extract()))
		if page_num_str:
			topic_item['page_num'] = page_num_str[1]
		else:
			topic_item['page_num'] = "0"
		if forum_sum_str:
			topic_item['forum_sum'] = forum_sum_str[1]
		else:
			topic_item['forum_sum'] = "0"

		yield topic_item
