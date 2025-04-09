from setuptools import setup, find_packages

setup(
    name='latlon_and_rowcol',  # 包名
    version='0.1.3',  # 版本号
    packages=find_packages(),  # 自动查找包中的所有子包和模块
    package_data={
        'latlon_and_rowcol': ['config.yml']  # 指定包含在包中的非Python文件
    },
    author='ld',
    author_email='1542864710@qq.com',
    description='用于风云卫星数据的经纬度和坐标互转',
    long_description=open('README.md',encoding='UTF-8').read(),  # 长描述，通常从README中读取
    long_description_content_type='text/markdown',  # 如果README是Markdown格式
    keywords=['经纬度', '坐标'],  # 关键字
    classifiers=[  # 分类，用于PyPI上的搜索和过滤
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)