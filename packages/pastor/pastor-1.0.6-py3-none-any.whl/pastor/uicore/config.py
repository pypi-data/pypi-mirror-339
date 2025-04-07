#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date   :2024/11/11 13:57
# @Author : liangchunhua
# @Desc   :
import os

from pastor.models import StepTypeEnum


def is_headless():
    return os.getenv("HEADLESS", False)


def get_page_load_timeout():
    return os.getenv("PAGE_LOAD_TIMEOUT", 30)


def get_implicitly_wait_time():
    return os.getenv("IMPLICITLY_WAIT_TIME", 3)


def get_window_size():
    return os.getenv("WINDOW_SIZE", '--start-maximized')


def get_remote_url():
    return os.getenv("REMOTE_URL", 'http://127.0.0.1:4444/wb/hub')


def get_domain():
    # 读取cookie数据时的domain,统一登录平台和实际应用url不一致，需要替换
    return os.getenv("DOMAIN", '.lyky.com.cn')


def is_read_cache():
    return os.getenv("CACHE", 'false').lower()


def get_browser():
    from pastor.uicore.driver import BrowserTypeEnum
    return os.getenv("BROWSER", BrowserTypeEnum.CHROME)


def gh_token():
    # gitlab接口请求token
    return os.getenv("GH_TOKEN", None)


def step_type():
    # 执行类型，api或ui
    return os.getenv('TYPE', StepTypeEnum.API).upper()


def database_url():
    # 默认database配置: mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4
    return os.getenv('DATABASE_URL', None)


def driver_latest_release_url():
    # 获取webdriver最后版本
    return os.getenv('DRIVER_LATEST_RELEASE_URL', None)


def driver_download_url():
    # 获取webdriver驱动下载信息
    return os.getenv('DRIVER_DOWNLOAD_URL', None)

def base_url():
    # 获取webdriver驱动下载信息
    return os.getenv('BASE_URL', None)
