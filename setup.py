#!/usr/bin/env python
"""
sentry-pushover
==================

A Sentry plugin that sends notifications to a Pushover https://pushover.net.

Plugin modification: Adam Balachowski

License
-------
Copyright 2012 Janez Troha

This file is part of Sentry-Pushover.

Sentry-Pushover is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sentry-Pushover is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sentry-Pushover.  If not, see <http://www.gnu.org/licenses/>.

:copyright: (c) 2011 by the Sentry Team, see AUTHORS for more details.
:license: GNU General Public License, see LICENSE for more details.
"""
from setuptools import setup, find_packages

tests_require = [
    'nose',
]

install_requires = [
    'sentry>=6.3.0',
    'requests>=0.2.0',
    'simplejson'
]

setup(
    name='sentry-pushover',
    version='1.0.4',
    author='Janez Troha',
    author_email='janez.troha@gmail.com',
    url='https://github.com/Adam16/sentry-pushover',
    description='A Sentry plugin that integrates with pushover',
    long_description=__doc__,
    license='GPL',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'pushover = sentry_pushover',
        ],
        'sentry.plugins': [
            'pushover = sentry_pushover.plugin:PushoverPlugin'
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
