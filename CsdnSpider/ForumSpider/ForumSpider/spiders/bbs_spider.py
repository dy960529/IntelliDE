# #!/usr/bin/env python
# # encoding: utf-8
#
# import os
# import re
# import scrapy
# from scrapy.loader import ItemLoader
# from ForumSpider.items import BbsComment, BbsAsk, Person
# from scrapy.spiders import Spider
# from scrapy.http import Request, FormRequest
# from scrapy.selector import Selector
#
# class BbsSpider(scrapy.Spider):
# 	handle_httpstatus_list = [403]
# 	name = 'bbs_spider'
# 	allowed_domains = ['bbs.csdn.net','my.csdn.net']
# 	start_urls = []
# 	curdir = os.path.abspath('./bbspage/args')
# 	urlfile = file(curdir + '/bbs_forum_urls.txt')
# 	for url_item in urlfile:
# 		forum_url_link_home = url_item[0:-1]
# 		# forum_url_link_closed = forum_url_link_home + '/closed'
# 		# forum_url_link_recommand = forum_url_link_home + '/recommend'
# 		start_urls.append(forum_url_link_home)
#
#
# 	def parse(self, response):
# 		cur_url = response._url
# 		sels = Selector(response)
# 		user_urls = sels.xpath('//div[@class="detailed"]/child::table/descendant::dl/dd[3]/a/@href').extract()
# 		for user_url in user_urls:
# 			yield Request(user_url, meta = {
# 				'user_url': user_url }, callback = self.parse_person)
#
# 		floor = 0
# 		p = re.compile('((\\n|\\t|\\r)+( )*)+')
# 		if re.search('page', cur_url):
# 			comment_id = re.search('\\d+', cur_url).group(0)
# 			for sel in sels.xpath('//div[@class="detailed"]/child::table'):
# 				comment_item = BbsComment()
# 				comment_item['comment_id'] = comment_id
# 				comment_item['comment_floor'] = p.sub(' ', ' '.join(sel.xpath('descendant::div/span[@class="fr"]/a/text()').extract()))
# 				comment_item['comment_person_url'] = p.sub(' ', ' '.join(sel.xpath('descendant::dl/dd[3]/a/@href').extract()))
# 				comment_item['comment_time'] = p.sub(' ', ' '.join(sel.xpath('descendant::div/span[@class="time"]/text()').extract()))
# 				comment_item['comment_context'] = p.sub(' ', ' '.join(sel.xpath('descendant::td/div[@class="post_body"]/text()').extract()))
# 				comment_item['comment_scores'] = p.sub(' ', ' '.join(sel.xpath('descendant::div/span[@class="fr"]/text()').extract()))
# 				comment_item['comment_up'] = p.sub(' ', ' '.join(sel.xpath('descendant::div/div[@class="fr"]/a[1]/text()').extract()))
# 				comment_item['comment_down'] = p.sub(' ', ' '.join(sel.xpath('descendant::div/div[@class="fr"]/a[2]/text()').extract()))
# 				yield comment_item
#
# 		else:
# 			comment_id = re.search('\\d+', cur_url).group(0)
# 			ask_id = comment_id
# 			ask_url = cur_url
# 			for sel in sels.xpath('//div[@class="detailed"]/child::table'):
# 				if floor == 0:
# 					ask_item = BbsAsk()
# 					ask_item['ask_id'] = ask_id
# 					ask_item['ask_url'] = ask_url
# 					ask_item['ask_person_url'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="detailed"]/table[1]/descendant::dl/dd[3]/a/@href').extract()))
# 					ask_item['ask_class'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="bread_nav"]/child::a/text()').extract()))
# 					ask_item['ask_tittle'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="detail_title"]/h1/child::span/text()').extract()))
# 					ask_item['ask_time'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="detailed"]/table[1]/descendant::div/span[@class="time"]/text()').extract()))
# 					ask_item['ask_context'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="detailed"]/table[1]/descendant::td/div[@class="post_body"]/text()').extract()))
# 					yield ask_item
# 					floor = floor + 1
# 					continue
# 				comment_item = BbsComment()
# 				comment_item['comment_id'] = comment_id
# 				comment_item['comment_floor'] = p.sub(' ', ' '.join(sel.xpath('descendant::div/span[@class="fr"]/a/text()').extract()))
# 				comment_item['comment_person_url'] = p.sub(' ', ' '.join(sel.xpath('descendant::dl/dd[3]/a/@href').extract()))
# 				comment_item['comment_time'] = p.sub(' ', ' '.join(sel.xpath('descendant::div/span[@class="time"]/text()').extract()))
# 				comment_item['comment_context'] = p.sub(' ', ' '.join(sel.xpath('descendant::td/div[@class="post_body"]/text()').extract()))
# 				comment_item['comment_scores'] = p.sub(' ', ' '.join(sel.xpath('descendant::div/span[@class="fr"]/text()').extract()))
# 				comment_item['comment_up'] = p.sub(' ', ' '.join(sel.xpath('descendant::div/div[@class="fr"]/a[1]/text()').extract()))
# 				comment_item['comment_down'] = p.sub(' ', ' '.join(sel.xpath('descendant::div/div[@class="fr"]/a[2]/text()').extract()))
# 				yield comment_item
#
# 		next_page = sels.xpath('//a[@class="next"]/@href').extract()
# 		if next_page:
# 			next_url = 'http://bbs.csdn.net' + next_page[0]
# 			yield Request(next_url, callback = self.parse)
#
#
# 	def parse_person(self, response):
# 		person_item = Person()
# 		sel = Selector(response)
# 		p = re.compile('((\\n|\\t|\\r)+( )*)+')
# 		person_item['user_url'] = response.meta['user_url']
# 		person_item['person_nick_name'] = p.sub(' ', ' '.join(sel.xpath('//dt[@class="person-nick-name"]/span/text()').extract()))
# 		person_item['person_detail'] = p.sub(' ', ' '.join(sel.xpath('string(//dd[@class="person-detail"])').extract()))
# 		person_item['person_sign'] = p.sub(' ', ' '.join(sel.xpath('//dd[@class="person-sign"]/text()').extract()))
# 		person_item['person_scores_label'] = p.sub(' ', ' '.join(sel.xpath('//span[@class="scores"]/child::em/@class').extract()))
# 		# ***********************************
# 		# The XPath down is wrong!
# 		person_item['person_field'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="field"]/div[@class="tags clearfix"]/child::div/span[1]/text()').extract()))
# 		person_item['person_skill'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="skill"]/div[@class="tags clearfix"]/child::div/span[1]/text()').extract()))
# 		person_item['person_edu'] = p.sub(' ', ' '.join(sel.xpath('string(//div[@class="person_education"])').extract()))
# 		person_item['person_job'] = p.sub(' ', ' '.join(sel.xpath('string(//div[@class="person_job"])').extract()))
#
# 		person_item['person_email'] = p.sub(' ', ' '.join(sel.xpath('//span[@nodetype="email"]/text()').extract()))
# 		person_item['person_mobile'] = p.sub(' ', ' '.join(sel.xpath('//span[@nodetype="modile"]/text()').extract()))
# 		person_item['person_qq'] = p.sub(' ', ' '.join(sel.xpath('//span[@nodetype="qq"]/text()').extract()))
# 		person_item['person_wexin'] = p.sub(' ', ' '.join(sel.xpath('//span[@nodetype="weixin"]/text()').extract()))
# 		# The XPath up is wrong!
# 		# ***********************************
# 		person_item['focus_num'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="focus"]/div[1]/span/text()').extract()))
# 		person_item['person_focus'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="focus"]/div[2]/child::a/@href').extract()))
# 		person_item['befocus_num'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="focus beFocus"]/div[1]/span/text()').extract()))
# 		person_item['person_befocus'] = p.sub(' ', ' '.join(sel.xpath('//div[@class="focus beFocus"]/div[2]/child::a/@href').extract()))
# 		yield person_item
