#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author="Thomas",
    author_email='substantialimpulse@pm.me',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python tool for extracting Visual Fox Pro DBF (database files) of the REIMS project.",
    entry_points={
        'console_scripts': [
            'reims_dbf_extractor=reims_dbf_extractor.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme,
    include_package_data=True,
    keywords='reims_dbf_extractor',
    name='reims_dbf_extractor',
    packages=find_packages(include=['reims_dbf_extractor', 'reims_dbf_extractor.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/l3d00m/reims_dbf_extractor',
    version='0.1.0',
    zip_safe=False,
)
