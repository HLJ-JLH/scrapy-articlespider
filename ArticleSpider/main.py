# -*- coding: utf-8 -*-

__author__ = "hlj"

from scrapy.cmdline import execute
import sys
import os

#获取当前main文件所在目录
#print(os.path.abspath(__file__))                  #E:\pythonscrapymuke\boke\ArticleSpider\ArticleSpider\main.py
#print(os.path.dirname(os.path.abspath(__file__))) #E:\pythonscrapymuke\boke\ArticleSpider\ArticleSpider
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "cnblogs"])
