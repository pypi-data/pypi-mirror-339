from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='projeto1-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib projeto1',
    author='Pedro Ulisses',
    author_email='ulissesph@gmail.com',
    url='https://github.com/ordepzero/projeto1',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
