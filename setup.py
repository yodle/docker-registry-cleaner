"""Setuptools based setup module for Docker Registry Cleaner
   https://github.com/yodle/Docker-Registry-Cleaner"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='docker-registry-cleaner',

    version='0.1.1',

    description='A tool to remove unused images from a Docker registry',
    long_description=long_description,

    url='https://github.com/yodle/Docker-Registry-Cleaner',

    author='John Downs',
    author_email='john.downs@yodle.com',
    license='Apache 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='docker docker-registry',

    packages=find_packages(exclude=['test']),
    install_requires=[],
    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={},


    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'docker_registry_cleaner=cleaner.__main__:main',
        ],
    },
)
