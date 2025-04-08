from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pytrading212api",
    version="2025.4.4",
    description="Trading 212 api wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryanbdclark/pytrading212api",
    author="Ryan Clark",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="trading, 212, api, trading212",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=["aiohttp"],
)
