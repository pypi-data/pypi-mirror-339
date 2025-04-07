from setuptools import setup, find_packages


setup(
    name="request_replay",
    version="0.1.0",
    author="htamlive",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "tqdm",
        "httpx[http2]",
    ],
)