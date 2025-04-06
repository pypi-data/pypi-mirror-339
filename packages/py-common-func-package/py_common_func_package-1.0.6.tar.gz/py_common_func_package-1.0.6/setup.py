from setuptools import setup, find_packages
import platform

# 判断系统，自动选择编译后缀
ext = ".pyd" if platform.system() == "Windows" else ".so"

setup(
    name="py_common_func_package",
    version="1.0.6",
    authors=[{"name": "wangli", "email": "wl_926454@163.com"}],
    description = "python test common function",
    packages=find_packages(),  # 自动寻找并包括所有包
    package_data={  # 确保混淆后的文件被包含
        '': ['obf/*/__pycache__/*.pyc'],
    },
    include_package_data=True,  # 确保包含 package_data 中的文件
    zip_safe=False,
    install_requires=[  # 如果有依赖的其他包
    ],
)
