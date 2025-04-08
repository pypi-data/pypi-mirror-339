from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pinit-pkg",  # Cambia esto por el nombre de tu paquete
    version="0.1.002",
    author="Eduardo Cifuentes",
    author_email="eduardo.cifuentes@bigsmart.mx",
    description="Paquete de utilidades para el servicio de clusterizado.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "loguru>=0.7.3",
    ],
)
