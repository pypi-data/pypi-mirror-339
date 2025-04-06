from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(this_directory, "README.md")
long_description = open(readme_path, encoding="utf-8").read() if os.path.exists(readme_path) else ""

setup(
    name="web3rpc",
    version="2.1.0",
    author="web3rpcs",
    description="Tools for Web3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
