# -*- coding: utf-8 -*-
""" Information module, containing version variables, plus some
setuptools-related variables
Attributes
----------
version_major
version_minor
version_micro
version_extra
"""

from __future__ import absolute_import
import sys

version_major = 5
version_minor = 3
version_micro = 0
version_extra = ''
_version_major = version_major
_version_minor = version_minor
_version_micro = version_micro
_version_extra = version_extra

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
__version__ = "%s.%s.%s%s" % (version_major,
                              version_minor,
                              version_micro,
                              version_extra)
CLASSIFIERS = ["Development Status :: 5 - Production/Stable",
               "Environment :: Console",
               "Operating System :: OS Independent",
               "Programming Language :: Python :: 3.6",
               "Programming Language :: Python :: 3.7",
               "Programming Language :: Python :: 3.8",
               "Programming Language :: Python :: 3.9",
               "Programming Language :: Python :: 3.10",
               "Programming Language :: Python :: 3 :: Only",
               "Topic :: Scientific/Engineering",
               "Topic :: Utilities"]

description = 'soma-base'

long_description = """
=========
SOMA-BASE
=========

Miscellaneous all-purpose classes and functions in Python.

"""

# versions for dependencies
SPHINX_MIN_VERSION = '1.0'

# Main setup parameters
NAME = 'soma-base'
ORGANISATION = "Populse"
MAINTAINER = "Populse team"
MAINTAINER_EMAIL = "support@brainvisa.info"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/populse/soma-base"
DOWNLOAD_URL = "https://github.com/populse/soma-base"
LICENSE = "CeCILL-B"
CLASSIFIERS = CLASSIFIERS
AUTHOR = "Populse team"
AUTHOR_EMAIL = "support@brainvisa.info"
PLATFORMS = "OS Independent"
ISRELEASE = version_extra == ''
VERSION = __version__
PROVIDES = ["soma-base"]
REQUIRES = [
    "six >= 1.13",
    "numpy",
]
EXTRAS_REQUIRE = {
    "doc": ["sphinx>=%s" % SPHINX_MIN_VERSION],
    "crypto": ["pycrypto"],
    "controller": ["traits"],
    "subprocess": ["subprocess32;python_version<'3.2'"],
    "test_utils": ["argparse"],
}
