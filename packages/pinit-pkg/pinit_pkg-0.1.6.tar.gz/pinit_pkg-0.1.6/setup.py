from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pinit-pkg",
    version="0.1.6",
    author="Eduardo Cifuentes",
    author_email="eduardo.cifuentes@bigsmart.mx",
    description="Paquete de utilidades para el servicio de clusterizado.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["pinit_pkg"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "loguru>=0.7.3",
        "pydantic>=2.10.6",
    ],
)
