from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ncc_cursofiap-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib ncc_cursofiap',
    author='Robson Nicácio',
    author_email='robson.nicacio@gmail.com',
    url='https://github.com/tadrianonet/ncc_cursofiap',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
