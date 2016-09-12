#!/usr/bin/env python

from subprocess import call
from sys import exit, version_info

from setuptools import Command, find_packages, setup
from grepg import __version__ as version

setup(
    name = 'grepg',
    version = version,
    description = 'GrepPage Command Line Client',
    url = 'https://github.com/evidanary/grepg-python',
    packages = find_packages(),
    include_package_data = True,

    # Author information:
    author = 'Yash Ranadive',
    author_email = 'yash@greppage.com',

    # Metadata:
    keywords = ['greppage', 'client', 'cli'],
    license = 'MIT',
    install_requires = [
        'PyYAML==3.12',
        'termcolor==1.1.0',
    ],
    extras_require = {
    },
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Environment :: Console',
        'Intended Audience :: Developers',
    ],

    # Script information:
    entry_points = {
        'console_scripts': [
            'grepg = grepg.main:main'
        ]
    },
)
