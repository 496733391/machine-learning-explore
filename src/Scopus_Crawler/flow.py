#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from selenium import webdriver
import pandas as pd
from selenium.webdriver import ChromeOptions

from src.Scopus_Crawler.scopus_config import driver_path
from src.Scopus_Crawler.get_cookies import get_cookies
from src.Scopus_Crawler.authorID_get import get_id
from src.Scopus_Crawler.person_match import match
from src.Scopus_Crawler.data_write import write2sql
from src.config.logConfig import logger_scopus as logger
from src.Scopus_Crawler.data_process import data_process

# 浏览器选项
options = ChromeOptions()
# 添加代理地址和header
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')


def start_driver():
    # 启动浏览器
    driver = webdriver.Chrome(driver_path, options=options)

    return driver


def main_prog(input_data):
    '''

    :param input_data: [{'person_id':1234564, 'name':'liu bo', 'ins':['fudan university', 'xx university', 'xxx university'],
                        'ins_id':[111, 222, 333], 'name_zh':'刘博'}, {...}]
    :return:
    '''
    count = 0
    while count < len(input_data):
        all_aff_df = pd.DataFrame(data=None, columns=None)
        basic_info_df = pd.DataFrame(data=None, columns=None)
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        driver.close()
        try:
            # 开始对每位学者再scopus上进行匹配和信息获取
            for i in range(count, len(input_data)):
                person_id = input_data[i]['person_id']
                author_name = input_data[i]['name']
                author_name_zh = input_data[i]['name_zh']
                author_ins = input_data[i]['ins']
                author_ins_id = input_data[i]['ins_id']
                logger.info('当前进度：软科id：%s, 姓名：%s,%s' % (person_id, author_name_zh, author_name))
                # 机构英文名称全部转为小写
                author_ins = [i.lower() for i in author_ins]
                authorID_list = get_id(person_id, author_name, author_name_zh, author_ins[0])
                # 以机构对应的scopus_id匹配
                aff_df, basic_info = match(cookies, person_id, author_name, author_name_zh, author_ins_id, authorID_list)

                if len(basic_info):
                    all_aff_df = all_aff_df.append(aff_df, ignore_index=True)
                    basic_info_df = basic_info_df.append(basic_info, ignore_index=True)

            # 结束循环
            count = len(input_data)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            logger.info('ERROR:%s' % err)
            logger.info('当前进度：%s / %s' % (i+1, len(input_data)))
            count = i

        # 将已完成的部分进行数据写入
        write2sql([['author_info_new', basic_info_df], ['author_exp', all_aff_df]])


if __name__ == '__main__':
    logger.info('********START********')
    logger.info('*********************')
    # 测试用，从本地excel中读数据
    input_df = pd.read_excel('C:/Users/Administrator/Desktop/test_data/test_data.xlsx')
    input_df.rename(columns={'学者代码': 'person_id',
                             '姓名': 'name',
                             '头衔当选单位': 'rankaff_name',
                             '软科代码': 'rankaff_id'}, inplace=True)
    
    lis = [70, 217, 237, 303, 324, 426, 469, 483, 550, 614, 772, 794, 818, 835, 951, 1001, 1002, 1005, 1013,
           1023, 1024, 1033, 1035, 1043, 1044, 1047, 1055, 1056, 1062, 1069, 1070, 1074, 1075, 1076, 1079, 1080,
           1083, 1085, 1086, 1087, 1089, 1097, 1098, 1106, 1111, 1114, 1126, 1127, 1138, 1146, 1147, 1153, 1155,
           1163, 1168, 1174, 1186, 1192, 1194, 1205, 1208, 1220, 1224, 1228, 1229, 1238, 1248, 1256, 1262, 1273,
           1275, 1276, 1280, 1283, 1287, 1290, 1293, 1295, 1297, 1298, 1304, 1313, 1315, 1318, 1332, 1338, 1360,
           1370, 1396, 1427, 1461, 1470, 1495, 1521, 1536, 1546, 1547, 1549, 1550, 1564, 1572, 1587, 1591,
           1601, 1610, 1613, 1623, 1641, 1644, 1657, 1658, 1661, 1684, 1734, 1735, 1739, 1740, 1741, 1742, 1743,
           1745, 1746, 1748, 1749, 1750, 1754, 1758, 1759, 1821, 1831, 1896, 1897, 1943, 1946,
           1950, 1951, 1952, 1953, 1957, 1959, 1967, 1969, 1976, 1978, 1983, 2008, 2019, 2022, 2056, 2063, 2067,
           2080, 2203, 2254, 2271, 2273, 2274, 2275, 2279, 2280, 2281, 2282, 2284, 2285, 2287, 2288, 2289,
           2291, 2292, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2302, 2304, 2305, 2306, 2310, 2312, 2313, 2315,
           2316, 2321, 2322, 2325, 2346, 2371, 2380, 2403, 2426, 2427, 2428, 2429, 2430, 2431, 2432, 2433, 2434,
           2435, 2436, 2437, 2438, 2458, 2462, 2464, 2465, 2483, 2484, 2489, 2530, 2535, 2541, 2552, 2555, 2566,
           2589, 2595, 2623, 2628, 2630, 2631, 2636, 2642, 2652, 2654, 2663, 2671, 2677, 2683, 2697, 2726, 2727,
           2747, 2774, 2782, 2793, 2806, 2817, 2826, 2848, 2857, 2884, 2889, 2895, 2963, 2995, 3010, 3024, 3086,
           3115, 3134, 3167, 3178, 3201, 3202, 3208, 3217, 3248, 3274, 3324, 3330, 3347, 3378, 3416, 3420, 3486,
           3520, 3523, 3564, 3574, 3748, 3760, 3761, 3763, 3769, 3778, 3783, 3807, 3808, 3809, 3816, 3832, 3841,
           3881, 3897, 3903, 3905, 3907, 3926, 3932, 3939, 3958, 3963, 3964, 3972, 3973, 3974, 3979, 3980, 3983,
           3985, 3998, 4003, 4004, 4005, 4008, 4016, 4018, 4023, 4028, 4033, 4035, 4046, 4047, 4049, 4056, 4060,
           4066, 4069, 4119, 4258, 4264, 4270, 4279, 4280, 4287, 4288, 4289, 4293, 4294, 4295, 4298, 4299, 4300,
           4301, 4302, 4304, 4305, 4317, 4318, 4319, 4320, 4353, 4378, 4431, 4462, 4468]

    input_df = input_df[input_df['person_id'].isin(lis)].reset_index(drop=True)

    input_data = data_process(input_df)

    main_prog(input_data)
    logger.info('*********END*********')
    logger.info('*********************')
