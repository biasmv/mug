#!/usr/bin/env python

from distutils.core import setup

setup(name='mug',
    version='0.1',
    description='mug --- manage multiple git repositories at once',
    author='Marco Biasini',
    author_email='mvbiasini@gmail.com',
    install_requires = ['pygit2>=0.21'],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
    ],
    entry_points={
        'console_scripts' : [ 'mug = mug.main:main' ]
    },
    packages=[ 'mug', 'mug.verbs' ],
)
