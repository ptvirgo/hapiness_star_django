import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as readme:
    README = readme.read()

setup(
    name='happiness_star',
    description='Django app for tracking life satisfaction or happiness',
    long_description=README,
    version='0.2.1',
    author='Pablo Virgo',
    author_email='mailbox@pablovirgo.com',
    packages=find_packages()
)
