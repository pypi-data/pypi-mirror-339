from setuptools import setup 

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='restaurante-sabor-express',
    version='0.0.1',
    license='MIT License',
    author='Gabriela Rodrigues Campanha',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='gabrielarcampanha@gmail.com.br',
    keywords='restaurante, sabor, express',
    description=u'biblioteca para gerenciar restaurantes',
    packages=['sabor_express'],)