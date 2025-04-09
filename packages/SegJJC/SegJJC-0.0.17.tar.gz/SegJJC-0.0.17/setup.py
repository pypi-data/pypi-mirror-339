from setuptools import setup, find_packages

setup(
    name="SegJJC",
    version="0.0.17",
    author="hfh",
    author_email="your.email@example.com",
    description="A AI train Python package of JJC for Detect,seg,classify",
    url="https://gitee.com/hfh936784552/Segjjc_git",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "SegJJC": ["dll/*.dll",
                   "fcn/*.json",
                   "fcn/*.txt",
                   "demo/*.json",
                   "demo/*.py", ],  # 指定要包含的 .pyd 文件
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # YOLOv8
        "ultralytics>=8.3.104",
        # mvtec-halcon（假设存在）
        "mvtec-halcon==24050",
        "onnxruntime>=1.18.0"
    ],
    dependency_links=[
        "https://download.pytorch.org/whl/cu116",  # 指定 PyTorch 的仓库地址
    ],
)



# from setuptools import setup, find_packages
# from glob import glob
# import os
#
# # # 查找所有的 .pyd 文件
# # pyd_files = glob("my_package/**/*.pyd", recursive=True)
#
# setup(
#     name="netpin2excel",                # 替换为你的包名
#     version="0.1.1",                  # 版本号
#     author="hfh",               # 作者信息
#     author_email="your.email@example.com",
#     description="A sample Python package with a .pyd file",
#     url="https://github.com/yourusername/my_package",  # 项目主页
#     packages=find_packages(),         # 自动查找包
#     include_package_data=True,        # 包含所有文件，包括 .pyd 文件
#     # package_data={
#     #     "my_package": ["netpin_process.pyd"],      # 指定包含 .pyd 文件
#     # },
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.6",          # Python 版本要求
#     install_requires=[],              # 依赖项，可根据需要添加
# )
