from setuptools import setup, find_packages

setup(
    name='ma100-plot',  # 修改包名为 ma100-plot
    version='0.1.0',
    packages=find_packages(include=['ma100.plot']),  # 明确指定 ma100.plot 包
    namespace_packages=['ma100'],  # 定义命名空间包
    install_requires=[
        # 列出 plot 包的依赖
    ],
    entry_points={
        'console_scripts': [
            # 如果有命令行工具，可以在这里定义
        ]
    }
)