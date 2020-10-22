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
def recoginse_text(image,ocr1):
    #image preprocessing
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)

    ret,binary = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV| cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT,(1,2))  
    morph1 = cv.morphologyEx(binary,cv.MORPH_OPEN,kernel)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 1)) 
    morph2 = cv.morphologyEx(morph1,cv.MORPH_OPEN,kernel)

    text = ocr1.ocr(morph2)
    print(text)
#    text=tess.image_to_string(textImage,lang='chi_sim')
    try:
        text=text[0]
        rem_num = ''.join(text[text.index('余')+1:text.index('汰')-1])
        kill_num = ''.join(text[text.index('汰')+1:])
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        Path("./test_croped.png").rename("./images/%s_rem%s_kill_%s"%(current_time,rem_num,kill_num))

        return "[剩余 : %s "%rem_num + "淘汰 : %s]"%kill_num
    except:
        print ('无淘汰数据')
        return '[无淘汰数据]'

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
        folder = "./test/%s"%today
    else:
        folder = "./%s"%today
    Path(folder).mkdir(parents=True, exist_ok=True)
    if Path(folder+"/stdout_0.txt").is_file():
        flist = sorted(Path(folder).iterdir(), key=os.path.getmtime)
        filename =folder+ '/stdout_' + str(int(flist[-1].name.split('_')[-1].split('.')[0])+1)+'.txt'
        print(filename)
    else:
        filename = folder+ '/stdout_0.txt'

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
    def __init__ (self, room_id='97796', msg=False, debug=True):
        #autoplay doesn't work here.
        profile = webdriver.FirefoxProfile()
        profile.set_preference("media.autoplay.enabled", True)
        self.driver = webdriver.Firefox(firefox_profile=profile)
        self.room_id = room_id
        self.live_count = 0
        self.vip_count = 0
        self.msg = msg
        self.soup = BeautifulSoup()
        self.logger = logger_setup(debug)
        with open('gift_price.txt') as json_file:
            self.gift_prices = json.load(json_file)
        
    def get_numofkill (self,ocr1):
        #mixmize windows and turn off danmu
        try:
            title = self.driver.find_element_by_class_name("player-play-btn").get_attribute("title") 
        except:
            try:
                title = self.driver.find_element_by_class_name("player-pause-btn").get_attribute("title")
            except:
                return  '[无淘汰数据]'   
        if title == '开始观看':
            self.driver.find_element_by_class_name("player-play-big").click()
            element = self.driver.find_element_by_xpath("//div[@class='player-gift-wrap']")
            self.driver.execute_script("arguments[0].style.visibility='hidden'", element)
            self.driver.find_element_by_id("player-danmu-btn").click()
            self.driver.find_element_by_id("player-fullscreen-btn").click()
        self.driver.get_screenshot_as_file('test.png')
        
        img = Image.open('test.png')
        img.crop((155,205,590,270)).save('./test_croped.png')
        img = cv.imread("./test_croped.png")
        text = recoginse_text(img, ocr1)
        return text
    
    def gift_msg (self):
        now = datetime.now()
        today = now.strftime("%Y_%m_%d")
        with open('gift_price.txt') as json_file:
            gift_prices = json.load(json_file)
        self.driver.get('https://www.huya.com/'+self.room_id)
        print("已成功连接房间 ： %s"%self.room_id)
        self.logger.info("已成功连接房间 ： %s"%self.room_id)
        self.login()
        msg_usr=[]
        id_list=[]
        gift_dict=defaultdict(int)
        fout = open("test/%s/msg.txt"%today,'a',buffering=1) 
        while True:
            self.soup = BeautifulSoup(self.driver.page_source,features="lxml")
#        soup.findAll("div", {"class": "msg-normal"})
#            gift_list = self.soup.findAll("div", {"class": "tit-h-send"})
            #document what people usually say when watching livestream
            data_list = self.soup.findAll("li", {"class": re.compile("J_msg")})
                                       
#             for gift in gift_list:
#                 user_name = gift.find_all('span',{'class':'cont-item name J_userMenu'})[0].text
#                 gift_price = self.gift_prices[gift.find_all('img')[0]['alt']] 
#                 gift_count1 = gift.find_all('span',{'class':'cont-item'})[3].text
#                 try:
#                     gift_count2 = gift.find_all('span',{'class':'cont-item send-comb'})[0].text[0:-2]
#                     gift_price = gift_price * int(gift_count1) * int(gift_count2)
#                     gift_dict[user_name] = gift_price
#                 except:
#                     gift_count2 = 1
#                     gift_price = gift_price * int(gift_count1) + gift_dict[user_name]
#                     gift_dict[user_name] = gift_price
#                 print("%s送了%s"%(user_name,gift_price))
# #    gift_dict.update({user_name:gift_price})
#                 if gift_price > 50 and not (user_name in msg_usr):
#                     self.send_msg ('哇哇')
#                     msg_usr.append(user_name)
                    
            #msg = self.soup.findAll("div", {"class": re.compile("msg-nobleSpeak box-noble-level-*|msg-normal")})          
