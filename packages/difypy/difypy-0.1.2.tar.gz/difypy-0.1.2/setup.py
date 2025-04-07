from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="difypy",
    version="0.1.2",
    author="likun.pm",
    author_email="likun2440@gmail.com",
    description="Python SDK for Dify API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/likunpm/difypy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.1",
        "aiohttp>=3.8.0",
    ],
) 