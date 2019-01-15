#!/usr/bin/env python3

from setuptools import setup, find_packages

requirements = [
    'aiohttp',
    'pulpcore-plugin>=0.1.0b7',
    'PyOpenSSL',
]

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='pulp-certguard',
    version='0.0.1a1',
    description='Certificate content guard plugin for the Pulp Project',
    long_description=long_description,
    license='GPLv2+',
    author='Pulp Project Developers',
    author_email='pulp-dev@redhat.com',
    url='http://www.pulpproject.org/',
    python_requires='>=3.6',
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(exclude=['test']),
    classifiers=(
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
    entry_points={
        'pulpcore.plugin': [
            'certguard = pulp_certguard:default_app_config',
        ]
    }
)
