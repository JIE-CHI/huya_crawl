#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 08:26:57 2020

@author: jiechi
"""
import json

data = {}
data['虎粮'] = 0
data['宝剑'] = 0.1
data['荧光棒'] = 0.1
data['血瓶'] = 6.6
data['火锅'] = 66
data['魔法书'] = 99
data['钞票枪'] = 300
data['超级星光阵'] = 300
data['虎牙一号'] = 1000
data['浪漫热气球'] = 5000
data['奖杯'] = 6.6
data['高能预警'] = 88
data['藏宝图'] = 5000
data['礼盒'] = 1
data['星云战机'] = 1000
data['超时空战舰'] = 5000
data['小紫本'] = 1
data['小星星'] = 0.1
data['能量石'] = 1
data['告白气球'] = 520
data['年度星光'] = 0.1
data['虎牙七号'] = 5000
data['火箭登陆'] = 10000

data['超粉卡.'] = 6
data['超火'] = 0.1
data['钻心'] = 6
data['守护之盾'] = 66
data['海洋之心'] = 5000
with open('gift_price.txt', 'w') as outfile:
    json.dump(data, outfile)

with open('gift_price.txt') as json_file:
    data2 = json.load(json_file)