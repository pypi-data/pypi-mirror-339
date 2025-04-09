# Script para instalar la librería
from setuptools import setup, find_packages

setup(
    name="matlab2pythonlib",
    version="0.2.7",
    packages=find_packages(),
    install_requires=[],
    author="BelloDev",
    author_email="fernandojbf123@gmail.com",
    description="Esta librería contiene funciones que permiten la conversión de fechas de formato MATLAB (datenum) al formato datetime de python. También contiene funciones para crear array de tiempo o convertir fácilmente fechas de formato datetime a datestr",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Fernandojbf123/MATLAB2PYTHONLIB",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)