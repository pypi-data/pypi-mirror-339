from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='helloworld-test-fiap-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib helloworld',
    author='seu nome',
    author_email='joaogabriel1598@gmail.com',
    url='https://github.com/gabrieljoaooo5/helloworld',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
