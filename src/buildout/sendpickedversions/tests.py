# -*- coding: utf-8 -*-
"""
Generic Test case
"""
import os
import sys
import re
import unittest
import doctest
import zc.buildout.testing
import pkg_resources
from zope.testing import renormalizing

normalize_version1 = (re.compile('= [0-9a-zA-Z -_]+([.][0-9a-zA-Z-_]+)+'), '= N.N')  # noqa
normalize_version2 = (re.compile('(#[^ ]*?) [0-9a-zA-Z -_]+([.][0-9a-zA-Z-_]+)+'), '\\1 N.N')  # noqa


def test_suite():
    globs = globals()
    dist = pkg_resources.get_distribution('buildout.sendpickedversions')
    os.environ['PYTHONPATH'] = '{}:{}'.format(
        os.environ.get('PYTHONPATH') or dist.location,
        dist.location
    )

    flags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
             doctest.REPORT_ONLY_FIRST_FAILURE)

    test_dir = os.path.abspath(os.path.dirname(__file__))
    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)

    doctest_dir = test_dir

    # filtering files on extension
    docs = [os.path.join(doctest_dir, doc) for doc in
            os.listdir(doctest_dir) if doc.endswith('.txt')]

    suite = []
    for test in docs:
        suite.append(doctest.DocFileSuite(
            test, optionflags=flags,
            globs=globs,
            setUp=zc.buildout.testing.buildoutSetUp,
            tearDown=zc.buildout.testing.buildoutTearDown,
            checker=renormalizing.RENormalizing([normalize_version1,
                                                 normalize_version2]),
            module_relative=False
        ))

    return unittest.TestSuite(suite)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
