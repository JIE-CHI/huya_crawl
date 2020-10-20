#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 05:12:23 2020

@author: jiechi
"""

import time
from selenium import webdriver
from lxml import etree
from datetime import datetime, timedelta
from pytz import timezone, utc
import logging
from pathlib import Path

def customTime(*args):
        utc_dt = utc.localize(datetime.utcnow())
        my_tz = timezone("Asia/Shanghai")
        converted = utc_dt.astimezone(my_tz)
        return converted.timetuple()

#setup logger and with china time zone
china_tz = timezone('Asia/Shanghai')
now = datetime.now()
today = now.strftime("%Y_%m_%d")
folder = "./%s"%today
#china_time = now + timedelta(hours=int((china_tz.utcoffset(now)).total_seconds()/3600))


Path(folder).mkdir(parents=True, exist_ok=True)
if Path(folder+"/stdout_0.txt").is_file():
    flist = [p.name for p in Path(folder).iterdir() if p.is_file()]
    filename =folder+ '/stdout_' + str( int(flist[-1].split('_')[1].split('.')[0])+1)+'.txt'
    print(filename)
else:
    filename = folder+ '/stdout_0.txt'

logger = logging.getLogger(__name__)  
logger.setLevel(logging.INFO)

# define file handler and set formatter
file_handler = logging.FileHandler(filename)
logging.Formatter.converter = customTime
#formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
formatter    = logging.Formatter('%(asctime)s : %(message)s',"%H:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)




class huya_info:
    def __init__ (self, room_id='97796', msg=False):
        self.driver = webdriver.Firefox()
        self.room_id = room_id
        self.live_count = 0
        self.vip_count = 0
        self.msg = msg
    
    def send_msg (self):
        input_text = self.driver.find_element_by_id('pub_msg_input')
        input_text.send_keys('test')
        time.sleep(3)
        send_btn = self.driver.find_element_by_id('msg_send_bt')
        send_btn.click()
       #  print(a)
       #  a.click()
       # # b=self.driver.find_element_by_id("Click/QuickLogin/AccountLogin")
       #  # print(b)
       #  # b.click()
       #  self.driver.switch_to_frame("UDBSdkLgn_iframe")
       #  self.driver.find_element_by_xpath('//div[@class="udb-input-item"]//input[@placeholder="手机号/虎牙号"]').send_keys("dd")
       #  self.driver.find_element_by_xpath("//input[@placeholder='密码']").send_keys("dddd")
       #  self.driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[2]/div/div/div/div/div[3]/a").click()
    def run (self):
        self.driver.get('https://www.huya.com/'+self.room_id)
        print("已成功连接房间 ： %s"%self.room_id)
        logger.info("已成功连接房间 ： %s"%self.room_id)
        while True:
            time.sleep(10)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            page_etree = etree.HTML(self.driver.page_source)
            if self.msg:
                try:
                    self.send_msg()
                except:
                    print('无法发送弹幕，请检查是否登陆成功')
            try:
                self.live_count = page_etree.xpath('//em[@id="live-count"]/text()')[0]
                self.vip_count = page_etree.xpath('//span[@class="week-rank__btn J_rankTabVip"]/text()')[0]
                self.vip_count = self.vip_count.split('(')[1][:-1]
                print("[人气值 : %s]"%self.live_count)
                logger.info("[人气值 : %s]"%self.live_count+"[贵宾数 : %s]"%self.vip_count)
                print("[贵宾数 : %s]"%self.vip_count)
 #               logger.info("[贵宾数 : %s]"%self.vip_count)
            except:
                print('直播未开始或房间连接失败')
                time.sleep(600)
                    
if __name__ == '__main__':
     huya = huya_info(room_id = '97796', msg = False)
     huya.run()