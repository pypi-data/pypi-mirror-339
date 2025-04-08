from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="autools_isee",  # 包名称（PyPI唯一标识）
    version="0.1.0",         # 初始版本号
    author="ISEE",      # 作者名称
    author_email="your.email@example.com",
    description="Advanced string manipulation utilities",  # 简短描述
    long_description=long_description,  # 详细说明（从README读取）
    long_description_content_type="text/markdown",
    url="",  # 项目地址
    packages=find_packages(),  # 自动发现所有包
    classifiers=[             # 分类器（帮助用户搜索）
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # Python版本要求
    install_requires=[        # 依赖库
        'requests>=2.32.3',  # 示例依赖
    ],
    extras_require={          # 可选依赖
        'dev': [
            'requests>=2.32.3'
        ]
    },
    entry_points={            # 命令行工具配置
        'console_scripts': [
            'strtool=autools.cli:main',  # 示例CLI入口
        ],
    },
)