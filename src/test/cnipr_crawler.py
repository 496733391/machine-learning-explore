#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import base64

from src.Scopus_Crawler.scopus_config import headers

headers['content-type'] = 'application/x-www-form-urlencoded'


login_url = 'http://search.cnipr.com/user!gotoLogin.action?forward=pages!operation.action'
session = requests.session()
login_page = session.get(url=login_url, headers=headers)
valid_code_pic = session.get('http://search.cnipr.com/user!imagecode.action')

# 图片识别
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

img = base64.b64encode(valid_code_pic.content)

params = {"image": img}
access_token = '24.4ca6688ffc63afbda8c00659c3c037bd.2592000.1603508761.282335-22749485'
request_url = request_url + "?access_token=" + access_token + 'language_type=ENG'
headers_pic = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers_pic)
print(response.json())
print(response.json()['words_result'][0]['words'].replace(' ', ''))

