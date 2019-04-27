#!/usr/bin/env python
#coding=utf-8
#File_name:ali_search
# 基于内容的推荐，其实就是要建立一个搜索引擎，索引短视频的标题、标签等文本,然后在推荐的时候，使用用户的标签，搜索视频内容，获得推荐结果
import sys
import urllib2
import urllib
import re
import time
import json
import socket

from opensearch import const
from opensearch import Client
from opensearch import IndexApp
from opensearch import Search
from opensearch import Suggest
from config import app_key, app_secret, base_url, build_index_name, client_name
reload(sys)

sys.setdefaultencoding('utf8')
socket.setdefaulttimeout(20)

"""
功能:获得aliyun的搜索结果,为全or检索
输入:query_list, 搜索词列表,list
返回:阿里云的搜索结果
try:
    import requests
    client_name = 'requests'
except ImportError:
    client_name = 'httplib'
"""
def search(query_list,limit=5): # query_list 搜索词列表
    table_name = 'main' #默认配置
    index_name = build_index_name
    client = Client(app_key, app_secret, base_url, lib=client_name) #base_url = 'http://opensearch-cn-beijing.aliyuncs.com'# 我建立的openserch应用的 公网API域名 返回的是什么？？
    indexSearch = Search(client)
    indexSearch.addIndex(build_index_name)
    #query_list = ["美女", "性感"]

    query_para_list = [] #检索字符串list
    for word in query_list:
        para = "default:'"+ word + "'"#转换格式  和阿里云的开放搜索页面的搜索测试相同的格式   default:'搜索'
        query_para_list.append(para)

    indexSearch.query = " OR ".join(query_para_list) #全or检索
    #print indexSearch.query
    indexSearch.addFilter("is_download=1")#过滤结果 要求 is_download字段必须设为1的才进行检索 数据库表 video_info

    indexSearch.start = 0 #start
    indexSearch.hits = limit #limit   hits
    indexSearch.format = 'json' #数据结果格式
    ret = indexSearch.call()
    #print json.dumps(ret)
    return ret["result"]["items"]

if __name__=="__main__":
    query_list = ["美女", "性感"]# default:'美女' ''性感    中间没有逗号
    print search(query_list)

