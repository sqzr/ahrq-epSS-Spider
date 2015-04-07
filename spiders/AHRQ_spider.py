from scrapy import Selector
import scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from pyquery import PyQuery
from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc


__author__ = 'Administrator'

class AHRQSpider(CrawlSpider):
    name = "ahrq"
    allowed_domains = ["epss.ahrq.gov"]
    start_urls = [
        "http://epss.ahrq.gov/ePSS/Topics.do"
    ]
    rules = [
        Rule(sle(
            allow=("/ePSS/TopicDetails.do"),
            allow_domains=("epss.ahrq.gov"),
            restrict_xpaths=('//*[@id="maincontent"]/ul')),
        follow=False,callback='parse_item')
    ]

    def parse_item(self, response):
        sel = Selector(response)
        query = PyQuery(response.body)
        item = AhrqItem()
        title = sel.xpath('//*[@id="content"]/h2/text()').extract()[0].encode("utf-8")
        contenthtml = query("#maincontent").html().encode("utf-8")
        contenttext = dehtml(contenthtml)
        item['url'] =  response.url
        item['title'] = title
        item['tab'] = 'Recommendations'
        item['contenthtml'] = contenthtml
        item['contenttext'] = contenttext
        yield item
        yield Request(response.url + "&tab=1",callback=self.parse_item_tab1)

    def parse_item_tab1(self,response):
        sel = Selector(response)
        query = PyQuery(response.body)
        item = AhrqItem()
        title = sel.xpath('//*[@id="content"]/h2/text()').extract()[0].encode("utf-8")
        contenthtml = query("#maincontent").html().encode("utf-8")
        contenttext = dehtml(contenthtml)
        item['url'] =  response.url
        item['title'] = title
        item['tab'] = 'Clinical Considerations'
        item['contenthtml'] = contenthtml
        item['contenttext'] = contenttext
        yield item
        yield Request(response.url + "&tab=2",callback=self.parse_item_tab2)

    def parse_item_tab2(self,response):
        sel = Selector(response)
        query = PyQuery(response.body)
        item = AhrqItem()
        title = sel.xpath('//*[@id="content"]/h2/text()').extract()[0].encode("utf-8")
        contenthtml = query("#maincontent").html().encode("utf-8")
        contenttext = dehtml(contenthtml)
        item['url'] =  response.url
        item['title'] = title
        item['tab'] = 'Rationale'
        item['contenthtml'] = contenthtml
        item['contenttext'] = contenttext
        yield item
        yield Request(response.url + "&tab=3",callback=self.parse_item_tab3)

    def parse_item_tab3(self,response):
        sel = Selector(response)
        query = PyQuery(response.body)
        item = AhrqItem()
        title = sel.xpath('//*[@id="content"]/h2/text()').extract()[0].encode("utf-8")
        contenthtml = query("#maincontent").html().encode("utf-8")
        contenttext = dehtml(contenthtml)
        item['url'] =  response.url
        item['title'] = title
        item['tab'] = 'Tools'
        item['contenthtml'] = contenthtml
        item['contenttext'] = contenttext
        yield item


class AhrqItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    tab = scrapy.Field()
    contenthtml = scrapy.Field()
    contenttext = scrapy.Field()
    url = scrapy.Field()
    pass

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text