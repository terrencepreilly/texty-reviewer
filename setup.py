from setuptools import setup, find_packages
from glob import glob
from os import path

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='texty',
    version='1.0',
    description='Textbook reviewing utility.',
    long_description=readme,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[path.splitext(path.basename(i))[0] for i in glob('src/*.py')],
    entry_points={
        'console_scripts': [
            'texty = texty.UpdateProblems:_main',
        ],
    },
)
