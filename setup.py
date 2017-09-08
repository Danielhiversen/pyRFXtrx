'''
This file is part of pyRFXtrx, a Python library to communicate with
the RFXtrx family of devices from http://www.rfxcom.com/
See https://github.com/Danielhiversen/pyRFXtrx for the latest version.

Copyright (C) 2012  Edwin Woudt <edwin@woudt.nl>

pyRFXtrx is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyRFXtrx is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyRFXtrx.  See the file COPYING.txt in the distribution.
If not, see <http://www.gnu.org/licenses/>.
'''

from setuptools import setup

setup(
    name = 'pyRFXtrx',
    packages = ['RFXtrx'],
    install_requires=['pyserial>=2.7'],
    version = '0.20.1',
    description = 'a library to communicate with the RFXtrx family of devices',
    author='Edwin Woudt',
    author_email='edwin@woudt.nl',
    url='https://github.com/Danielhiversen/pyRFXtrx',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ' +
            'GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
)
