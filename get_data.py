#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 03:39:39 2020

@author: jiechi
"""
from run import *


if __name__ == '__main__':
    end_dt = datetime.strptime(time.strftime("11:0:0"), '%H:%M:%S')
    now = datetime.now()
    a = customTime(now)        
    start_dt = datetime.strptime(time.strftime('%H:%M:%S', a), '%H:%M:%S')
    time.sleep((end_dt - start_dt).total_seconds())
    huya = huya_info(room_id = '97796', msg = False, debug = False,headless=True)
    huya.run()
#     huya.gift_msg()
