from distutils.core import setup
from os.path import join, dirname

import setuptools

import chirpstack

with open(join(dirname(__file__), 'requirements.txt'), 'r') as f:
    install_requires = f.read().split("\n")

setup(name='py-chirpstack',
      version=chirpstack.__version__,
      author=chirpstack.__author__,
      install_requires=install_requires,
      description=chirpstack.__doc__.strip(),
      python_requires='>=3.6',
      packages=setuptools.find_packages(),
      )
