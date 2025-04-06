import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read_requirements(name):
    with open(os.path.join(here, name), encoding='utf-8') as f:
        require_str = f.read()
        return require_str.split()

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='open-image-cli',
    version='0.2.0',
    author='youngfreefjs',
    url='https://github.com/youngfreeFJS/imagecli',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=read_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'img=imagecli.cli:main',
        ],
    },
)
