from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='cursomlet-package',
    version='1.0.0',
    packages=find_packages(),
    description='Um exemplo simples de biblioteca - curso Fiap Mlet',
    author='Artur Mata',
    author_email='arturrogerio@gmail.com',
    url='https://github.com/arfmatta/cursoMlet',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
