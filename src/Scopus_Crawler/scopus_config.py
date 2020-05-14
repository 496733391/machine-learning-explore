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
search_url = 'https://www.scopus.com/results/authorNamesList.uri?origin=searchauthorlookup&src=al&edit=&poppUp=&' \
              'basicTab=&affiliationTab=&advancedTab=&' \
              'st1={}&' \
              'st2={}&' \
              'institute={}' \
              '&orcidId=&authSubject=LFSC&_authSub' \
              'ject=on&authSubject=HLSC&_authSubject=on&authSubject=PHSC&_authSubject=on&authSubject=SOSC&_authSubj' \
              'ect=on&s=AUTHLASTNAME%28liu%29+AND+AUTHFIRST%28bo%29&sdt=al&sot=al&searchId=42a0860e2008958faf4e6c64' \
              '4b496275&exactSearch=on&sid=42a0860e2008958faf4e6c644b496275'

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
data_url = 'https://www.scopus.com/authid/detail.uri?authorId=%s'

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
polyphony_surname = {'曾': 'Zeng'}

# selenium用cookies
cookies_str = 'scopus.machineID=C95FAA82D76902CFBA9ADB44D5C59CF2.wsnAw8kcdt7IPYLO0V48gA; optimizelyEndUserId=o' \
              'eu1588830449793r0.7402451939845718; optimizelyBuckets=%7B%7D; xmlHttpRequest=true; optimizelyS' \
              'egments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22no' \
              'ne%22%2C%22278903113%22%3A%22referral%22%7D; __cfruid=ccee03229d9a9aa5a08d9d8893d9634dd8dd7b89-' \
              '1589419179; check=true; javaScript=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; screenInf' \
              'o="1080:1920"; __cfduid=d2bc1953f026de4ee3abec5f6eb4cc0731589448214; SCSessionID=38B0E0A5EFC9E1' \
              'FCDD83B87EA240F115.wsnAw8kcdt7IPYLO0V48gA; scopusSessionUUID=a501b7a5-7cea-4a0d-9; AWSELB=CB931' \
              '7D502BF07938DE10C841E762B7A33C19AADB17A59DD6BA0784DD207E0A02D026B49B728C51DE21F0721BEC11F8AF279A' \
              '07842BAFDF2ADE925350150D7900CAD0CA8A60A1E3E7F2A0213D204EDAE70096BF096; optimizelyPendingLogEvents' \
              '=%5B%5D; mbox=PC#0d2fc3c7b0294bd788e2024d386337d6.22_0#1652693940|session#cc487aa1eb60483fa4032e3' \
              '907ca8761#1589450999; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=1075005958%7CMCIDTS%7C18396%7CMCMI' \
              'D%7C23612113200045070330531324322910847678%7CMCAAMLH-1590053940%7C11%7CMCAAMB-1590053940%7CRKhpRz' \
              '8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589456340s%7CNONE%7CMCAID%7CNONE%7CMCCI' \
              'DH%7C1130218189%7CvVersion%7C4.4.1; s_pers=%20c19%3Dsc%253Asearch%253Aauthor%2520results%7C1589450' \
              '940194%3B%20v68%3D1589449138951%7C1589450940216%3B%20v8%3D1589449153446%7C1684057153446%3B%20v8_s%' \
              '3DLess%2520than%25201%2520day%7C1589450953446%3B; s_sess=%20s_cpc%3D0%3B%20c7%3Daffilcntry%253Dsin' \
              'gapore%3B%20c21%3Dlastname%253Dan%2526firstname%253Dtaicheng%3B%20e13%3Dlastname%253Dan%2526firstn' \
              'ame%253Dtaicheng%253A1%3B%20c13%3Ddocument%2520count%2520%2528high-low%2529%3B%20e41%3D1%3B%20s_cc' \
              '%3Dtrue%3B%20s_ppvl%3Dsc%25253Asearch%25253Aauthor%252520results%252C50%252C50%252C937%252C1920%25' \
              '2C937%252C1920%252C1080%252C1%252CP%3B%20s_sq%3Delsevier-sc-prod%25252Celsevier-global-prod%253D%2' \
              '52526c.%252526a.%252526activitymap.%252526page%25253Dsc%2525253Asearch%2525253Aauthor%25252520resu' \
              'lts%252526link%25253DAn%2525252C%25252520Taicheng%252526region%25253DnameVariant7004832388%252526p' \
              'ageIDType%25253D1%252526.activitymap%252526.a%252526.c%252526pid%25253Dsc%2525253Asearch%2525253Aa' \
              'uthor%25252520results%252526pidt%25253D1%252526oid%25253Dhttps%2525253A%2525252F%2525252Fwww.scopu' \
              's.com%2525252Fauthor%2525252Fsubmit%2525252Fprofile.uri%2525253FauthorId%2525253D7004832388%252525' \
              '26origin%2525253DAuthorNamesList%25252526offset%2525253D1%252526ot%25253DA%3B%20s_ppv%3Dsc%25253Ase' \
              'arch%25253Aauthor%252520results%252C50%252C50%252C937%252C771%252C937%252C1920%252C1080%252C1%252CL%3B'

cookies_list = [i.split('=') for i in cookies_str.split('; ')]
