'''
Created on Aug 15, 2013

@author: Alejandro Riveros Cruz <lariverosc@gmail.com>
'''

from setuptools import setup, find_packages

setup(
    name='elibom',
    version='1.2',
    description='Elibom API Python Client v1.2',
    author='Alejandro Riveros Cruz',
    author_email='lariverosc@gmail.com',
    url='http://www.elibom.com',
    packages=find_packages(),
    install_requires = ['requests>=1.1.0'],
    test_suite = 'tests.ClientTests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7'
    ]
)
