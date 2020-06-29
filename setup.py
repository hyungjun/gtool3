#!/usr/bin/env python

from distutils.core import setup

setup( name                 = 'gtool3',
       version              = '0.6a',
       description          = 'gtool io sub module of coreFrame',
       long_description     = ''' long_description to be written. ''',
       classifiers          = [
                            'Development Status :: 4 - Beta',
                            'License :: OSI Approved :: MIT License',
                            'Programming Language :: Python :: 2.7',
                            'Topic :: Scientific/Engineering :: Atmospheric Science',
                            ],
       keywords             = 'gtool miroc matsiro',
       url                  = 'https://github.com/hyungjun/gtool3',
       author               = 'Hyungjun Kim',
       author_email         = 'hyungjun@gmail.com',
       license              = 'MIT',

       package_dir          = {'gtool3/gtool3':''},
       packages             = ['gtool3', 'gtool3/filters'],
      )

