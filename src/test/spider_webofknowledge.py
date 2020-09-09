# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re
import xlwt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
}

def get_regex_data(regex, buf):
    """
    正则抓取
    :param regex:正则语法
    :param buf: html
    :return: str
    """
    group = re.search(regex, buf)
    if group:
        return group.groups()[0]
    else:
        return ''

def getXpath(xpath, content):
    """
    xpath 抓取
    :param xpath:  xpath语法
    :param content: html内容
    :return: list
    """
    out = []
    tree = etree.HTML(content)
    results = tree.xpath(xpath)
    print(results)
    for result in results:
        if 'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)):
            out.append(result)
        else:
            out.append(etree.tostring(result))
    return out

def run():
    #创建excel，添加头信息
    # wbk = xlwt.Workbook()
    # sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    # rowsTitle = ['UT号', '地址类型', '作者名称', '地址位次', '地址', '增强组织信息']
    # for i in range(0, len(rowsTitle)):
    #     sheet.write(0, i, rowsTitle[i])
    # wbk.save('webofknowledge.xlsx')
    # num = 1
    # sheet_num = 1


    keyword_list = [1]
    # 读取keyword.txt 获取id
    # file = open('keyword.txt','r',encoding='utf-8-sig')
    # keywords = file.readlines()
    # for keyword in keywords:
    #     keyword_list.append(str(keyword).strip())
    # file.close()

    proxies = {
        "http": "http://202.120.43.93:8059"
    }

    for k in keyword_list:
        print(k)
        url = 'http://apps.webofknowledge.com/CitedFullRecord.do?product=WOS&colName=WOS&SID=8EiqbVPdAtDaBXMmcWH&search_mode=CitedFullRecord&isickref=WOS:000502546200008'
        session = requests.session()
        temp = session.post('http://apps.webofknowledge.com/UA_GeneralSearch.do', headers=headers, proxies=proxies, timeout=300)
        response = session.get(url, headers=headers, proxies=proxies, timeout=300)
        print(response)
        table = getXpath('//div[@class="l-content "]//div[@class="block-record-info"]', response)
        # table = getXpath('/html/body/div[1]/div[26]/form[3]/div/div/div/div[1]/div/div', response)
        for t in table:
            print('123', t)
            try:
                title3 = str(getXpath('//div/div[@class="title3"]/text()',t)[0]).strip()
            except:
                continue
            #判断是否是作者信息部分。
            if title3 == '作者信息':
                msg_tables = re.findall('(<span class="FR_label">[\d\D]*?</table>)',str(t).strip())
                num_ = 1
                for mt in msg_tables:

                    address_type = get_regex_data('<span class="FR_label">(.*?):', mt) #地址类型
                    author = get_regex_data('<span class="FR_label">.*?</span>(.*?)<',mt).replace('\\n','') #作者
                    address_table = getXpath('//table/tr/td[2]',mt)
                    print('*********')
                    print(address_table)
                    for at in address_table:
                        print(at)
                        try:
                            address = str(getXpath('//td/text()',at)[0]).strip()  #地址
                        except:
                            address = str(getXpath('//td/a/text()', at)[0]).strip() #地址

                        information_table = getXpath('//td/span/preferred_org/text()',at) #增强组织信息列表
                        for it in information_table:

                            item = []
                            item.append(str(k).strip())
                            item.append(str(address_type).strip())
                            item.append(str(author).strip())
                            item.append(str(num_).strip())
                            item.append(str(address).strip())
                            item.append(str(it).strip())

                            print(item)

                            # 判断是否大于6W行，大于6W行切换excel的sheet
                            if num > 60000:
                                s_num = sheet_num + 1
                                sheet = wbk.add_sheet('Sheet%s' % s_num, cell_overwrite_ok=True)
                                rowsTitle = ['UT号', '地址类型', '作者名称', '地址位次', '地址', '增强组织信息']
                                for i in range(0, len(rowsTitle)):
                                    sheet.write(0, i, rowsTitle[i])
                                wbk.save('webofknowledge.xlsx')
                                num = 1
                                sheet_num = s_num
                            #写入excel
                            for x in range(len(item)):
                                sheet.write(num, x, item[x])
                            num += 1
                            wbk.save('webofknowledge.xlsx')


                    num_ += 1


            else:
                continue



if __name__ == '__main__':

    run()