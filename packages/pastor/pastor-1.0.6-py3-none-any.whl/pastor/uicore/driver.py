#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time   :2024/10/29 16:18
# @Author : liangchunhua
# @Desc   :
import json
import os
from enum import Enum
from venv import logger

from pydantic import Field, BaseModel
from pydantic.v1 import HttpUrl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager_zh.chrome import ChromeDriverManager

from pastor.exceptions import ParamsError
from pastor.uicore.config import get_domain, is_read_cache
import validators

class BrowserTypeEnum(str, Enum):
    """浏览器类型"""
    CHROME = "Chrome"
    FIREFOX = "Firefox"
    EDGE = "Edge"
    IE = "IE"


class DriverSetting(BaseModel):
    """driver设置"""
    remote_url: str = Field("http://127.0.0.1:4444/wb/hub", description="远程地址")
    browser: str = Field(BrowserTypeEnum.CHROME, description="浏览器名称")
    headless: bool = Field(True, description="是否无头模式")
    page_load_timeout: int = Field(90, description="页面加载超时时间")
    implicitly_wait_time: int = Field(5, description="元素等待超时时间")


class AutoDriver():
    def __init__(self, ignore_browser_cache: bool = False):
        from pastor.uicore.config import get_remote_url, is_headless, get_page_load_timeout, \
            get_implicitly_wait_time, get_window_size
        setting = DriverSetting(
            remote_url=get_remote_url(),
            browser=BrowserTypeEnum.CHROME,
            headless=is_headless(),
            page_load_timeout=get_page_load_timeout(),
            implicitly_wait_time=get_implicitly_wait_time(),
        )
        self.page_load_timeout = setting.page_load_timeout
        self.implicitly_wait_time = setting.implicitly_wait_time
        if setting.browser == BrowserTypeEnum.CHROME:
            options = Options()
            # 设置浏览器尺寸
            options.add_argument(get_window_size())
            # 通过端口号接管已打开的浏览器
            # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            # 添加浏览器缓存
            user_directory_path = os.path.join(os.path.expanduser('~'), "selenium_chrome_cookies")
            if not os.path.exists(user_directory_path):
                # 缓存路径不存在时，直接创建
                options.add_argument(f'--user-data-dir={user_directory_path}')
            # options.add_argument(f'--disk-cache-dir={user_directory_path}')
            elif is_read_cache() == 'true' and ignore_browser_cache is False:
                options.add_argument(f'--user-data-dir={user_directory_path}')

            options.add_argument('--disable-gpu')
            # linux无头模式以root用户运行，开启可能会报错
            options.add_argument("--no-sandbox")
            # options.add_argument('--ignore-certificate-errors')
            # options.add_experimental_option("excludeSwitches",
            #                                 ['load-extension', 'enable-automation', 'enable-logging'])
            if setting.remote_url != 'http://127.0.0.1:4444/wb/hub':
                """远程执行"""
                # 默认vnc密码：secret
                if setting.headless:
                    options.add_argument("--headless")
                self.driver = webdriver.Remote(command_executor=setting.remote_url, options=options)
            else:
                """本地执行"""
                # os.environ['GH_TOKEN'] = '' # gitlab访问token
                from pastor.uicore.config import driver_latest_release_url, driver_download_url
                latest_release_url = driver_latest_release_url() if driver_latest_release_url() else 'https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build.json'
                url = driver_download_url() if driver_download_url() else 'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'
                # drivers = webdriver.Chrome(service=ChromeService(
                #     ChromeDriverManager(url=url, latest_release_url=latest_release_url).install()))
                # self.drivers = webdriver.Chrome(executable_path=setting.executable_path, options=options)
                driver_path = ChromeDriverManager(url=url, latest_release_url=latest_release_url).install()
                self.driver = webdriver.Chrome(options, service=webdriver.ChromeService(driver_path))
        else:
            raise Exception(f"暂不支持其他浏览器: {setting.browser}")
        # 元素等待超时时间
        self.driver.implicitly_wait(setting.implicitly_wait_time)  # seconds
        # 页面刷新超时时间
        self.driver.set_page_load_timeout(setting.page_load_timeout)  # seconds

    def open(self, url):
        r = validators.url(url)
        if not r:
            if self.driver:
                self.driver.quit()
            raise r
        self.driver.get(url)
        # if is_read_cookie() is True:
        #     self.read_browser_cookies(url)
        return self.driver

    def get_session_variables(self):
        """获取session变量"""
        return self._session_variables

    def quit(self):
        """退出"""
        self.driver.quit()

    def get_driver_session_id(self):
        """获取session_id"""
        return self.driver.session_id

    def get_screenshot(self, screenshot_type="base64", file_path=None):
        """截图"""
        if screenshot_type == "base64":
            """方法得到图片的base64编码"""
            return self.driver.get_screenshot_as_base64()
        elif screenshot_type == "png":
            """方法得到图片的二进制数据"""
            return self.driver.get_screenshot_as_png()
        elif screenshot_type == "file":
            """方法得到图片的二进制数据"""
            if not file_path:
                raise Exception("截图路径不能为空")
            return self.driver.get_screenshot_as_file(file_path)
        else:
            raise Exception(f"不支持的截图类型: {screenshot_type}")

    def save_browser_cookies(self):
        cookies = self.driver.get_cookies()
        json_cookies = json.dumps(cookies)
        directory = os.path.join(os.path.expanduser('~'), "selenium_chrome_cookies.json")
        logger.info(f'browser cookies save : {directory}')
        with open(directory, 'w') as f:
            f.write(json_cookies)

    def read_browser_cookies(self, url):
        self.driver.delete_all_cookies()
        directory = os.path.join(os.path.expanduser('~'), "selenium_chrome_cookies.json")
        with open(directory, 'r', encoding='utf-8') as f:
            cookie_list = json.loads(f.read())
        if len(cookie_list) > 0:
            for cookie in cookie_list:
                # 解决统一登录平台和实际登录域名不一致
                cookie['domain'] = get_domain()
                # 删除过期时间
                del cookie['expiry']
                self.driver.add_cookie(cookie)
            self.driver.get(url)
            self.driver.refresh()


