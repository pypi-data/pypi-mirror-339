# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LGPLv3
"""
A minimal setup script for Anthropogenic mw.

All the remaining configuration is in pyproject.toml.
"""
from setuptools import setup, find_packages

def current_version():
    changelog = open('CHANGELOG.md', 'r')
    changelog_items = changelog.readlines()
    version = "0.0.0"
    version_date = "2025-01-01"
    for item in changelog_items:
        if item.startswith("##"):
            pos = item.split();
            version = pos[1][1:]
            version_date = pos[3]
    return version, version_date

Version, VersionDate = current_version()

setup(
    name='amw',
    version=Version,
    date=VersionDate,
    description='Earthquake moment magnitude estimation from P, S or common P and S waves',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jan Wiszniowski',
    author_email='jwisz@igf.edu.pl',
    url='https://github.com/JanWiszniowski/amw',
    packages=find_packages(),
    install_requires=[
        'matplotlib>=3.9.2',
        'obspy>=1.2.0',
        'future>=1.0.0'
    ],
    license='GNU Lesser General Public License, Version 3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': ['spectral_mw = amw.mw.spectral_mw:main',
                            'view_green_fun = amw.mw.test_greens_function:main'],
    },
    keywords='seismology, moment magnitude, anthropogenic seismicity, near field, intermediate field',
)
