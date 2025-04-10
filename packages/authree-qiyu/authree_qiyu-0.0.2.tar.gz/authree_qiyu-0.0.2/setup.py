from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="authree_qiyu",                               # 包名
    version="0.0.2",                                 # 版本号
    author="qiyu",                                     # 作者
    author_email="yiyanjyx@yeah.net",                        # 邮箱
    description="",                      # 简短描述
    long_description=long_description,               # 详细说明
    long_description_content_type="text/markdown",   # 详细说明使用标记类型
    # url="https://github.com/",                     # 项目主页
    packages=find_packages(where="src"),             # 需要打包的部分
    package_dir={"": "src"},                         # 设置src目录为根目录
    python_requires=">=3.0",                         # 项目支持的Python版本
    # install_requires=required,                     # 项目必须的依赖
    package_data={
        'src': ['crud/ephe/*'],
    },
    include_package_data=True                       # 是否包含非Python文件（如资源文件）
)
