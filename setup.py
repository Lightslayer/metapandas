#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import configparser
import datetime

setup_kwargs = {}

from setuptools import find_packages, setup

try:
    import pbr

    setup_kwargs['pbr'] = True
except ImportError:
    setup_kwargs['pbr'] = False

here = os.path.abspath(os.path.dirname(__file__))
basename = os.path.basename(os.path.dirname(__file__))

# give a list of scripts and how they map to a package module
CONSOLE_SCRIPTS = []

# load config using parser
parser = configparser.ConfigParser()
parser.read('%s/setup.cfg' % here)

# add setup.cfg information back from metadata
try:
    from setuptools.config import read_configuration

    config = read_configuration('%s/setup.cfg' % here)
    metadata = config['metadata']
    metadata['summary'] = metadata.get('summary', metadata['description'].split('\n')[0])
    if setup_kwargs.pop('pbr', False) is not True:
        setup_kwargs.update(metadata)
        install_requirements = [line.split('#')[0].strip(' ')
                                for line in open('%s/requirements.txt' % here).readlines()
                                if line and line.split('#')[0]]

        # explicitly compile a master list of install requirements - workaround for bug with PBR & bdist_wheel 
        setup_kwargs['install_requires'] = list(set(list(setup_kwargs.get('install_requires',
                                                                        config.get('options', {})
                                                                                .get('install_requires', []))) +
                                                    install_requirements))
except ImportError:
    metadata = {}

# update with further information for sphinx
metadata.update(parser['metadata'])

if __name__ == '__main__':
    # actually perform setup here
    setup(
        setup_requires=['pbr', 'setuptools'],
        packages=find_packages(),
        entry_points={
            'console_scripts': CONSOLE_SCRIPTS
        },
        tests_require=['pytest', 'coverage'],
        include_package_data=True,
        **setup_kwargs
    )
