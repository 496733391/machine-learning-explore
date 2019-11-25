#! /usr/bin/python
# -*- coding: utf-8 -*-

import json
json_file_path = 'C:/Users/lenovo/Desktop/d_k4pl6i.json'
with open(json_file_path, 'r') as load_f:
    load_dict = json.load(load_f)
print(load_dict)
