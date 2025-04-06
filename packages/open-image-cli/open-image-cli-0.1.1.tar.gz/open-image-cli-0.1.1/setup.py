import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read_requirements(name):
    with open(os.path.join(here, name), encoding='utf-8') as f:
        require_str = f.read()
        return require_str.split()

setup(
    name='open-image-cli',
    version='0.1.1',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'img=imagecli.cli:main',
        ],
    },
)
