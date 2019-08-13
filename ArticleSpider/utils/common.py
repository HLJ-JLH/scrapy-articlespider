# -*- coding: utf-8 -*-

__author__ = 'hlj'
import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest() #抽取摘要

if __name__ == "__main__":
    pass
   # print(get_md5("http://cnblogs.com".encode('utf-8')))