# -*- coding: utf-8-*-
from setuptools import setup, find_packages
setup(
    # 以下为必需参数
    name='scrapy-rabbitmq-scheduler-saylor',  # 模块名
    version='1.0.3',  # 当前版本
    description='Rabbitmq for Distributed scraping',  # 简短描述
    author='saylorzhu',
    author_email='531301071@qq.com',
    license='MIT',
    url='https://github.com/SaylorZhu/scrapy-rabbitmq-scheduler.git',
    install_requires=[
        'pika',
        'Scrapy'
    ],
    packages=['scrapy_rabbitmq_scheduler_saylor'],
    package_dir={'': 'src'}
)
