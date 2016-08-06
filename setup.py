#!/usr/local/bin/python3
# setup.py for planar
#
import os
from setuptools import setup, find_packages

srcdir = os.path.dirname(__file__)


def read(fname):
    return open(os.path.join(srcdir, fname)).read()

long_description = ''
if os.path.exists('README.txt'):
    long_description = read('README.txt')

setup(
    name='pygonal',
    version='0.1.0',  # *** REMEMBER TO UPDATE __init__.py ***
    author='Rezart Qelibari',
    author_email='qelibarr@informatik.uni-freiburg.de',
    url='https://github.com/rqelibari/pygonal',
    description='A 2D planar geometry library for Python.',
    long_description=long_description,
    download_url='https://github.com/rqelibari/pygonal/archive/master.zip',
    provides=['pygonal'],
    license='Apache 2.0',
    packages=find_packages(),
    keywords='2d planar geometry',
    install_requires=[],
    extras_require={'dev': ['pep8>=1.7.0']},
    test_suite="pygonal.tests",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Operating System :: MacOS :: MacOS X'
    ]
)
