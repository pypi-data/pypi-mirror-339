#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='distcrab',
    version='0.0.65',
    long_description=(Path(__file__).parent / 'readme.md').read_text(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        '': ['**/*.*']
    },
    install_requires=[
        'asyncssh',
        'aiodav',
        'aiofile',
        'aiostream',
        'gpg',
        'humanize',
        'dnspython',
        'GitPython',
        'httpx',
        'pyOpenSSL',
    ]
)
