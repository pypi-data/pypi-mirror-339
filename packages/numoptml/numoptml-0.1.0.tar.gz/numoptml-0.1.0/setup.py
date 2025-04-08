from setuptools import setup, find_packages

setup(
    name='numoptml',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    author='Егор',
    description='Библиотека численных методов для оптимизации в ML',
    python_requires='>=3.7',
)
