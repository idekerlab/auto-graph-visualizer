# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()


def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

# Add importlib for older versions
install_requires = read_requirements()
if sys.version_info[:2] < (3, 7):
    install_requires.append("importlib_resources")

setup(
    name='auto-graph-visualizer',
    version='0.1.0',
    description='Automatic graph visualization package',
    long_description=readme,
    author='Mikio Shiga, Atsuya Matsubara',
    author_email='m-shiga@ist.osaka-u.ac.jp, at-matbr@ist.osaka-u.ac.jp',
    url='https://github.com/idekerlab/auto-graph-visualizer',
    install_requires=install_requires,
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    # packages=['auto_graph_visualizer'],
    package_data={'': ['*.json']},
    entry_points={
        "console_scripts": [
            "agviz=auto_graph_visualizer.core:main",
        ]
    },
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    )
)
