# coding=utf-8
# 配置文件配置阿里云搜索
#File_name:cofig.py
import os
import uuid

app_key = "LTAIzGBPGOHIHZex" #阿里云的key
app_secret = "EYXphaNNC6gRQXfr1ilKpcW6dMv0Jj" #阿里云账号：lebin_neu  阿里云的secret
base_url = 'http://opensearch-cn-beijing.aliyuncs.com'# 我建立的openserch应用的 公网API域名
index_name = 't_' + str(uuid.uuid4()).replace('-', '')[2:30] #都不变  这个是做什么的？？
build_index_name = 'short_video'#数据库名字

try:
    import requests
    client_name = 'requests'
except ImportError:
    client_name = 'httplib'