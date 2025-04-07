"""
脚手架
"""

import os.path
import subprocess
import sys

from loguru import logger

from pastor.utils import ga_client


def init_parser_scaffold(subparsers):
    sub_parser_scaffold = subparsers.add_parser(
        "startproject", help="Create a new project with template structure."
    )
    sub_parser_scaffold.add_argument(
        "project_name", type=str, nargs="?", help="Specify new project name."
    )
    return sub_parser_scaffold


def create_scaffold(project_name):
    """ create scaffold with specified project name.
    """

    def show_tree(prj_name):
        try:
            print(f"\n$ tree {prj_name} -a")
            subprocess.run(["tree", prj_name, "-a"])
            print("")
        except OSError:
            logger.warning("tree command not exists, ignore.")

    if os.path.isdir(project_name):
        logger.warning(
            f"Project folder {project_name} exists, please specify a new project name."
        )
        show_tree(project_name)
        return 1
    elif os.path.isfile(project_name):
        logger.warning(
            f"Project name {project_name} conflicts with existed file, please specify a new one."
        )
        return 1

    logger.info(f"Create new project: {project_name}")
    print(f"Project Root Dir: {os.path.join(os.getcwd(), project_name)}\n")

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    demo_testcase_request_content = """
config:
    name: "request methods testcase with functions"
    variables:
        foo1: config_bar1
        foo2: config_bar2
        expect_foo1: config_bar1
        expect_foo2: config_bar2
    base_url: "https://postman-echo.com"
    verify: False
    export: ["foo3"]

teststeps:
-
    name: get with params
    variables:
        foo1: bar11
        foo2: bar21
        sum_v: "${sum_two(1, 2)}"
    request:
        method: GET
        url: /get
        params:
            foo1: $foo1
            foo2: $foo2
            sum_v: $sum_v
        headers:
            User-Agent: pastor/${get_pastor_version()}
    extract:
        foo3: "body.args.foo2"
    validate:
        - eq: ["status_code", 200]
        - eq: ["body.args.foo1", "bar11"]
        - eq: ["body.args.sum_v", "3"]
        - eq: ["body.args.foo2", "bar21"]
-
    name: post raw text
    variables:
        foo1: "bar12"
        foo3: "bar32"
    request:
        method: POST
        url: /post
        headers:
            User-Agent: pastor/${get_pastor_version()}
            Content-Type: "text/plain"
        data: "This is expected to be sent back as part of response body: $foo1-$foo2-$foo3."
    validate:
        - eq: ["status_code", 200]
        - eq: ["body.data", "This is expected to be sent back as part of response body: bar12-$expect_foo2-bar32."]
-
    name: post form data
    variables:
        foo2: bar23
    request:
        method: POST
        url: /post
        headers:
            User-Agent: pastor/${get_pastor_version()}
            Content-Type: "application/x-www-form-urlencoded"
        data: "foo1=$foo1&foo2=$foo2&foo3=$foo3"
    validate:
        - eq: ["status_code", 200]
        - eq: ["body.form.foo1", "$expect_foo1"]
        - eq: ["body.form.foo2", "bar23"]
        - eq: ["body.form.foo3", "bar21"]
"""
    demo_testcase_with_ref_content = """
config:
    name: "request methods testcase: reference testcase"
    variables:
        foo1: testsuite_config_bar1
        expect_foo1: testsuite_config_bar1
        expect_foo2: config_bar2
    base_url: "https://postman-echo.com"
    verify: False

teststeps:
-
    name: request with functions
    variables:
        foo1: testcase_ref_bar1
        expect_foo1: testcase_ref_bar1
    testcase: testcases/demo_testcase_request.yml
    export:
        - foo3
-
    name: post form data
    variables:
        foo1: bar1
    request:
        method: POST
        url: /post
        headers:
            User-Agent: pastor/${get_pastor_version()}
            Content-Type: "application/x-www-form-urlencoded"
        data: "foo1=$foo1&foo2=$foo3"
    validate:
        - eq: ["status_code", 200]
        - eq: ["body.form.foo1", "bar1"]
        - eq: ["body.form.foo2", "bar21"]
"""
    ignore_content = "\n".join(
        [".env", "reports/*", "__pycache__/*", "*.pyc", ".python-version", "logs/*"]
    )
    demo_debugtalk_content = """import time

from pastor import __version__


def get_pastor_version():
    return __version__


def sum_two(m, n):
    return m + n


def sleep(n_secs):
    time.sleep(n_secs)
"""
    demo_env_content = "\n".join(["TYPE=ui", "GH_TOKEN=glpat-LD_-wPXsMJQdHvHAj5V-", "DRIVER_LATEST_RELEASE_URL=http://gitlab.lyky.xyz/api/v4/projects/200/repository/files/latest-patch-versions-per-build.json/raw?ref=main", "DRIVER_DOWNLOAD_URL=http://gitlab.lyky.xyz/api/v4/projects/200/repository/files/known-good-versions-with-downloads.json/raw?ref=main", "BASE_URL=https://b2c-test.lyky.com.cn/", "DATABASE_URL=mysql+pymysql://root:rJCuKfeVB6nUZfSk@47.101.134.204:3306/sit_cas_new?charset=utf8mb4"])

    demo_testcase_with_ui = """
config:
    name: "request methods testcase with functions"
    variables:
        value: "#div-hover .dropbtn"
        expect_foo1: '123'
    ignore_cache: true

teststeps:
-
    name: 输入账号密码
    variables:
        send_keys: send_keys
    location:
        - by: ID
          value: input
          action: $send_keys
          data: 'b2cnewtester3'
          desc: '输入用户名'
        - by: ID
          value: 'normal_login_password'
          action: $send_keys
          data: 'aa123456'
          desc: '输入密码'
        - by: CSS_SELECTOR
          value: ".login-agreement .ant-checkbox-input"
          action: click
          sleep: 1
          desc: '勾选同意'
        - by: CSS_SELECTOR
          value: ".login-button-box .login-button"
          action: click
          desc: '点击登录'
    validate:
      - eq:
          by: ID
          value: "phone"
          disabled: 'true'
      - eq:
          by: XPATH
          value: "//input[@autocomplete='one-time-code']"
          placeholder: '输入你的验证码'
      - eq:
          by: XPATH
          value: "//input[@autocomplete='one-time-code']"
          type: 'text'
      - eq:
          by: CSS_SELECTOR
          value: ".ant-input-group-addon button"
          val: '发送验证码'
      - eq:
          by: CSS_SELECTOR
          value: ".ant-form-item-control-input-content button[type='submit']"
          val: '下一步'
-
    name: 发送验证码
    location:
        - by: CSS_SELECTOR
          value: ".ant-input-group-addon button"
          action: click
          desc: '发送验证码'
          sleep: 2
    validate:
      - contains:
          by: CSS_SELECTOR
          value: ".code-input button"
          disabled: 'true'

-
    name: 输入验证码登录
    pre_sql:
      - datasource: test
        dml:
          - 'select code from cn_sms_code order by created_at desc limit 1'
    location:
        - by: XPATH
          value: "//input[@autocomplete='one-time-code']"
          action: send_keys
          data: $code
          desc: '输入正确验证码'
        - by: CSS_SELECTOR
          value: ".ant-form-item-control-input-content button[type='submit']"
          action: click
          desc: '点击下一步'
          sleep: 2
        - action: visibility_of_element_located
          data: '15'
          by: XPATH
          value: "//span[@class='i-layout-menu-side-title-text']"
          desc: '等待首页元素'
    post_sql:
      - datasource: test
        dml:
          - 'select code as code2 from cn_sms_code order by created_at desc limit 1'
    validate:
      - contains:
          by: XPATH
          value: "//span[@class='i-layout-menu-side-title-text']"
          val: '商家首页'
    """

    create_folder(project_name)
    create_folder(os.path.join(project_name, "har"))
    create_folder(os.path.join(project_name, "testcases"))
    create_folder(os.path.join(project_name, "reports"))

    create_file(
        os.path.join(project_name, "testcases", "demo_testcase_request.yml"),
        demo_testcase_request_content,
    )
    create_file(
        os.path.join(project_name, "testcases", "demo_testcase_ref.yml"),
        demo_testcase_with_ref_content,
    )
    create_file(
        os.path.join(project_name, "testcases", "login.yml"),
        demo_testcase_with_ui,
    )
    create_file(os.path.join(project_name, "debugtalk.py"), demo_debugtalk_content)
    create_file(os.path.join(project_name, ".env"), demo_env_content)
    create_file(os.path.join(project_name, ".gitignore"), ignore_content)

    show_tree(project_name)
    return 0


def main_scaffold(args):
    ga_client.track_event("Scaffold", "startproject")
    sys.exit(create_scaffold(args.project_name))
