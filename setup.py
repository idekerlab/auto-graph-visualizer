# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='auto-graph-visualizer',
    version='0.1.0',
    description='Automatic graph visualization package',
    long_description=readme,
    author='',
    author_email='',
    url='https://github.com/idekerlab/auto-graph-visualizer',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        "console_scripts": [
            "agviz=auto_graph_visualizer.core:main",
        ]
    }
)
