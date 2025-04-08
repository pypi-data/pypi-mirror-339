# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='litepolis-database-example',                                     # Change
    version="0.0.2",                                                       # Change
    description='The database module for LitePolis',                       # Change
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Your name',                                                    # Change
    # author_email='Optional',                                             # Change
    url='https://github.com/NewJerseyStyle/LitePolis-database-example',    # Change
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['litepolis', 'sqlmodel'],
)
