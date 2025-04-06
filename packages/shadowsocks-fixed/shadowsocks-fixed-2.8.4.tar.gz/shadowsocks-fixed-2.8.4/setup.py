from setuptools import setup

setup(
    name="shadowsocks-fixed",
    version="2.8.4",  # 更新版本号
    packages=['shadowsocks', 'shadowsocks.crypto'],
    description="A fixed version of Shadowsocks with Python 3.10+ and OpenSSL 1.1+ compatibility",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/shadowsocks-fixed",
    license="Apache License 2.0",
    install_requires=['pycryptodome'],
)
