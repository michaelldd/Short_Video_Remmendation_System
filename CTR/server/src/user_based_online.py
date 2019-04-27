#!/usr/bin/env python
#coding=utf-8
#########################################################################
# Author: 1396705216@qq.com
# Created Time: Saturday 26 Aug 2017 12:00:16 PM CST
# File Name: user_based_oneline.py
# Description: 使用sql语句,实现简单的基于用户的协同过滤推荐
# 功能：基于sql，实现实时的基于用户的协同过滤推荐
#输入：user id
#输出： 短视频推荐结果
######################################################################
import json
import time
import sys
sys.path.append("/root/base")
import sql_appbk
reload(sys)
sys.setdefaultencoding('utf8')

"""
功能:实现基于用户的协同过滤推荐
输入:uid
返回:推荐的vid列表
找到 “别的用户浏览过的vid”，按照“别的用户”中浏览过的人数从高到低排序。
"""

def recommend(uid,limit=20):   # 推荐十条视频记录  source_vid*10
    #直接通过sql语句，通过对用户记录库的查询，来获得协同过滤推荐
    # sql 语句的非文本类型要放在   双引号 " " 里面表示字符串；   单引号 ''  是SQL语句里面的
    sql = "SELECT source_vid, count(*) as score from user_action right JOIN \
             ( \
            SELECT uid,count(*) as num from user_action where source_vid in \
            (select source_vid FROM user_action where uid='"+uid+"') and uid!='" + uid +"' \
            GROUP BY uid \
            ORDER BY num DESC limit 50 \
            ) as simliar_user \
            on user_action.uid=simliar_user.uid \
            GROUP BY source_vid ORDER BY score DESC limit " + str(limit)
    result = sql_appbk.mysql_com(sql)
    vid_list = []
    for item in result:
        vid_list.append(item["source_vid"])
    return vid_list

if __name__=="__main__":
    print recommend("717")
