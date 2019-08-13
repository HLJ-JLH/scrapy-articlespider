# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader

def add_str(value):
    return value + "sssss"
def return_value(value):
    pass
# def date_convert(value):
#     # try
#     #     date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
#     # except Exception as e:
#     #     date = datetime.datetime.now().date()  #获取当前日期
#       return date
class ArticleItemLoader(ItemLoader):
    #自定义ItemLoader
    default_output_processor = TakeFirst()
    #在cnblogs中使用自定义的loader(ArticleItemLoader)就可以直接全部只取出第一个，不用一个字段一个字段的TakeFirst。

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(
        input_processor = MapCompose(add_str)
        #将传递进来的值预处理，eg：title传入add_str函数进行拼接。可以写多个函数，按照从左到右的顺序调用
    )
    front_image_url = scrapy.Field()
    # front_image_url = scrapy.Field(
    #      output_processor=MapCompose(return_value)
    # #     #特殊情况，需要返回list时（default_output_processor设置返回str）。
    # #     # 覆盖default_output_processor，可以另写一个函数return_value
    # #     #mysql插入数据时也要注意只取第一个值进行插入，否则是list会报错
    # )
    front_image_path = scrapy.Field()
    url_object_id = scrapy.Field()
    url = scrapy.Field()
    #Join举例
    # tags = scrapy.Field(
    #     output_processor = Join(",") #连接
    # )
    #举例，时间的转换
    # date = scrapy.Field(
    #     input_processor=MapCompose(date_convert),
    #     output_processor=TakeFirst() #只取结果中的第一个，改变item中只能是list的现状
    # )

