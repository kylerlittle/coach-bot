# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='coach-bot',
    version='0.1.0',
    description='A personal coach bot for people who want to work out, eat better, and live healthier',
    long_description=readme,
    author='Chris Young, Connor Wright, Kelsey Nash, Kyler Little, Lucy Tran, Shusanta Bhattarai',
    author_email='kyler.little@wsu.edu',
    url='https://gitlab.eecs.wsu.edu/cpts422/coach-bot',
    license=license,
    packages=find_packages(exclude=('tests'))
)
