#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pulpcore-plugin>=0.1.0b7',
    'PyOpenSSL',
]


setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Pulp Team",
    author_email='pulp-list@redhat.com',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Pulp plugin that provides X.509 ba",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pulp_certguard',
    name='pulp_certguard',
    packages=find_packages(include=['pulp_certguard']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/pulp/pulp_certguard',
    version='0.1.0',
    zip_safe=False,
    entry_points={
        'pulpcore.plugin': [
            'certguard = pulp_certguard:default_app_config',
        ]
    }

)
