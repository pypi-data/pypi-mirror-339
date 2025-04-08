# setup.py

from setuptools import setup, find_packages

setup(
    name='StatOmics',
    version=0.4,
    author="Nathan Li",
    url="https://github.com/nathanxli/StatOmics",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rpy2",
        "pathlib"
    ],
)

