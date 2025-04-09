# setup.py
from setuptools import setup, find_packages

setup(
    name="cipherShad0w",
    version="0.1.1",
    packages=find_packages(),
    author="cipher-shad0w",
    author_email="Jannis.krija@icloud.com",
    description="Zeug von Jannis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cipher-shad0w/sorting_visualizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
