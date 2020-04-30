#! /usr/bin/python
# -*- coding: utf-8 -*-

import random


def select_sort1(li):
    for i in range(len(li) - 1):
        print(min(li[i+1:len(li)]))
        min_pos = li.index(min(li[i + 1:len(li)]))
        print(i, li[min_pos])
        li[i], li[min_pos] = li[min_pos], li[i]

    return li


li = list(range(10000))
random.shuffle(li)
li = select_sort1(li)
print(li)

dic = dict(a=1, b=2, c=3, d=4)
key_list = list(dic.keys())
for key in key_list:
    del dic[key]
