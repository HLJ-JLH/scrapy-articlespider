# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import ArticlespiderItem
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['https://www.cnblogs.com']

    def parse(self, response):
        """
        1 获取文章列表页中的文章url并交给解析函数进行具体字段解析
        2 获取下一页的url病交给scrapy进行下载
        :param response:
        :return:
        """
        #解析列表页所有文章的url
        #post_urls = response.xpath('//a[@class="titlelnk"]/@href').extract()
        #post_urls = response.css('.titlelnk::attr(href)').extract()
        post_nodes = response.css('.post_item_body')
        for post_node in post_nodes:
            #extract_first("")取不到数据时，默认值为空
            image_url = post_node.css("p a img::attr(src)").extract_first("")
            post_url  = post_node.css('h3 a::attr(href)').extract_first("")
            print("wwwwwwwww %s", post_url)#https://www.cnblogs.com/yaohong/p/11331154.html
            #https://www.cnblogs.com https://www.cnblogs.com/yaohong/p/11331154.html
            print("qqqqqqqqq %s  %s", response.url, parse.urljoin(response.url, post_url))
            print("iiiiiiiii %s", image_url)
            yield Request(url=parse.urljoin(response.url, post_url),meta={"front_image_url": image_url}, callback=self.parse_detail)

        #提取下一页的url
        urls = response.css('.pager a::attr(class)').extract()
        for ele in urls:
            if re.match('p_(\d+) current', ele) and urls.index(ele) + 1 != len(urls):
                temp = urls[urls.index(ele) + 1]
                re_match = re.match('.*?(\d+).*', temp)

                yield Request('https://www.cnblogs.com/#p' + re_match.group(1), callback=self.parse)

    def parse_detail(self, response):
        #提取文章的具体字段
        #返回为SelectorList，方便进一步做selector筛选（嵌套selector）
        #front_image_url = response.meta['front_image_url']
        #使用get方法可以传递默认值，建议使用
        articleItem = ArticlespiderItem() #实例化
        #raise ValueError('Missing scheme in request url: %s' % self._url)改为列表
        # articleItem['front_image_url'] = [response.meta.get('front_image_url','')]
        # articleItem['title'] = response.xpath('//a[@id="cb_post_title_url"]/text()').extract_first("")
        # articleItem['url_object_id'] = get_md5(response.url)

        # #假设字段中有日期类型的，将爬取下来的字符串转化为日期
        # try
        #     date = datetime.datetime.strptime(date, "%Y/%m/%d").date()
        # except Exception as e:
        #     date = datetime.datetime.now().date()  #获取当前日期


        #通过itemLoader加载item
        item_loader = ItemLoader(item=ArticlespiderItem(), response=response)
        #item_loader.add_css()
        item_loader.add_xpath('title', '//a[@id="cb_post_title_url"]/text()')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_value('front_image_url', [response.meta.get('front_image_url','')])

        articleItem = item_loader.load_item() #articleItem里面所有的项默认都是list




        yield articleItem


