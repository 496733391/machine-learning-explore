# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 15:47:42 2019

@author: ruanke
"""

from selenium import webdriver
import time, os, json, shutil
from datetime import datetime

from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path

url = 'https://esi.clarivate.com/IndicatorsAction.action#'

def InitDriver():
    #初始化游览器选项：
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    
    #打开Chrome游览器，并窗口最大化：
    driver = webdriver.Chrome(driver_path, chrome_options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    #打开网址，并给其3秒加载时间：
    driver.get(url)
    # time.sleep(3)
    return driver


def Login(driver):
    driver.find_element_by_xpath('//*[@id="username"]').send_keys('503351081@qq.com')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys('ranking2019@')
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div/div[1]/div[3]/div[1]/div/div/div/form/button').click()
    time.sleep(5)
    print('登录成功！\n')

def get_dic(driver):
    li = driver.find_elements(By.XPATH,'//*[@id="researchFieldsInnerPopUp"]/div/div/label')
    li_t = [x.text for x in li]
    for i in range(22):
        li_t.remove('')
    li = li_t
    for i in range(22):
        li[i] = li[i].replace(' ','%20')
        li[i] = li[i].replace('&','%26')
    dic ={}
    for i in range(22):
        dic.setdefault(i,li[i])
    result = json.dumps(dic, indent = 4)
    return result


def Download(driver):
    result = '''{
    "0": "Agricultural%20Sciences",
    "1": "Biology%20%26%20Biochemistry",
    "2": "Chemistry",
    "3": "Clinical%20Medicine",
    "4": "Computer%20Science",
    "5": "Economics%20%26%20Business",
    "6": "Engineering",
    "7": "Environment/Ecology",
    "8": "Geosciences",
    "9": "Immunology",
    "10": "Materials%20Science",
    "11": "Mathematics",
    "12": "Microbiology",
    "13": "Molecular%20Biology%20%26%20Genetics",
    "14": "Multidisciplinary",
    "15": "Neuroscience%20%26%20Behavior",
    "16": "Pharmacology%20%26%20Toxicology",
    "17": "Physics",
    "18": "Plant%20%26%20Animal%20Science",
    "19": "Psychiatry/Psychology",
    "20": "Social%20Sciences,%20General",
    "21": "Space%20Science"
}'''
    dic = json.loads(result)
    
    #可能需要替换网址
    u = 'https://esi.clarivate.com/IndicatorsExport.action?exportFile&_dc=1368621151464&groupBy=Institutions&start=0&limit=2500&filterBy=ResearchFields&filterValue={}&show=Highly%20Cited&sort=%5B%7B%22property%22:%22cites%22,%22direction%22:%22DESC%22%7D%5D&colFilterVal=&exportType=indicators&colNames=RowSeq,,Institutions,Countries/Regions,Web%20of%20Science%20Documents,Cites,Cites/Paper,Highly%20Cited%20Papers&fileType=Excel&f=IndicatorsExport.xls'
    
    print('开始下载！')
    for st in list(dic.values())[:]:
        url = u.format(st.upper())
        driver.get(url)
        time.sleep(5)
    print('下载完成！')
    return

def Cd():
    Dl = os.path.join(os.getcwd(),'Downloads')
    x = datetime.now()
    st = '{}-{}-{}-{}-{}-{}'.format(x.year,x.month,x.day,x.hour,x.minute,x.second)
    if not os.path.exists(os.path.join(Dl,st)):
        os.mkdir(os.path.join(Dl,st))
    li = os.listdir(Dl)
    for item in li:
        if item[-5:] == '.xlsx':
            shutil.move(os.path.join(Dl,item),os.path.join(Dl,st))
    print('\n文件移动成功！\nBingo!!!')
    return
    
if __name__ == '__main__':
    driver = InitDriver()
    # Login(driver)
    
    Download(driver)
    Cd()
    
    driver.quit()


