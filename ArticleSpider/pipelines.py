# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi #异步化操作
import codecs  #避免编码方面的工作
import json
import pymysql
import pymysql.cursors

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8') #打开文件
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)  #写入文件
        return item
    def spider_closed(self, spider):
        self.file.close() #关闭文件

class JsonExporterPipeline(object):
    #调用scrapy提供的JsonItemExporter导出的json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class ArticleImagePipeline(ImagesPipeline):
    #重载函数
    def item_completed(self, results, item, info):
        if "front_image_path" in item:
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
        return item

class MysqlPipeline(object):
    #自定义方法插入mysql数据库，同步机制
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root','123456','article_spider',charset = 'utf8',
                                    use_unicode = True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article values(%s, %s, %s, %s)
        """

        self.cursor.execute(insert_sql, (item['title'],item['front_image_url'],item['front_image_path'],item['url_object_id']))
        self.conn.commit()

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    #将配置写入setting,异步防止堵塞，有连接池
    @classmethod
    def from_settings(cls, settings): #自定义主键或扩展时有用
        #通过前面的connect一直点进去之后，参数名称要一致
        dbparams =  dict(
            host = settings["MYSQL_HOST"],
            db  = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True
         )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparams)
        return cls(dbpool) #实例化对象


    def process_item(self, item, spider):
        #使用twisted将mysql插入变为异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #异步错误处理

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        insert_sql = """
            insert into article values(%s, %s, %s, %s)
        """
        #自动提交
        cursor.execute(insert_sql, (item['title'],item['front_image_url'],item['front_image_path'],item['url_object_id']))


















