#!/usr/bin/env python
# coding=utf-8
#########################################################################
# Author: 1396705216@qq.om
# Created Time: Sun 27 Aug 2017 04:29:27 PM CST
# File Name: get_ctr.py
# Description:获得点击率预估
# 功能：输入一条action数据，给出其点击率估计
# 输入：用户访问记录
# 输出：点击率估计
######################################################################
import json
import time
from datetime import *
import sys
sys.path.append("/root/base/")
sys.path.append('/root/liblinear-2.11/python')
from liblinear import *
from liblinearutil import *
import build_feature
reload(sys)
sys.setdefaultencoding('utf8')

model_ = '' #liblinear模型
model_ = load_model("ctr.train.model") #加载模型
build_feature.load_feature_id() #加载字典id

"""
功能：获得一个action的点击率预估
输入：action，dict，字段名包括uid，source_vid,update_time
返回：点击概率估计
"""
def get_ctr(action):
    vsm = build_feature.get_vsm(action)
    #print vsm
    if -1 == vsm:#这里有问题
        return 0
    #写成liblinear需要的格式
    tmp_dict = {} #临时词典,key为特征id,value为特征值
    if len(vsm)>0:
        for item in vsm:
            tmp_dict[item[0]] = item[1]

        y = []
        x = []
        x.append(tmp_dict)
        #liblinear python接口

        p_labs,p_acc,p_vals = predict(y,x,model_,'-b 1')
        #同学们自己填写，获得点击概率
        label_list = model_.get_labels()
        index = label_list.index(1)
        return p_vals[0][index]
    else:
        return -1


"""
功能：获得基于点击率预估的推荐
输入：uid，用户id
输入：video_id_list,候选视频列表
返回：根据点击率预估排序后的视频列表
"""
def get_ctr_recommend(uid, video_id_list):
    #构造action历史
    update_time = datetime.now()
    video_id_score_list = []
    for video_id in video_id_list:
        action = {}
        action = {}
        action["uid"] = uid
        action["source_vid"] = str(video_id)
        action["update_time"] = update_time
        #========================这里
        ctr = get_ctr(action) #ctr预估
        video_id_score_list.append([video_id, ctr])

       # for video_id in video_id_list:
       #同学们完成这一部分,其中ctr为获取的video_id的点击率预估
        # ctr = 0
        # video_id_score_list.append([video_id, ctr])

    #排序
    score_list = sorted(video_id_score_list,key=lambda d:d[1], reverse=True)
    #print score_list
    recommend_video_list = [video_id for video_id,score in score_list]

    return recommend_video_list


if __name__=="__main__":
    uid = "541132"#用户id    根据用户进行对下边的两个视频的点击率估计
    video_id_list = ["4445027","4445026"] #输入一条action数据，给出其点击率估计
    print get_ctr_recommend(uid, video_id_list)



