from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="five9-stats",
    version="0.1.0",
    author="Five9 Stats Library",
    author_email="james.smart@five9.com",
    description="Python client library for Five9 Statistics APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JamesSmart/five9-stats",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
        "pydantic>=1.9.0",
    ],
)