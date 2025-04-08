from setuptools import setup, find_packages

setup(
    name='ma100-odbc',  # 修改包名为 ma100-odbc
    version='0.1.0',
    packages=find_packages(include=['ma100.odbc']),  # 明确指定 ma100.odbc 包
    namespace_packages=['ma100'],  # 定义命名空间包
    install_requires=[
        # 列出 odbc 包的依赖
    ],
    entry_points={
        'console_scripts': [
            # 如果有命令行工具，可以在这里定义
        ]
    },
    package_data={
        # 如果有需要包含的数据文件，可以在这里定义
        '': ['*.txt', '*.rst'],
        'mypackage': ['data/*.dat'],
    },
    include_package_data=True,
)