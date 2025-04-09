from setuptools import setup, find_packages

setup(
    name='justasimpletest',  # 模块名称
    version='0.0.0',  # 版本号
    description='A short description of your module',  # 模块简短描述
    long_description=open('README.md').read(),  # 详细描述，通常是 README 文件的内容
    long_description_content_type='text/markdown',  # markdown 格式
    author='szx21023',  # 作者信息
    author_email='szx21023@gmail.com',  # 作者邮箱
    url='https://github.com/szx21023/fastapi-base',  # 项目链接
    packages=find_packages(),  # 自动查找包
    classifiers=[  # 分类标签
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[  # 依赖库
        'requests',  # 举例：模块依赖 requests
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)
