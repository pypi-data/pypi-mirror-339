from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='curso-fiap-package-santerio',
    version='1.0.0',
    packages=find_packages(),
    description='curso-fiap-hello-word',
    author='santeriogouveia',
    author_email='santerioj@gmail.com',
    url='https://github.com/santerioj/curso-fiap',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
