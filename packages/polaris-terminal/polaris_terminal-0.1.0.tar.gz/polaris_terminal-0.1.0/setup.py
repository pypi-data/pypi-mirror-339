#!/usr/bin/env python
"""
Setup script for Polaris Terminal package
"""

from setuptools import find_packages, setup

# Read version from __init__.py
with open("polaris_terminal/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"\'')
            break
    else:
        version = "0.1.0"

# Read long description from README.md
try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Polaris Terminal - CLI tool for connecting to Polaris containers"

setup(
    name="polaris-terminal",
    version=version,
    description="CLI tool for connecting to Polaris containers via terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Polaris Team",
    author_email="info@polaris.com",
    url="https://github.com/BANADDA/polaris-terminal",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0",
        "websockets>=10.0",
    ],
    entry_points={
        "console_scripts": [
            "polaris=polaris_terminal.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
) 