import os

from setuptools import find_packages, setup

# Read version from __init__.py
with open(os.path.join('payler_sdk', '__init__.py'), 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"\'')
            break

# Read long description from README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="payler-sdk",
    version=version,
    description="Python SDK for integration with the Payler payment system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mdigital",
    author_email="ulukmanmuratov@gmail.com",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0,<3.0.0",
    ],
    keywords="payler, payment, api, sdk",
)
