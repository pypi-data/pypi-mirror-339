from setuptools import setup, find_packages

setup(
    name="pipswl",
    version="1.3.0",
    description="Steam Workshop Download List",
    author="lesUchiha",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm"
    ],
)
