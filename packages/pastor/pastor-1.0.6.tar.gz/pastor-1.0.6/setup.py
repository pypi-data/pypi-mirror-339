

from setuptools import find_packages, setup


setup(
    name="pastor",
    version="1.0.6",
    python_requires=">=3.7",
    packages=find_packages(exclude=["examples", "tests", "tests.*"]),
    description="ui and api autotest",
    author="chliang",
    install_requires = [
        'selenium~=4.25.0',
        'requests~=2.32.3',
        'webdriver_manager_zh~=4.0.3',
        'pytest~=8.3.3',
        'urllib3~=2.2.3',
        'loguru~=0.7.2',
        'PyYAML~=6.0.2',
        'pydantic~=2.9.2',
        'jinja2~=3.1.4',
        'sentry_sdk==2.17.0',
        'jmespath~=1.0.1',
        'starlette~=0.41.2',
        'fastapi~=0.115.4',
        'SQLAlchemy~=2.0.36',
        'requests_toolbelt~=1.0.0',
        'pywin32==308',
        'wheel==0.44.0',
        'pymysql==1.1.1',
        'black==24.10.0',
        'validators==0.34.0'
    ],
    entry_points={
        'console_scripts': [
            'har2case=pastor.cli:main_har2case_alias',
            'pmake=pastor.cli:main_make_alias',
            'prun=pastor.cli:main_prun_alias',
            'pastor=pastor.cli:main',
            'locusts=pastor.ext.locust:main_locusts'
        ]
    }
)