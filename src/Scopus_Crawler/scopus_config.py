#! /usr/bin/python
# -*- coding: utf-8 -*-

import json

# 数据库信息
host = 'localhost'
port = 3306
database = 'local'
username = 'root'
password = 'admin'

# chrome浏览器driver路径
driver_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

# 搜索页面地址
# search_url = 'https://www.scopus.com/results/authorNamesList.uri?origin=searchauthorlookup&src=al&edit=&poppUp=&' \
#               'basicTab=&affiliationTab=&advancedTab=&' \
#               'st1={}&' \
#               'st2={}&' \
#               'institute={}' \
#               '&orcidId=&authSubject=LFSC&_authSub' \
#               'ject=on&authSubject=HLSC&_authSubject=on&authSubject=PHSC&_authSubject=on&authSubject=SOSC&_authSubj' \
#               'ect=on&s=AUTHLASTNAME%28liu%29+AND+AUTHFIRST%28bo%29&sdt=al&sot=al&searchId=42a0860e2008958faf4e6c64' \
#               '4b496275&exactSearch=on&sid=42a0860e2008958faf4e6c644b496275'

search_url = 'https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al' \
             '&st1={}' \
             '&st2={}' \
             '&orcidId=&affilName={}' \
             '&sot=anl&sdt=anl&sl=64&resultsPerPage=200&offset=1&jtp=false&currentPage=1&exactAuthorSearch=true'

# 代理地址
proxies = {
            "http": "http://202.120.43.93:8059"
}

# cookies
# with open('cookies.json', 'r') as js:
#     cookie = json.load(js)

# headers
headers = {
            # 'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/81.0.4044.138 Safari/537.36'
}

# 学者机构信息地址
ins_url = 'https://www.scopus.com/author/affilHistory.uri?auId=%s'

# 学者详细页面地址
# data_url = 'https://www.scopus.com/authid/detail.uri?authorId=%s'
data_url = 'https://www.scopus.com/author/highchart.uri?authorId=%s'

# 复姓清单
compound_surname = ['欧阳', '太史', '端木', '上官', '司马', '东方', '独孤', '南宫', '万俟', '闻人', '夏侯',
                    '诸葛', '尉迟', '公羊', '赫连', '澹台', '皇甫', '宗政', '濮阳', '公冶', '太叔', '申屠',
                    '公孙', '慕容', '仲孙', '钟离', '长孙', '宇文', '司徒', '鲜于', '司空', '闾丘', '子车',
                    '亓官', '司寇', '巫马', '公西', '颛孙', '壤驷', '公良', '漆雕', '乐正', '宰父', '谷梁',
                    '拓跋', '夹谷', '轩辕', '令狐', '段干', '百里', '呼延', '东郭', '南门', '羊舌', '微生',
                    '公户', '公玉', '公仪', '梁丘', '公仲', '公上', '公门', '公山', '公坚', '左丘', '公伯',
                    '西门', '公祖', '第五', '公乘', '贯丘', '公皙', '南荣', '东里', '东宫', '仲长', '子书',
                    '子桑', '即墨', '达奚', '褚师', '吴铭']

# 多音字姓氏
polyphony_surname = {'曾': 'Zeng', '单': 'Shan', '呙': 'Guo', '吕': 'Lü', '柏': 'Bai', '查': 'Zha',
                     '仇': 'Qiu', '都': 'Du', '郝': 'Hao', '解': 'Xie', '乐': 'Le', '缪': 'Miao',
                     '覃': 'Qin', '翟': 'Zhai'}

doc_num_limit = 10
aff_limit_high = 25
aff_limit_low = 2
