from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bsn-ss-new",
    version="0.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A modified Shadowsocks package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_github_username/bsn-ss-new",
    # 移除 packages 参数
    py_modules=[
        'asyncdns',
        'common',
        'daemon',
        'encrypt',
        'eventloop',
        'local',
        'lru_cache',
        'manager',
        'server',
        'shell',
        'tcprelay',
        'udprelay',
    ],
    python_requires=">=3.7",
    install_requires=[
        'pycryptodome>=3.8.0',
        'blinker>=1.4',
        'dnspython>=1.15.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
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
