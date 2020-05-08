#! /usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
import time

url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=selenium%E6%BB%9A%E5%8A%A8%E7%AA%97%E5%8F%A3'
driver_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

driver = webdriver.Chrome(driver_path)

driver.get(url)

time.sleep(3)

e = driver.find_element_by_class_name('feedback')

e.location_once_scrolled_into_view()

time.sleep(3)
