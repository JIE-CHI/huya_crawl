#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 05:12:23 2020

@author: jiechi
"""

import time
from selenium import webdriver
from datetime import datetime
from pytz import timezone, utc
import logging
from pathlib import Path
import pickle
from bs4 import BeautifulSoup
from PIL import Image
import mxnet as mx
from cnocr import CnOcr
import cv2 as cv
import os
import json
import re
from collections import defaultdict
import random 
from selenium.webdriver.firefox.options import Options
import sched, time


    

def customTime(*args):
        utc_dt = utc.localize(datetime.utcnow())
        china_tz = timezone('Asia/Shanghai')
        converted = utc_dt.astimezone(china_tz)
        return converted.timetuple()

def logger_setup(debug):
    #setup logger and with china time zone
    
    now = datetime.now()
    today = now.strftime("%Y_%m_%d")
    if debug:
        folder = "./lottery_debug"
    else:
        folder = "./lottery"
    Path(folder).mkdir(parents=True, exist_ok=True)
    if Path(folder+"/msg.%s_0.txt"%today).is_file():
        flist = sorted(Path(folder).iterdir(), key=os.path.getmtime)
        filename =folder+ "/msg.%s_"%today + str(int(flist[-1].name.split('_')[-1].split('.')[0])+1)+'.txt'
        print(filename)
    else:
        filename = folder+ "/msg.%s_0.txt"%today

    logger = logging.getLogger(__name__)  
    if debug:
        logger.disabled = True
    logger.setLevel(logging.INFO)

    # define file handler and set formatter
    file_handler = logging.FileHandler(filename,encoding='utf-8')
    logging.Formatter.converter = customTime
    formatter    = logging.Formatter('%(asctime)s : %(message)s',"%H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger




class huya_info:
    def __init__ (self, room_id='97796', msg=False, debug=True, headless=False):
        #autoplay doesn't work here.
        profile = webdriver.FirefoxProfile()
        options = Options()
        options.headless = headless
        profile.set_preference("media.autoplay.enabled", True)
        self.driver = webdriver.Firefox(options=options,firefox_profile=profile)
        self.driver.maximize_window()
        self.room_id = room_id
        self.live_count = 0
        self.vip_count = 0
        self.msg = msg
        self.soup = BeautifulSoup()
        self.logger = logger_setup(debug)
        with open('gift_price.txt') as json_file:
            self.gift_prices = json.load(json_file)
        
    
    def lottery_log (self, autoreply=True):
        self.driver.get('https://www.huya.com/'+self.room_id)
        print("已成功连接房间 ： %s"%self.room_id)
        self.logger.info("已成功连接房间 ： %s"%self.room_id)
        id_list=[]
        live_close=True

        while (live_close):
            try:
                #the easiest way to check if the live is on
                soup1 = BeautifulSoup(self.driver.page_source,features="lxml")
                print('soup')
                vip_count = soup1.findAll("span", {"class": "room-weeklyRankList-nav-item J_rankTabVip"})[0].text
                print('vip_count')

                live_close=False
            except:
                print('直播未开始或房间连接失败')
                time.sleep(60)
                self.driver.refresh()
        while (not live_close):
            self.soup = BeautifulSoup(self.driver.page_source,features="lxml")
            
                #self.send_msg (msg+emoji*3)
            #document what people usually say when watching livestream
#            data_list = self.soup.findAll("div", {"class": "msg-onTVLottery"})+self.soup.findAll("div", {"class": re.compile("msg-sys")})
            data_list = self.soup.findAll("li", {"class": re.compile("J_msg")})
                                       
            for i in data_list:
                if not i['data-id'] in id_list:
                    id_list.append(i['data-id'])
            
                    if i.find("div", {"class": "msg-onTVLottery"}):
                        user_name = i.find('span',{'class':'name J_userMenu'}).text
                        msg = i.find('span',{'class':'msg'}).text
                        self.logger.info("user: %s; msg: %s"%(user_name,msg))
                        print("user: %s; msg: %s"%(user_name,msg))
                    elif i.find("div", {"class": "msg-sys"}):
                        try:
                            
                            if i.find('span',{'class':'msg-sys-admin'}).text=='上电视公告':
                                msg = i.find('span',{'class':'msg'}).text
                                self.logger.info("winner: %s"%msg)
                                print("winner: %s"%msg)
                        except:
                            pass
                    elif i.find("div", {"class": re.compile("msg-nobleSpeak box-noble-level-*|msg-normal")}):
                        
                        id_msg = i.find('span',{'class':'msg'}).text
                        if (re.search('下播' , id_msg)) and (i.find('span',{'class':'name J_userMenu'}).text in ['【米粉】仿生猪很自由', '池三斗' ]):
                            live_close=True
       
    def login (self):
        time.sleep(2)
        #you can log into your account by loading the cookies
        if Path("./cookies.pkl").is_file():
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            pickle.dump(self.driver.get_cookies() , open("cookies.pkl","wb"))
        else:
            # the codes here work with password login, but 
            # sometimes you have to use huya app to scan the QR code at the first time
            self.driver.find_element_by_id("nav-login").click()
            time.sleep(30)
#            self.driver.switch_to.frame("UDBSdkLgn_iframe")
#            time.sleep(10)
#            self.driver.find_element_by_class_name("input-login").click()
#            self.driver.find_element_by_xpath('//div[@class="udb-input-item"]//input[@placeholder="手机号/虎牙号"]').send_keys("***")
#            self.driver.find_element_by_xpath("//input[@placeholder='密码']").send_keys("***")
            
#            self.driver.find_element_by_id("login-btn").click()
            pickle.dump(self.driver.get_cookies() , open("cookies.pkl","wb"))
    def send_msg (self, msg):
        input_text = self.driver.find_element_by_id('pub_msg_input')
        input_text.send_keys(msg)
#        time.sleep(1)
        send_btn = self.driver.find_element_by_id('msg_send_bt')
        send_btn.click()
        #if send is not allowed, the msg will be cleared
        self.driver.find_element_by_id('pub_msg_input').clear()
        time.sleep(2)
    def send_msg2 (self, msg):
        JS_ADD_TEXT_TO_INPUT = """
        var elm = arguments[0], txt = arguments[1];
        elm.value += txt;
        elm.dispatchEvent(new Event('change'));
        """
        #punch emoji
        text = u'\ud83d\udc4a'
        
        input_text = self.driver.find_element_by_id('pub_msg_input')
        self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, input_text, text)
        input_text.send_keys('[猪头]')
#        time.sleep(1)
        self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, input_text, text)
        send_btn = self.driver.find_element_by_id('msg_send_bt')
        send_btn.click()
        #if send is not allowed, the msg will be cleared
        self.driver.find_element_by_id('pub_msg_input').clear()
    def run (self):
        self.driver.get('https://www.huya.com/'+self.room_id)
        print("已成功连接房间 ： %s"%self.room_id)
        self.logger.info("已成功连接房间 ： %s"%self.room_id)
        #the alphabet set we need
#        ocr1 = CnOcr(cand_alphabet=['0','1','2','3','4','5','6','7','8','9','淘','汰','剩','余'])
#        self.login()
#        gameinfo = '[无淘汰数据]'
        live_close=False
        id_list=[]
        while (not live_close):
            time.sleep(10)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            self.soup = BeautifulSoup(self.driver.page_source,features="lxml")
            
            data_list = self.soup.findAll("li", {"class": re.compile("J_msg")})
                                       
            for i in data_list:
                if not i['data-id'] in id_list:
                    id_list.append(i['data-id'])
                    if i.find("div", {"class": re.compile("msg-nobleSpeak box-noble-level-*|msg-normal")}):
                        
                        id_msg = i.find('span',{'class':'msg'}).text
                        
                        if (re.search('下播' , id_msg)) and (i.find('span',{'class':'name J_userMenu'}).text in ['【米粉】仿生猪很自由', '池三斗' ]):
                            live_close=True
            if self.msg and self.gift_info()[0]:
                try:
                    self.send_msg()
                except:
                    try:
                        self.login()
                    except:
                        print('无法发送弹幕，请检查是否登陆成功')
            try:

                self.live_count = self.soup.findAll("em", {"id": "live-count"})[0].text
                self.vip_count = self.soup.findAll("span", {"class": "room-weeklyRankList-nav-item J_rankTabVip"})[0].text
                self.vip_count = self.vip_count.split('(')[1][:-1]

#                gameinfo = self.get_numofkill(ocr1)
                print("[人气值 : %s]"%self.live_count)
                self.logger.info("[人气值 : %s]"%self.live_count+"[贵宾数 : %s]"%self.vip_count)
#                self.logger.info("[人气值 : %s]"%self.live_count+"[贵宾数 : %s]"%self.vip_count+gameinfo)
                print("[贵宾数 : %s]"%self.vip_count)
#                print(gameinfo)
 
            except:
                print('直播未开始或房间连接失败')
                time.sleep(60)
                self.driver.refresh()
            
                    
if __name__ == '__main__':
    end_dt = datetime.strptime(time.strftime("11:0:0"), '%H:%M:%S')
    now = datetime.now()
    a = customTime(now)        
    start_dt = datetime.strptime(time.strftime('%H:%M:%S', a), '%H:%M:%S')
    if (end_dt - start_dt).total_seconds() > 0:
        time.sleep((end_dt - start_dt).total_seconds())
    huya = huya_info(room_id = '97796', msg = False, debug = False)
      #huya.run()
    huya.lottery_log()
    huya.driver.close()
