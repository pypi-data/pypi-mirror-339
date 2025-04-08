from setuptools import setup, find_packages

description = open("README.md", "r", encoding="utf-8").read()

setup(
    name="request_replay",
    version="0.1.1",
    author="htamlive",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "tqdm",
        "httpx[http2]",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)