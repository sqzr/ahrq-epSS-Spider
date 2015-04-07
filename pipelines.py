# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AhrqPipeline(object):
    def process_item(self, item, spider):
        return item


class HtmlP(object):
    def __init__(self):
        print '输出'

    def process_item(self,item,spider):
        titlename = item['title'].replace('/','').replace(':','').replace('/','')
        htmlfile = file(titlename + '---' + item['tab'] + '.html','w')
        textfile = file(titlename + '---' + item['tab'] + '.txt','w')
        htmlfile.write(item['contenthtml'])
        textfile.write(item['contenttext'])
        textfile.close()
        htmlfile.close()
