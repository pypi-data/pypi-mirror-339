from setuptools import setup, find_packages

VERSION = '2.0.7'
DESCRIPTION = 'hoanggiakiet: Customized Zalo API for Python'
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="hoanggiakiet",
    version=VERSION,
    author="Hoang Gia Kiet",
    author_email="hoanggiakiet@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests', 'aiohttp', 'aenum', 'attr', 'pycryptodome', 'datetime', 'munch', 'websockets'],
    keywords=['python', 'zalo', 'api', 'zalo api', 'zalo chat', 'requests', 'hoanggiakiet'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ]
)