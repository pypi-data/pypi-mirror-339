#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date   :2024/11/6 9:21
# @Author : liangchunhua
# @Desc   :
from typing import List, Any, Text

from selenium.webdriver.remote.webelement import WebElement


def check_eq(elements: List[WebElement], exp: Any, message: Text = ""):
    assert True