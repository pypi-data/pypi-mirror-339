from setuptools import setup
with open("README.md", "r") as arq:
    readme = arq.read()
    
setup(name='upxd_functions',
    version='0.3',
    license='MIT License',
    author='Tork9023',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='Tork9023@gmail.com',
    keywords='UPX',
    description=u'Funções baseadas no uso diário para teste de criação de biblioteca',
    packages=['upxd'],
    install_requires=['google-generativeai'])