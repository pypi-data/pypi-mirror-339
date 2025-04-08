from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='numoptml',
    version='0.1.1',
    packages=find_packages(),
    install_requires=['numpy'],
    author='Егор',
    description='Численные методы оптимизации для машинного обучения и автоматизации ИИ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
)
