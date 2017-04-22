#-*-coding:utf-8-*-
from scrapy import cmdline

cmdline.execute("scrapy crawl forum_list_spider".split())
cmdline.execute("scrapy crawl topic_map_spider".split())
# cmdline.execute("scrapy crawl bbs_spider3".split())

# cmdline.execute("scrapy crawl bbs_spider4".split())
# cmdline.execute("scrapy crawl bbs_spider5".split())
