# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages


setup(
    name='buildout.sendpickedversions',
    version=open('VERSION').read().strip(),
    description='Sends picked packages and versions to a whiskers server.',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGELOG.rst').read()),
    classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    license='GPL2',
    keywords='buildout extension send picked versions',
    author='Jukka Ojaniemi',
    author_email='jukka.ojaniemi@jyu.fi',
    url='http://github.com/pingviini/buildout.sendpickedversions',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['buildout'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout',
        'requests',
    ] + (int(sys.version[0]) == 2 and
         int(sys.version[2]) < 7 and
         ['simplejson'] or
         []),
    tests_require=[
        'zc.buildout',
        'zc.recipe.egg',
        'zope.testing',
    ],
    test_suite='buildout.sendpickedversions.tests.test_suite',
    extras_require={
        'tests': [
            'zc.buildout',
            'zc.recipe.egg',
            'zope.testing',
        ]
    },
    entry_points={
        'zc.buildout.extension': [
            'default = buildout.sendpickedversions:install'
        ]
    }
)
