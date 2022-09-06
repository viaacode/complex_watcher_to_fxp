#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:21:11 2022

@author: tina
"""

from setuptools import setup

setup(name='complex_watcher',
      version='v1.0.1',
      description='watchfolder for .complex',
      long_description='Publiseh fxp msg to rabbitmq.',
      classifiers=[
          'Development Status :: v1.0',
          'Intended Audience :: Developers',
          'License :: MIT 2020 Meemomo',
          'Programming Language :: Python :: 3.10',
          'Topic :: watchfolder',
      ],
      keywords='rabbitmq',
      author='Tina Cochet',
      author_email='tina.cochet@meemoo.be',
      license='MIT 2020 Meemoo',
      packages=['complex_watcher'],
      package_dir={'complex_watcher': 'complex_watcher'},
      install_requires=[
          'pika==1.1.0',
          'requests',
          'urllib3==1.26.12',
          'retry==0.9.2',
          'mako',
          'markdown >= 3.0',
          'inotify==0.2.9',
          'pytest==5.4.1',
          'pytest-cov==2.8.1',
          'lxml == 4.9.1'
      ],


      entry_points={
          'console_scripts': ['complex_watcher=complex_watcher.watcher:__main__'],
      }, include_package_data=True, zip_safe=False)
