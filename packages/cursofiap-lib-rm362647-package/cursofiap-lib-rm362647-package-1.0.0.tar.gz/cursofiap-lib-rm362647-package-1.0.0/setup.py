from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='cursofiap-lib-rm362647-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib cursofiap-lib-rm362647',
    author='Ailton Pardócimo Jr',
    author_email='jpardocimo@gmail.com',
    url='https://github.com/jpardocimo/cursofiap-lib-rm362647',
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
