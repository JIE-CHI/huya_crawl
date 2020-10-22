#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 03:39:39 2020

@author: jiechi
"""
from run import *


if __name__ == '__main__':
     huya = huya_info(room_id = '97796', msg = False, debug = False)
     huya.run()
#     huya.gift_msg()