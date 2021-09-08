# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 09:17:14 2021

@author: макс
"""

from setuptools import setup
import subprocess

setup(
    install_requires=['requests', 'wheel'],
)

subprocess.run('python -m pip install 2captcha-python', shell=True)
