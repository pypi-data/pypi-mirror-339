# setup.py
from setuptools import setup, find_packages

with open("README_pypi.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="rainrunoff",
    version="0.0.1",
    description="A simple daily rainfall-runoff model",
    #long_description part is for pypi
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Gokhan Cuceloglu",
    author_email="cucelog@example.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "geopandas",
        "rasterio",
        "pyproj",
        "scipy"
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Hydrology",
    ],
    python_requires=">=3.8",
)
