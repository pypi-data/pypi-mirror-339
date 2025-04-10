from setuptools import setup, find_packages
setup(
    name='DATAx-ETL',
    version='0.0.7',
    author='Almir J Gomes',
    author_email='almir.jg@hotmail.com',
    packages=find_packages(),
    install_requires=[],
    python_requeries=">=3.9",
    description="DATAx-Projeto de ETL",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/DE-DATAx/DAX_DB.git',
)