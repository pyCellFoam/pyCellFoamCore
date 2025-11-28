#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setup.py for pyCellFoamCore

A Python library that implements the Cell Method to simulate heat transfer
on open cell foams.
"""

from setuptools import setup, find_packages
import os


# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''


# Package metadata
setup(
    name='pyCellFoamCore',
    version='0.1.0',
    author='TUM Chair of Automatic Control & LAGEPP',
    author_email='',
    description=(
        'A Python library implementing the Cell Method to simulate '
        'heat transfer on open cell foams'
    ),
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/pyCellFoam/pyCellFoamCore',
    project_urls={
        'Bug Tracker': 'https://github.com/pyCellFoam/pyCellFoamCore/issues',
        'Documentation': 'https://github.com/pyCellFoam/pyCellFoamCore',
        'Source Code': 'https://github.com/pyCellFoam/pyCellFoamCore',
    },
    packages=find_packages(exclude=['doc', 'tutorial', 'unittests', 'img']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy',
        'matplotlib',
        'tabulate',
    ],
    extras_require={
        'dev': [
            'sphinx',
            'sphinxcontrib-fulltoc',
            'sphinx-autodoc-typehints',
            'pytest',
        ],
        'viz': [
            'vtk',
        ],
        'video': [
            'ffmpeg-python',
        ],
    },
    keywords=(
        'cell method, heat transfer, open cell foam, simulation, '
        'finite volume'
    ),
    license='GPL-3.0',
    include_package_data=True,
    zip_safe=False,
)
