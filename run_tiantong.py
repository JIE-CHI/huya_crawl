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
import os
import json
import re
from collections import defaultdict
import random 
from selenium.webdriver.firefox.options import Options


    
    


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
    def __init__ (self, room_id='97796', msg=False, debug=True, headless=False):
        #autoplay doesn't work here.
        options = Options()
        options.headless = headless
        self.driver = webdriver.Firefox(options=options)
        self.room_id = room_id
        self.live_count = 0
        self.vip_count = 0
        self.msg = msg
        self.soup = BeautifulSoup()
#        self.logger = logger_setup(debug)
        with open('gift_price.txt') as json_file:
            self.gift_prices = json.load(json_file)
        
    
    def gift_msg (self, autoreply=True):
        now = datetime.now()
        today = now.strftime("%Y_%m_%d")
        self.driver.get('https://www.huya.com/'+self.room_id)
        print("已成功连接房间 ： %s"%self.room_id)
        # self.logger.info("已成功连接房间 ： %s"%self.room_id)
        self.login()
        #
        msg_usr=['【米粉】仿生猪猪']
        id_list=[]
        gift_dict=defaultdict(int)
        msg_folder = "./msgs/%s"%today
        Path(msg_folder).mkdir(parents=True, exist_ok=True)
        fout = open("msgs/%s_msg.txt"%today,'a',buffering=1) 
        # count_66 = [0,now ]
        # count_haha = [0,now ] 
        # count_pei = [0,now ] 
        # linmindu = now

        live_close=True
        while (live_close):
            try:
                #the easiest way to check if the live is on
                soup1 = BeautifulSoup(self.driver.page_source,features="lxml")
                vip_count = soup1.findAll("span", {"class": "week-rank__btn J_rankTabVip"})[0].text
                vip_count = vip_count.split('(')[1][:-1]
                live_close=False
            except:
                print('直播未开始或房间连接失败')
                time.sleep(60)
                self.driver.refresh()
#        rose_msg = now
        while (not live_close):
            now = datetime.now()
            tag = now.strftime("%H:%M:%S")
            self.soup = BeautifulSoup(self.driver.page_source,features="lxml")
            
            # if  (now - rose_msg).total_seconds() > 60*5:
            #     rose_msg = now
            #     self.send_msg ('10个荧光棒卡牌子～7级进群 跟米粉一起不定期水友赛[心动]')
            #document what people usually say when watching livestream
            data_list = self.soup.findAll("li", {"class": re.compile("J_msg")})
                                       
            for i in data_list:
                ci = random.choice([2,3,4])
                if not i['data-id'] in id_list:
                    id_list.append(i['data-id'])
            
                    if i.find("div", {"class": "tit-h-send"}):
                        user_name = i.find('span',{'class':'cont-item name J_userMenu'}).text
                        if i.find('img')['alt'] in self.gift_prices:
                            gift_price = self.gift_prices[i.find('img')['alt']] 
                        else:
                            gift_price = 0.1
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
                            try:
                                self.send_msg ('哇'*ci)
                                msg_usr.append(user_name)
                            except:
                                pass
                            if len(msg_usr) > 6:
                                msg_usr=['【米粉】仿生猪猪']
                                gift_dict=defaultdict(int)
                    elif  i.find("div", {"class": re.compile("msg-noble noble-recharge noble-recharge-level")}):
                        try:
                            self.send_msg ('哇'*ci)
                        except:
                                pass
                    elif i.find("div", {"class": re.compile("msg-nobleSpeak box-noble-level-*|msg-normal")}):
                        
                        id_msg = i.find('span',{'class':'msg'}).text
                        
#                         if re.search('什么.*手机(?!壳)' , id_msg) or re.search('啥.*手机(?!壳)' , id_msg):
#                             try:
#                                 self.send_msg ('主播手机: iPhone 11 Pro Max')
#                             except:
#                                 pass
                        
#                         if re.search('什么.*耳机' , id_msg) or re.search('啥.*耳机' , id_msg):
#                             try:
#                                 self.send_msg ('主播耳机: 金士顿云雀')
#                             except:
#                                 pass
#                         if (re.search('灵敏度' , id_msg) or re.search('键位设置' , id_msg)) and (not i.find('span',{'class':'name J_userMenu'}).text == '【米粉】仿生猪猪') and (datetime.now() - linmindu).total_seconds() > 10:
#                             try:
# #                                self.send_msg ('灵敏度键位设置搜索新浪微博：虎牙炒米粉，置顶就有')
#                                 self.send_msg ('灵敏度键位设置搜索: 虎牙炒米粉')
#                                 self.send_msg ('在wb置顶')
#                                 linmindu = datetime.now()
#                             except:
#                                 pass
#                         if (re.search('怎.进群' , id_msg) or re.search('如何进群' , id_msg)) and (datetime.now() - linmindu).total_seconds() > 10:
#                             try:
#                                 self.send_msg ('加主播公告微信')
#                                 self.send_msg ('MFen521')
#                                 self.send_msg ('进粉丝群')
#                                 linmindu = datetime.now()
#                             except:
#                                 pass
                               
#                         elif re.search('666' , id_msg) and not i.find('span',{'class':'name J_userMenu'}).text == '【米粉】店小二':
#                             count_66[0] += 1
#                             if count_66[0] > 7 and (datetime.now() - count_66[1]).total_seconds() > 20 :
#                                 try:
#                                     self.send_msg ('666[赞][赞][赞]')
#                                     count_66[0]=0
#                                     count_66[1]=datetime.now()
#                                 except:
#                                     pass
                            
