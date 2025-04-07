from setuptools import setup, find_packages

setup(
    name="pipswl",  # Cambia el nombre aquí
    version="1.0.0",
    description="Steam Workshop Download List",
    author="lesUchiha",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
)
