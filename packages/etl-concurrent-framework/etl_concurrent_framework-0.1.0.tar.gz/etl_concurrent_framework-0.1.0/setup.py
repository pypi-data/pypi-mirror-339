from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="etl_concurrent_framework",  # PyPI上的包名，建議用下劃線
    version="0.1.0",                  # 版本號
    author="himmel0549",              # 作者
    author_email="your.email@example.com",  # 作者郵箱
    description="高效能、可擴展的ETL併發處理框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/etl-concurrent-framework",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=["etl_concurrent_framework", "etl_concurrent_framework.*"]),
    python_requires=">=3.8",
    install_requires=[
        "pandas",
        "numpy",
        "openpyxl",  # Excel支持
        "pyarrow",   # Parquet支持
        "psutil",    # 系統資源監控
        "et_xmlfile",
        "python-dateutil",
        "pytz",
        "tzdata",
        "six",
    ],
)