#                         elif re.search('哈哈哈' , id_msg):
#                             count_haha[0] += 1
#                             if count_haha[0] > 7 and  (datetime.now() - count_haha[1]).total_seconds() > 20:
#                                 try:
#                                     self.send_msg ('哈哈'*ci)
#                                     count_haha[0]=0
#                                     count_haha[1]=datetime.now()
#                                 except:
#                                     pass
#                         elif re.search('呸*呸*呸' , id_msg):
#                             count_pei[0] += 1
#                             if count_pei[0] > 5 and  (datetime.now() - count_pei[1]).total_seconds() > 20:
#                                 try:
#                                     self.send_msg ('呸呸'*ci)
#                                     count_pei[0]=0
#                                     count_pei[1]=datetime.now()
#                                 except:
#                                     pass
                        if re.search('下播' , id_msg) and (i.find('span',{'class':'name J_userMenu'}).text in ['【米粉】甜筒很机智','【米粉】欧筒' ]):
                            live_close=True
                        print("%s - %s : %s" %(tag,i.find('span',{'class':'name J_userMenu'}).text,id_msg))
                        
                        fout.writelines("%s - %s : %s" %(tag,i.find('span',{'class':'name J_userMenu'}).text,id_msg))
                        fout.writelines("\n")
                        fout.flush()

    def login (self):
        time.sleep(2)
        #you can log into your account by loading the cookies
        if Path("./cookies_dq.pkl").is_file():
            cookies = pickle.load(open("cookies_dq.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        else:
            # the codes here work with password login, but 
            # sometimes you have to use huya app to scan the QR code at the first time
            self.driver.find_element_by_id("nav-login").click()
            time.sleep(60)
            # self.driver.switch_to.frame("UDBSdkLgn_iframe")
            # time.sleep(10)
            # self.driver.find_element_by_class_name("input-login").click()
            # self.driver.find_element_by_xpath('//div[@class="udb-input-item"]//input[@placeholder="手机号/虎牙号"]').send_keys("***")
            # self.driver.find_element_by_xpath("//input[@placeholder='密码']").send_keys("***")
            
#            self.driver.find_element_by_id("login-btn").click()
            pickle.dump(self.driver.get_cookies() , open("cookies_dq.pkl","wb"))
    def send_msg (self, msg):
        input_text = self.driver.find_element_by_id('pub_msg_input')
        input_text.send_keys(msg)
#        time.sleep(1)
        send_btn = self.driver.find_element_by_id('msg_send_bt')
        send_btn.click()
        #if send_btn is not allowed, the msg will be cleared
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
#     def run (self):
#         self.driver.get('https://www.huya.com/'+self.room_id)
#         print("已成功连接房间 ： %s"%self.room_id)
#         self.logger.info("已成功连接房间 ： %s"%self.room_id)
#         #the alphabet set we need
# #        ocr1 = CnOcr(cand_alphabet=['0','1','2','3','4','5','6','7','8','9','淘','汰','剩','余'])
# #        self.login()
# #        gameinfo = '[无淘汰数据]'
#         live_close=False
#         id_list=[]
#         while (not live_close):
#             time.sleep(10)
#             now = datetime.now()
#             current_time = now.strftime("%H:%M:%S")
#             print("Current Time =", current_time)
#             self.soup = BeautifulSoup(self.driver.page_source,features="lxml")
            
#             data_list = self.soup.findAll("li", {"class": re.compile("J_msg")})
                                       
#             for i in data_list:
#                 if not i['data-id'] in id_list:
#                     id_list.append(i['data-id'])
#                     if i.find("div", {"class": re.compile("msg-nobleSpeak box-noble-level-*|msg-normal")}):
                        
#                         id_msg = i.find('span',{'class':'msg'}).text
                        
#                         if re.search('下播' , id_msg) and (i.find('span',{'class':'name J_userMenu'}).text in ['【米粉】仿生猪猪', '池三斗' ]):
#                             live_close=True
#             if self.msg and self.gift_info()[0]:
#                 try:
#                     self.send_msg()
#                 except:
#                     try:
#                         self.login()
#                     except:
#                         print('无法发送弹幕，请检查是否登陆成功')
#             try:

#                 self.live_count = self.soup.findAll("em", {"id": "live-count"})[0].text
#                 self.vip_count = self.soup.findAll("span", {"class": "week-rank__btn J_rankTabVip"})[0].text
#                 self.vip_count = self.vip_count.split('(')[1][:-1]

# #                gameinfo = self.get_numofkill(ocr1)
#                 print("[人气值 : %s]"%self.live_count)
#                 self.logger.info("[人气值 : %s]"%self.live_count+"[贵宾数 : %s]"%self.vip_count)
# #                self.logger.info("[人气值 : %s]"%self.live_count+"[贵宾数 : %s]"%self.vip_count+gameinfo)
#                 print("[贵宾数 : %s]"%self.vip_count)
# #                print(gameinfo)
 
#             except:
#                 print('直播未开始或房间连接失败')
#                 time.sleep(60)
#                 self.driver.refresh()
            
                    
if __name__ == '__main__':
    end_dt = datetime.strptime(time.strftime("11:0:0"), '%H:%M:%S')
    now = datetime.now()
    a = customTime(now)        
    start_dt = datetime.strptime(time.strftime('%H:%M:%S', a), '%H:%M:%S')
    if (end_dt - start_dt).total_seconds() > 0:
        time.sleep((end_dt - start_dt).total_seconds())
    huya = huya_info(room_id = '97796', msg = False, debug = True)
      #huya.run()
    huya.gift_msg()
    huya.driver.close()