from setuptools import setup, find_namespace_packages

setup(
    name="qlsdk-test",
    version="0.1",
    packages=find_namespace_packages(where="src", include=["qlsdk.*"]),
    package_dir={"": "src"},
    install_requires=[],  # 总包无依赖，子模块若有依赖需自行声明
    # 可选：声明子模块为独立"extra"依赖（按需安装）
    extras_require={
        "ar4m": [],
        "c64r": [],
        "x8": [],
    },
)