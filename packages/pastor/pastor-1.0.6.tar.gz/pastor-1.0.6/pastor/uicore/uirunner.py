#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time   :2024/10/31 16:50
# @Author : liangchunhua
# @Desc   :
import os

import validators
from validators import ValidationError


def open(url2):
    r = validators.url(url2)
    if not r:
        raise r
    else:
        print(2)
    print(3)

if __name__ == '__main__':
    appdata_path = os.environ['LOCALAPPDATA'] if 'LOCALAPPDATA' in os.environ else os.environ['APPDATA']
    cache_path = os.path.join(appdata_path, 'Google', 'Chrome', 'User Data')

    print(cache_path+'\\')