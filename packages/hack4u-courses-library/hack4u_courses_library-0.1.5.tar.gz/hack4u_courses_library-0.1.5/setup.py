from setuptools import find_packages, setup

# Leer el contenido del arhivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u-courses-library",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[],
    author="Juanhez",
    description="Libreria de prueba - Consultar los cursos de un modulo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)
