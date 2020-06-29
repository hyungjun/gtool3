#!/usr/bin/env python

from distutils.core import setup

setup( name                 = 'gtool3',
       version              = '0.6',
       description          = 'gtool io sub module of coreFrame',
       author               = 'Hyungjun Kim',
       author_email         = 'hyungjun@gmail.com',
       url                  = '',
       package_dir          = {'gtool3':'./'},
       packages             = ['gtool3'],
       install_requires     = ['numpy'],
      )
