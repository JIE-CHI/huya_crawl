#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 05:06:20 2020

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
import re
from PIL import Image
import mxnet as mx
from cnocr import CnOcr
import cv2 as cv
import pickle


def recoginse_text(image,ocr1):
    #image preprocessing
    cv.imshow('test1',image)
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)

    ret,binary = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV| cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT,(1,2))  #
    morph1 = cv.morphologyEx(binary,cv.MORPH_OPEN,kernel)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 1)) 
    morph2 = cv.morphologyEx(morph1,cv.MORPH_OPEN,kernel)
    cv.imshow('test2',morph2)
    text = ocr1.ocr(morph2)[0]
    print(text)
#    text=tess.image_to_string(textImage,lang='chi_sim')
    try:
        rem_num = text[text.index('余')+1:text.index('汰')-1]
        kill_num = text[text.index('汰')+1:]
        return "[剩余 : %s "%rem_num + "淘汰 : %s]"%kill_num
    except:
        print ('无淘汰数据')
        return '[无淘汰数据]'
# driver = webdriver.Firefox()
# driver.get('https://www.huya.com/'+'97796')
#ocr1 = CnOcr(cand_alphabet=['0','1','2','3','4','5','6','7','8','9','淘','汰','剩','余'])
try:
    title = driver.find_element_by_class_name("player-play-btn").get_attribute("title") 
except:
    title = driver.find_element_by_class_name("player-pause-btn").get_attribute("title") 
if title == '开始观看':
    driver.find_element_by_class_name("player-play-big").click()
    element = driver.find_element_by_xpath("//div[@class='player-gift-wrap']")
    driver.execute_script("arguments[0].style.visibility='hidden'", element)
    driver.find_element_by_id("player-danmu-btn").click()
    driver.find_element_by_id("player-fullscreen-btn").click()
driver.get_screenshot_as_file('test.png')
        
img = Image.open('test.png')
img.show()
img.crop((155,205,590,270)).save('./test_croped.png')
img = cv.imread("./test_croped.png")
text = recoginse_text(img, ocr1)