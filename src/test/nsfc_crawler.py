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
from src.Scopus_Crawler.data_write import write2sql

basic_url = 'https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list'

# 浏览器选项
options = webdriver.ChromeOptions()
# 添加代理地址和header
options.add_argument('--proxy-server=202.120.43.93:8059')
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
    response = requests.post(request_url, data=params, headers=headers_pic).json()
    if response['words_result']:
        valid_code = response['words_result'][0]['words'].replace(' ', '')
    else:
        valid_code = '111'
    print(response)
    return valid_code


def get_data(driver):
    # 总页数
    page_num = driver.find_element_by_id('sp_1_TopBarMnt').text
    if page_num == '0':
        return []
    if not page_num:
        return []
    # 获取数据
    table_body = driver.find_element_by_xpath('/html/body/div[4]/div[5]/div[2]/div[3]/div[2]/div/table/tbody')
    # 去除列名
    ranks = table_body.find_elements_by_tag_name('tr')[1:]
    # 提取text
    elements = [rank.find_elements_by_tag_name('td') for rank in ranks]
    data_info = [[k.text for k in element] for element in elements]
    result_list = data_info[:]
    for page in range(int(page_num)-1):
        while data_info[0][0] != str(page*10+11):
            # 识别验证码
            check_code = check_code_ocr(driver)
            # 填入验证码
            driver.find_element_by_id('checkCode').clear()
            driver.find_element_by_id('checkCode').send_keys(check_code)
            time.sleep(0.5)
            # 查询
            driver.find_element_by_id('next_t_TopBarMnt').click()
            time.sleep(1)
            # 获取数据
            table_body = driver.find_element_by_xpath('/html/body/div[4]/div[5]/div[2]/div[3]/div[2]/div/table/tbody')
            # 去除列名
            ranks = table_body.find_elements_by_tag_name('tr')[1:]
            # 提取text
            elements = [rank.find_elements_by_tag_name('td') for rank in ranks]
            data_info = [[k.text for k in element] for element in elements]

        result_list.extend(data_info)

    return result_list


def main_prog(driver, subject_code, type_code):
    driver.get(basic_url)
    time.sleep(0.5)
    # 选择资助类别
    driver.find_element_by_id('f_grantCode').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/table/tbody/tr[1]/td/table/tbody/tr[6]/td[2]/select/option[%s]' % type_code).click()
    time.sleep(0.5)
    # 选择年份
    # driver.find_element_by_id('f_year').click()
    # time.sleep(0.5)
    # driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/table/tbody/tr[1]/td/table/tbody/tr[10]/td[2]/select/option[1]').click()
    # 选择申请代码
    driver.find_element_by_name('subjectCode').send_keys(subject_code)
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[6]/ul/li[1]').click()
    time.sleep(0.5)
    # 输入验证码，识别错误时重新输入
    while '递减' not in driver.page_source:
        # 识别验证码
        check_code = check_code_ocr(driver)
        # 填入验证码
        driver.find_element_by_id('f_checkcode').clear()
        driver.find_element_by_id('f_checkcode').send_keys(check_code)
        time.sleep(0.5)
        # 查询
        driver.find_element_by_id('searchBt').click()
        time.sleep(0.5)

    result_list = get_data(driver)
    if result_list:
        result_df = pd.DataFrame(data=result_list, columns=['id', '项目批准号', '申请代码', '项目名称', '项目负责人', '依托单位', '批准金额', '项目起止年月'])
        write2sql([['nsfc_data', result_df]])


if __name__ == '__main__':
    type_dict = {2: '面上项目',
                 3: '重点项目',
                 4: '重大项目',
                 5: '重大研究计划',
                 6: '国家接触青年科学基金',
                 7: '创新研究群体项目',
                 8: '国际(地区)合作与交流项目',
                 9: '专项基金项目',
                 10: '联合基金项目',
                 11: '青年科学基金项目',
                 12: '地区科学基金项目',
                 13: '海外及港澳学者合作研究基金',
                 14: '国家基础科学人才培养基金',
                 15: '国家重大科研仪器设备研制专项',
                 16: '国家重大科研仪器研制项目',
                 17: '优秀青年科学基金项目',
                 18: '应急管理项目',
                 19: '科学中心项目',
                 20: '专项项目'}
    with open('C:/Users/Administrator/Desktop/subject_code.txt', 'r') as fl:
        subject_code_list = fl.read().split('\n')
    # 启动浏览器
    driver = webdriver.Chrome(driver_path, options=options)
    for subject_code in subject_code_list:
        for type_code in range(2, 21):
            main_prog(driver, subject_code, type_code)
    driver.close()

