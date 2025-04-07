from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='handson-parte1-package',
    version='1.0.0',
    packages=find_packages(),
    description='Lib construida como exercício',
    author='Marcos Trivelato',
    author_email='mp.trivelato@gmail.com ',
    url='https://github.com/tadrianonet/handson-parte1',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
