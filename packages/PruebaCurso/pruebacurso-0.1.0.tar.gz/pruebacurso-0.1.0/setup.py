from setuptools import setup, find_packages

# Hay que leer el contenido README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="PruebaCurso",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Off_Klix",
    description="Biblioteca para consultar cursos de hack4u a modo de aprendizaje",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)
