# pastor

- ***创建venv虚拟环境并激活，最后安装依赖***
```
$ python -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```
---
- ***上传到pypi*** \
上传到pypi需要更新setup.py里的version版本号
```
python setup.py sdist bdist_wheel
python -m pip install --upgrade twine
twine upload --repository pypi dist/*
```
  是否更新成功，可以查看以下地址 \
  https://pypi.org/project/pastor/

---
- ***创建一个新的项目*** \
pastor startproject xxx 
---
- ***运行命令*** \
prun=pastor run: 用于运行 YAML/JSON/pytest 测试用例 \
pmake=pastor make: 用于将 YAML/JSON 测试用例转换为 pytest 文件 \
har2case=pastor har2case: 用于将 HAR 转换为 YAML/JSON 测试用例
---
- ***生成html测试报告*** \
prun 文件路径  --html=report.html 
---
- ***生成allure测试报告*** \
安装: pip install allure-pytest 和 allure并配置 \
步骤一，运行用例生成allure报告内容 \
prun ./testcases/test_har.yml --alluredir=./reports/tmp \
#步骤二，根据收集的内容再生成allure报告html文件 \
allure generate ./reports/tmp -o allure-report --clean  #  --clean是为了清空已有的测试报告； -o allure-report 是指定清空测试报告的文件allure-report

