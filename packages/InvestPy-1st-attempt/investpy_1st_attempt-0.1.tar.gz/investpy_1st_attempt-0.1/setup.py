# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 14:33:47 2025

@author: josea
"""

from setuptools import setup, find_packages

setup(
   name='InvestPy-1st-attempt',
   version='0.1',
   packages=find_packages(),
   install_requires=[],
   author='José Augusto Devienne',
   author_email='joseaugusto.devienne@gmail.com',
   description='Uma biblioteca para cálculos de investimentos (Material curso FIAP 2025).',
   url='https://github.com/devienne/Machine-Learning-Engineering',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
)