#            print(data_list)
            for i in data_list:
                if not i['data-id'] in id_list:
                    id_list.append(i['data-id'])
            
                    if i.find("div", {"class": "tit-h-send"}):
                        user_name = i.find('span',{'class':'cont-item name J_userMenu'}).text
                        gift_price = self.gift_prices[i.find('img')['alt']] 
                        gift_count1 = i.find_all('span',{'class':'cont-item'})[3].text
                        try:
                            gift_count2 = i.find_all('span',{'class':'cont-item send-comb'})[0].text[0:-2]
                            current_price=0
                        except:
                            gift_count2 = 1
                            current_price = gift_dict[user_name]
                        gift_price = gift_price * int(gift_count1) * int(gift_count2) + current_price
                        gift_dict[user_name] = gift_price
                        print("%s送了%s"%(user_name,gift_price))
                        if gift_price > 50 and not (user_name in msg_usr):
                            self.send_msg ('哇哇')
                            msg_usr.append(user_name)
                            if len(msg_usr) > 5:
                                msg_usr=[]
                                gift_dict=defaultdict(int)
                    elif i.find("div", {"class": re.compile("msg-nobleSpeak box-noble-level-*|msg-normal")}):
                        
                        id_msg = i.find('span',{'class':'msg'}).text
                        
                        if '猪猪' in id_msg:
                            for emoji in i.find('span',{'class':'msg'}).find_all('img'):
                                if emoji['alt'] == "[亲亲]":
                                    self.send_msg ('[亲亲][亲亲]')
                        if re.search('什么.*手机' , id_msg):
                            self.send_msg ('手机: iPhone 11 Pro Max')
                        if re.search('什么.*耳机' , id_msg):
                            self.send_msg ('耳机: 金士顿云雀')
                        print(id_msg)
                        
                        fout.writelines(id_msg)
                        fout.writelines("\n")
                        fout.flush()
        #         return (True, new_gift)
        # return (False,new_gift)
        
    def login (self):
        time.sleep(5)
        #you can log into your account by loading the cookies
        if Path("./cookies.pkl").is_file():
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        else:
            # the codes here work with password login, but 
            # sometimes you have to use huya app to scan the QR code at the first time
            self.driver.find_element_by_id("nav-login").click()
            self.driver.switch_to.frame("UDBSdkLgn_iframe")
            self.driver.find_element_by_class_name("input-login").click()
            self.driver.find_element_by_xpath('//div[@class="udb-input-item"]//input[@placeholder="手机号/虎牙号"]').send_keys("***")
            self.driver.find_element_by_xpath("//input[@placeholder='密码']").send_keys("****")
            self.driver.find_element_by_id("login-btn").click()
            pickle.dump(self.driver.get_cookies() , open("cookies.pkl","wb"))
    def send_msg (self, msg):
        input_text = self.driver.find_element_by_id('pub_msg_input')
        input_text.send_keys(msg)
        time.sleep(1)
        send_btn = self.driver.find_element_by_id('msg_send_bt')
        send_btn.click()

    def run (self):
        self.driver.get('https://www.huya.com/'+self.room_id)
        print("已成功连接房间 ： %s"%self.room_id)
        self.logger.info("已成功连接房间 ： %s"%self.room_id)
        #the alphabet set we need
        ocr1 = CnOcr(cand_alphabet=['0','1','2','3','4','5','6','7','8','9','淘','汰','剩','余'])
        self.login()
        gameinfo = '[无淘汰数据]'
        while True:
            time.sleep(10)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            self.soup = BeautifulSoup(self.driver.page_source,features="lxml")
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
                self.vip_count = self.soup.findAll("span", {"class": "week-rank__btn J_rankTabVip"})[0].text
                self.vip_count = self.vip_count.split('(')[1][:-1]

                gameinfo = self.get_numofkill(ocr1)
                print("[人气值 : %s]"%self.live_count)
                self.logger.info("[人气值 : %s]"%self.live_count+"[贵宾数 : %s]"%self.vip_count+gameinfo)
                print("[贵宾数 : %s]"%self.vip_count)
                print(gameinfo)
 
            except:
                print('直播未开始或房间连接失败')
                time.sleep(60)
                self.driver.refresh()
            
                    
if __name__ == '__main__':
     huya = huya_info(room_id = '97796', msg = False, debug = True)
     #huya.run()
     huya.gift_msg()