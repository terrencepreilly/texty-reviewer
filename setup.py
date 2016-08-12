"""Allow the user to install with setup or pip."""
from os import path
from glob import glob
from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    README = f.read()

setup(
    name='texty',
    version='1.0',
    data_files=[('src', ['src/texty/parser_arguments.json']),],
    description='Textbook reviewing utility.',
    long_description=README,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[path.splitext(path.basename(i))[0] for i in glob('src/*.py')],
    entry_points={
        'console_scripts': [
            'texty = texty.UpdateProblems:_main',
        ],
    },
)
