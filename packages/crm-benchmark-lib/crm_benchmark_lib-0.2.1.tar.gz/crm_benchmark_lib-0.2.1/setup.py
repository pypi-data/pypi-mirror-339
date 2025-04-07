from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crm-benchmark-lib",
    version="0.2.1",
    author="CRM Benchmark Team",
    author_email="info@aiagentchallenge.com",
    description="Client library for the CRM AI Agent Benchmarking API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aiagentchallenge/crm-benchmark-lib",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.1.0",
        "tqdm>=4.50.0",
    ],
    include_package_data=True,
) 