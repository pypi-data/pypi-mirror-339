from setuptools import setup, find_packages

setup(
    name='ma100',
    version='0.1.0',

    packages=find_packages(include=['ma100']),
    # 明确指定 ma100.plot 包
    # namespace_packages=['ma100'],  # 定义命名空间包

    install_requires=[
        'ma100-odbc>=0.1.0',
        'ma100-plot>=0.1.0',  # 修改依赖项为 ma100-plot
        # 列出 ma100 包的其他依赖
    ],
    entry_points={
        'console_scripts': [
            # 如果有命令行工具，可以在这里定义
        ]
    }
)