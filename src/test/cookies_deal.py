#! /usr/bin/python
# -*- coding: utf-8 -*-



cookies_str = 'scopus.machineID=C95FAA82D76902CFBA9ADB44D5C59CF2.wsnAw8kcdt7IPYLO0V48gA; optimizelyEndUserId=oeu1' \
              '588830449793r0.7402451939845718; optimizelyBuckets=%7B%7D; xmlHttpRequest=true; optimizelySegments=%' \
              '7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%2227' \
              '8903113%22%3A%22referral%22%7D; __cfruid=ccee03229d9a9aa5a08d9d8893d9634dd8dd7b89-1589419179; chec' \
              'k=true; javaScript=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; screenInfo="1080:1920"; __cfd' \
              'uid=d2bc1953f026de4ee3abec5f6eb4cc0731589448214; SCSessionID=38B0E0A5EFC9E1FCDD83B87EA240F115.wsnA' \
              'w8kcdt7IPYLO0V48gA; scopusSessionUUID=a501b7a5-7cea-4a0d-9; AWSELB=CB9317D502BF07938DE10C841E762B' \
              '7A33C19AADB17A59DD6BA0784DD207E0A02D026B49B728C51DE21F0721BEC11F8AF279A07842BAFDF2ADE925350150D79' \
              '00CAD0CA8A60A1E3E7F2A0213D204EDAE70096BF096; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=1075005958%7' \
              'CMCIDTS%7C18396%7CMCMID%7C23612113200045070330531324322910847678%7CMCAAMLH-1590053020%7C11%7CMCAA' \
              'MB-1590053020%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589455420s%7CNON' \
              'E%7CMCAID%7CNONE%7CMCCIDH%7C-1185074918%7CvVersion%7C4.4.1; mbox=PC#0d2fc3c7b0294bd788e2024d38633' \
              '7d6.22_0#1652693070|session#1c37b60c5fd7435ea9380c1109e66257#1589448759; s_pers=%20v8%3D15894482' \
              '89665%7C1684056289665%3B%20v8_s%3DLess%2520than%25201%2520day%7C1589450089665%3B%20c19%3Dsc%253A' \
              'search%253Aauthor%2520searchform%7C1589450089671%3B%20v68%3D1589448268660%7C1589450089676%3B; s_' \
              'sess=%20s_cpc%3D0%3B%20c7%3Daffilcntry%253Dsingapore%3B%20c21%3Dlastname%253Dcai%2526firstname%2' \
              '53Dan%3B%20e13%3Dlastname%253Dcai%2526firstname%253Dan%253A1%3B%20c13%3Ddocument%2520count%2520%2' \
              '528high-low%2529%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Asearch%25253Aauthor%252520searchform%252' \
              'C77%252C77%252C937%252C1920%252C937%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dsc%25253Asearch%252' \
              '53Aauthor%252520searchform%252C77%252C77%252C937%252C771%252C937%252C1920%252C1080%252C1%252CL%3B' \
              '%20e41%3D1%3B%20s_sq%3Delsevier-sc-prod%25252Celsevier-global-prod%253D%252526c.%252526a.%252526a' \
              'ctivitymap.%252526page%25253Dsc%2525253Asearch%2525253Aauthor%25252520searchform%252526link%25253' \
              'D%252525E6%252525A3%25252580%252525E7%252525B4%252525A2%252526region%25253DauthorLookupSearchForm' \
              '%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%252526pid%25253Dsc%2525253Asearch%' \
              '2525253Aauthor%25252520searchform%252526pidt%25253D1%252526oid%25253Dfunctiononclick%25252528event' \
              '%25252529%2525257BcheckAuthOrOrcid%25252528this.form.name%25252529%2525253B%2525257D%252526oidt%25' \
              '253D2%252526ot%25253DSUBMIT%3B'

cookies_list = [i.split('=') for i in cookies_str.split('; ')]

pass