def browser_type(bw_type, open_url):
    if bw_type == "Chrome":
        pass

    elif bw_type == "Edge":
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager_zh.microsoft import EdgeChromiumDriverManager
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        driver.get(open_url)

    elif bw_type == "Firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager_zh.firefox import GeckoDriverManager
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.get(open_url)

    elif bw_type == "IE":
        from selenium.webdriver.ie.service import Service as IEService
        from webdriver_manager_zh.microsoft import IEDriverManager
        driver = webdriver.Ie(service=IEService(IEDriverManager().install()))
        driver.get(open_url)


def test():
    from webdriver_manager_zh.chrome import ChromeDriverManager
    from webdriver_manager_zh.core.os_manager import OperationSystemManager
    from webdriver_manager_zh.core.file_manager import FileManager
    from webdriver_manager_zh.core.driver_cache import DriverCacheManager

    # https://registry.npmmirror.com/-/binary/chrome-for-testing

    # 配置操作系统管理器
    os_manager = OperationSystemManager(os_type="win64")

    # 配置文件管理器
    file_manager = FileManager(os_system_manager=os_manager)

    # 配置驱动缓存管理器
    cache_manager = DriverCacheManager(file_manager=file_manager)

    # 配置 Chrome 驱动管理器
    chrome_manager = ChromeDriverManager(cache_manager=cache_manager)
    chrome_manager.install()

    # OperationSystemManager: 操作系统管理器，用于配置操作系统的类型。
    # FileManager: 文件管理器，用于管理文件操作。
    # DriverCacheManager: 驱动缓存管理器，用于管理驱动的缓存。
    # ChromeDriverManager: Chrome


if __name__ == '__main__':
    a = AutoDriver().open('https://www.baidu.com/')
