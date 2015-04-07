# -*- coding: utf-8 -*-

# Scrapy settings for AHRQ project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'AHRQ'

SPIDER_MODULES = ['AHRQ.spiders']
NEWSPIDER_MODULE = 'AHRQ.spiders'

ITEM_PIPELINES = ['AHRQ.pipelines.HtmlP']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'AHRQ (+http://www.yourdomain.com)'
