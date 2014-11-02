#!/usr/bin/env python

from distutils.core import setup

setup(name='mug',
      version='0.1',
      description='mug --- manage multiple git repositories at once',
      author='Marco Biasini',
      author_email='mvbiasini@gmail.com',
      packages=[ 'mug', 'mug.verbs' ],
)
