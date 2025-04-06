

from setuptools import setup, find_packages

setup(
    name="mathutilsVV",
    version="0.1.1",
    author="renfm",
    author_email="1210139408@qq.com",
    description="A simple package for basic mathematical operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mathutils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)