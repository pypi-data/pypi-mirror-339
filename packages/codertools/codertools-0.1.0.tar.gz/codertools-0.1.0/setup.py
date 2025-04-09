from setuptools import find_packages, setup

setup(
    name="codertools",
    version="0.1.1",
    author="zhaoxuefeng",
    author_email="82304233@qq.com",
    description="负责工具",
    url="",
    packages=find_packages(),
    install_requires=[
        "pydantic~=2.10.4",
        "pyyaml~=6.0.2",
        "loguru~=0.7.3",

    ],
    python_requires=">=3.10",
)
