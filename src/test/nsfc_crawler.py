#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import base64
from selenium import webdriver
from PIL import Image
from io import BytesIO
import time
import pandas as pd

from src.Scopus_Crawler.scopus_config import headers, driver_path

# p_url = 'https://isisn.nsfc.gov.cn/egrantindex/cpt/ajaxload-tree?locale=zh_CN&key=subject_code_index&cacheable=true&sqlParamVal='
#
# info = requests.get(p_url, headers).json()
# df = pd.DataFrame(data=info)
# df.to_excel('C:/Users/Administrator/Desktop/学科数据0928.xlsx', index=False)

# headers['content-type'] = 'application/x-www-form-urlencoded'
# headers['Referer'] = 'https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list'
# headers['Cookie'] = 'UM_distinctid=1725e06dd0a5dd-00666f02cc0b92-f7d1d38-1fa400-1725e06dd0b1cb; isisn=67313298'

# init_post_data = 'resultDate=prjNo%3A%2Cctitle%3A%2CpsnName%3A%2CorgName%3A%2CsubjectCode%3AC0713.%E7%BB%86%E8%83%9E%' \
#             'E4%BF%A1%E5%8F%B7%E8%BD%AC%E5%AF%BC%2Cf_subjectCode_hideId%3AC0713%2CsubjectCode_hideName%3A%2CkeyWords%3A%2C' \
#             'checkcode%3A{}%2CgrantCode%3A218%2CsubGrantCode%3A%2ChelpGrantCode%3A%2Cyear%3A2019%2Csqdm%3AC0713' \
#             '&checkcode={}'
#
basic_url = 'https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list'
#
# valid_code_url = 'https://isisn.nsfc.gov.cn/egrantindex/validatecode.jpg'
# session = requests.session()
#
# cookie_dict = {'UM_distinctid': '1725e06dd0a5dd-00666f02cc0b92-f7d1d38-1fa400-1725e06dd0b1cb', 'isisn': '67313298'}
# requests.utils.add_dict_to_cookiejar(session.cookies, cookie_dict)
#
# basic_page = session.get(url=basic_url, headers=headers)
# print(session.cookies._cookies)
# valid_code_pic = session.get(url=valid_code_url, headers=headers)
# print(session.cookies._cookies)

# 图片识别
# request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
#
# img = base64.b64encode(valid_code_pic.content)
#
# params = {"image": img}
# access_token = '24.4ca6688ffc63afbda8c00659c3c037bd.2592000.1603508761.282335-22749485'
# request_url = request_url + "?access_token=" + access_token + 'language_type=ENG'
# headers_pic = {'content-type': 'application/x-www-form-urlencoded'}
# response = requests.post(request_url, data=params, headers=headers_pic)
# valid_code = response.json()['words_result'][0]['words'].replace(' ', '')
# print(valid_code)

# temp_url = 'https://isisn.nsfc.gov.cn/egrantindex/funcindex/validate-checkcode'
# temp_post_data = 'checkCode={}'.format(valid_code)
# temp_page = session.post(url=temp_url, data=temp_post_data, headers=headers)
# print(session.cookies._cookies)
#
# post_url = 'https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list'
#
# post_data = init_post_data.format(valid_code, valid_code)
# data_page = session.post(url=post_url, data=post_data, headers=headers)
# print(session.cookies._cookies)

# post_url2 = 'https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list?flag=grid&checkcode='
#
# init_post_data2 = '_search=false&nd=1601197171519&rows=10&page=1&sidx=&sord=desc&searchString=resultDate%5E%3AprjNo' \
#                   '%253A%252Cctitle%253A%252CpsnName%253A%252CorgName%253A%252CsubjectCode%253AC0713.%25E7%25BB%2586' \
#                   '%25E8%2583%259E%25E4%25BF%25A1%25E5%258F%25B7%25E8%25BD%25AC%25E5%25AF%25BC%252Cf_subjectCode_h' \
#                   'ideId%253AC0713%252CsubjectCode_hideName%253A%252CkeyWords%253A%252Ccheckcode%253A{}%252Cgran' \
#                   'tCode%253A218%252CsubGrantCode%253A%252ChelpGrantCode%253A%252Cyear%253A2019%252Csqdm%253AC0713' \
#                   '%5Btear%5Dsort_name1%5E%3ApsnName%5Btear%5Dsort_name2%5E%3AprjNo%5Btear%5Dsort_order%5E%3Adesc'
#
# post_data2 = init_post_data2.format(valid_code)
# data_page2 = session.post(url=post_url2, data=post_data2, headers=headers)
# print(1)

# 浏览器选项
options = webdriver.ChromeOptions()
# 添加代理地址和header
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')

def check_code_ocr(driver):
    img = driver.find_element_by_id('img_checkcode')

    location = img.location
    size = img.size
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']

    driver.save_screenshot('full_snap.png')
    page_snap_obj = Image.open('full_snap.png')

    image_obj = page_snap_obj.crop((left, top, right, bottom))

    output_buffer = BytesIO()
    image_obj.save(output_buffer, format='png')
    image_obj = output_buffer.getvalue()

    # 图片识别
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

    img = base64.b64encode(image_obj)

    params = {"image": img}
    access_token = '24.4ca6688ffc63afbda8c00659c3c037bd.2592000.1603508761.282335-22749485'
    request_url = request_url + "?access_token=" + access_token
    headers_pic = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers_pic)
    valid_code = response.json()['words_result'][0]['words'].replace(' ', '')
    return valid_code


driver = webdriver.Chrome(driver_path, options=options)
driver.get(basic_url)
time.sleep(0.5)
driver.find_element_by_id('f_grantCode').click()
time.sleep(0.5)
driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/table/tbody/tr[1]/td/table/tbody/tr[6]/td[2]/select/option[2]').click()
time.sleep(0.5)
driver.find_element_by_id('f_year').click()
time.sleep(0.5)
driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/table/tbody/tr[1]/td/table/tbody/tr[10]/td[2]/select/option[2]').click()

check_code = check_code_ocr(driver)
time.sleep(0.5)
driver.find_element_by_id('f_checkcode').send_keys(check_code)

time.sleep(0.5)
driver.find_element_by_name('subjectCode').send_keys('A01')
time.sleep(2)
driver.find_element_by_xpath('/html/body/div[6]/ul/li[1]').click()
time.sleep(1)
driver.find_element_by_id('searchBt').click()
print(1)

