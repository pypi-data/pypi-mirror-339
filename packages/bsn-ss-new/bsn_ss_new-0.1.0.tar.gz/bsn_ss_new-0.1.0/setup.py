from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bsn-ss-new",  # 你希望在 PyPI 上使用的包名
    version="0.1.0",  # 设置一个初始版本号，根据你的修改进行调整
    author="Your Name",  # 你的名字或组织名称
    author_email="your.email@example.com",  # 你的邮箱
    description="A modified Shadowsocks package",  # 包的简短描述
    long_description=long_description,  # 包的详细描述 (从 README.md 读取)
    long_description_content_type="text/markdown",  # 指定 README.md 的格式
    url="https://github.com/hebinboss/bsn-ss-new",  # 你的项目 GitHub 仓库 URL (如果适用)
    packages=find_packages(include=['.']),  # 查找当前目录下的所有包 (因为你的 __init__.py 在根目录)
    python_requires=">=2.7",  # 指定所需的 Python 版本
    install_requires=[  # 列出你的包的依赖项 (如果需要)
        # 例如: 'cryptography>=3.4',
        'pycryptodome>=3.8.0',
        'blinker>=1.4',
        'dnspython>=1.15.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 替换为你的实际许可证
        "Operating System :: OS Independent",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Security :: Cryptography",
    ],
    entry_points={
        'console_scripts': [
            'sslocal = local:main',
            'ssserver = server:main',
            'ssmanager = manager:main',
            'ssshell = shell:main',
        ],
    },
)
