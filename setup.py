# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import sys


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements


setup(
    name='auto-graph-visualizer',
    version='0.1.0',
    description='Automatic graph visualization package',
    long_description=readme,
    author='Mikio Shiga, Atsuya Matsubara',
    author_email='m-shiga@ist.osaka-u.ac.jp, at-matbr@ist.osaka-u.ac.jp',
    url='https://github.com/idekerlab/auto-graph-visualizer',
    install_requires=read_requirements(),
    license=license,
    #packages=find_packages(exclude=('tests', 'docs')),
    packages=['auto_graph_visualizer'],
    package_data={'auto_graph_visualizer': ['cy_visual.json']},
    entry_points={
        "console_scripts": [
            "agviz=auto_graph_visualizer.core:main",
        ]
    }
)
