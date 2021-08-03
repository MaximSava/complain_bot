# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 09:17:14 2021

@author: макс
"""

from setuptools import setup

setup(
    install_requires=['requests', 'wheel'],
)

import subprocess

subprocess.run('python -m pip install 2captcha-python', shell=True)