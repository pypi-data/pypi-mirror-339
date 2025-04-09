from setuptools import setup, find_packages

setup(
    name="excel4rag",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "openpyxl>=3.1.2",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],
    author="Ben",
    author_email="benmcnicol@gmail.com",
    description="A Python package for extracting tables and key-value pairs from Excel files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/benmcnicol/excel4rag",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 