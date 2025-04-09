from setuptools import setup, find_packages

setup(
    name="excel4rag",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "openpyxl>=3.1.2,<4.0.0",
        "pandas>=2.0.3,<3.0.0",
        "numpy>=1.24.3,<2.0.0",
    ],
    python_requires=">=3.8,<3.12",
    author="Ben",
    author_email="benmcnicol@gmail.com",
    description="A Python package for extracting tables and key-value pairs from Excel files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/benmcnicol/excel4rag",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    keywords="excel, tables, json, html, markdown, rag, data extraction",
    project_urls={
        "Bug Reports": "https://github.com/benmcnicol/excel4rag/issues",
        "Source": "https://github.com/benmcnicol/excel4rag",
    },
) 