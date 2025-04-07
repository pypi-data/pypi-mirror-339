from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='investpy-mptrivelato',
    version='1.0.0',
    packages=find_packages(),
    description='Biblioteca com funções de calculos de investimento,',
    author='MpTrivelato',
    author_email='mp.trivelato@gmail.com ',
    url='https://github.com/marcostrivelato/Hands-on/investpy',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)