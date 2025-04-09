from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dio_osny_processamento_imagem",
    version="0.0.1",
    author="Osny MSN",
    author_email="osnynt@gmail.com",
    description="Processamento de imagens com Python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OsnyNeto/Programas_Python/tree/main/dio_osny_processamento_imagem",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)