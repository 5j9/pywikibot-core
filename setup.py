# -*- coding: utf-8 -*-
"""Installer script for Pywikibot 3.0 framework."""
#
# (C) Pywikibot team, 2009-2018
#
# Distributed under the terms of the MIT license.
#
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import sys

from setuptools import find_packages, setup

if sys.version_info[:3] < (2, 7, 4):
    try:
        # Work around a traceback on Python < 2.7.4
        # http://bugs.python.org/issue15881#msg170215
        import multiprocessing
    except ImportError:
        pass
    else:
        _unused = multiprocessing  # pyflakes workaround


PYTHON_VERSION = sys.version_info[:3]
PY2 = (PYTHON_VERSION[0] == 2)

versions_required_message = """
Pywikibot is not available on:
{version}

This version of Pywikibot only supports Python 2.7.2+ or 3.4+.
"""


def python_is_supported():
    """Check that Python is supported."""
    # Any change to this must be copied to pwb.py
    return PYTHON_VERSION >= (3, 4, 0) or PY2 and PYTHON_VERSION >= (2, 7, 2)


if not python_is_supported():
    raise RuntimeError(versions_required_message.format(version=sys.version))

# ============
# Dependencies
# ============
# It is good practise to install packages using the system
# package manager if it has a packaged version. If you are unsure,
# please use pip.
#
# To get a list of potential matches, on some Linux distributions
# you can use:
#
# $ awk -F '[#>=]' '{print $1}' setup.py | xargs yum search
#     or
# $ awk -F '[#>=]' '{print $1}' setup.py | xargs apt-cache search
#
# Some dependencies can be found also in tox.ini.

# Extra dependencies
# ==================
# Core library dependencies.
#
# Extra dependencies can be installed using
# $ pip install -e .[extras]
#
# It is organised so that simple requirements are processed first,
# and more difficult packages are last. All dependencies
# other than requests are optional.
extra_deps = {
    'requests': ['requests >= 2.9, != 2.18.2'],
    # requests security extra
    'security': ['requests[security]', 'pycparser != 2.14'],
    # OAuth support
    # mwoauth 0.2.4 is needed because it supports getting identity
    # information about the user.
    'mwoauth': ['mwoauth >= 0.2.4, != 0.3.1'],
    'pydot': ['pydot >= 1.0.28'],
    # csv is needed other unittest fails to load tests
    'csv': ['unicodecsv; python_version < "3"'],
    'stdnum': ['python-stdnum'],
    'pillow': ['Pillow'],
    'google': ['google >= 1.7'],
    'sseclient': ['sseclient >= 0.0.18'],
    # for incomplete component botirc
    'irc': ['irc'],
    'mwparserfromhell': ['mwparserfromhell >= 0.3.3'],
    # The MySQL generator in pagegenerators depends on either PyMySQL
    # or MySQLdb. Pywikibot prefers PyMySQL
    # over MySQLdb (Python 2 only).
    'mysql': ['PyMySQL'],
    # HTML comparison parser in diff module
    'beautifulsoup': ['BeautifulSoup4']
}

# Scripts dependencies
# ====================
# Scripts dependencies can be installed using
# $ pip install -e .[scripts]
scripts_deps = {
    'data_ingestion': extra_deps['csv'],
    'flickrripper': ['flickrapi'] + extra_deps['pillow'],
    'imageharvest': extra_deps['beautifulsoup'],
    'isbn': extra_deps['stdnum'],
    'match_images': extra_deps['pillow'],
    'patrol': extra_deps['mwparserfromhell'],
    'script_wui': ['crontab'] + extra_deps['irc'],
    'states_redirect': ['pycountry'],
    'weblinkchecker': ['memento_client >= 0.5.1, != 0.6.0']
}
extra_deps.update(scripts_deps)
extra_deps_list = [i for k, v in extra_deps.items() for i in v]
extra_deps.update({'extras': extra_deps_list})
extra_deps.update({'scripts': [i for k, v in scripts_deps.items() for i in v]})


# Mandatory dependencies
# ======================
dependencies = [
    # bug fixes for HTMLParser
    'future >= 0.15; python_full_version == "2.7.2"',
    # tools.ip does not have a hard dependency on an IP address module,
    # as it falls back to using regexes if one is not available.
    # The functional backport of py3 ipaddress is acceptable:
    # https://pypi.org/project/ipaddress
    # However the Debian package python-ipaddr is also supported:
    # https://pypi.org/project/ipaddr
    # Other backports are likely broken.
    # ipaddr 2.1.10+ is distributed with Debian and Fedora. See T105443.
    'ipaddr >= 2.1.10; python_version < "3"'
]
# requests is mandatory; see README.conversion.txt
dependencies += extra_deps['requests']

# Python versions before 2.7.9 will cause urllib3 to trigger
# InsecurePlatformWarning warnings for all HTTPS requests.
# By installing with security extras, requests will automatically
# set them up and the warnings will stop. See
# <https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning>
# for more details. There is no secure version of cryptography
# for Python 2.7.6 or older. See also bug T105767
# on Python 2.7 release 9+.
dependencies += [dep + '; python_full_version > "2.7.6" '
                 'and python_full_version < "2.7.9"'
                 for dep in extra_deps['security']]

# Pywikibot prefers using the inbuilt bz2 module if Python was compiled
# with bz2 support. But if it wasn't, bz2file is used instead.
try:
    import bz2
except ImportError:
    # Use bz2file if the Python is not compiled with bz2 support.
    dependencies.append('bz2file')
else:
    _unused = bz2


# Development dependencies
# ========================
# Development dependencies can be installed using
# $ pip install -e .[devel]
devel_deps = {
    'unittest2': ['unittest2 == 0.8.0; python_full_version == "2.7.2"'],
    'pytest': [
        'pytest >= 3.6',
        'pytest-timeout',
        'pytest-runner',
        'pytest-cov',
        'pytest-attrib >= 0.1.3',
        'pytest-httpbin'
    ],
    'nose': ['nose'],
    # six is needed other unittest fails to load tests
    'six': ['six; python_version >= "3"'],
    'mock': ['mock; python_version < "3"'],
    'nose-detecthttp': ['nose-detecthttp >= 0.1.3'],
    'nosetrim': ['nosetrim'],
    'pep257': ['pep257 >= 0.6'],
    'pyflakes': ['pyflakes >= 1.1'],
    'flake8': [  # due to incompatibilities between packages the order matters
        'flake8 >= 3.0.2',
        'pydocstyle',
        'hacking',
        'flake8-coding',
        'flake8-comprehensions',
        'flake8-docstrings >= 1.1',
        'flake8-future-import',
        'flake8-invalid-escape-sequences',
        'flake8-mock >= 0.3',
        'flake8-per-file-ignores',
        'flake8-print >= 2.0.1',
        'flake8-quotes',
        'flake8-string-format',
        'flake8-tuple >= 0.2.8',
        'pep8-naming >= 0.7'
    ],
    'coverage': ['codecov', 'coverage'],
    'unidiff': ['unidiff']
}
devel_deps.update({'devel': [i for k, v in devel_deps.items() for i in v]})


# Tox dependencies
# ================
tox_deps = {
    # diff-checker
    'diff-checker': devel_deps['unidiff'],
    # pyflakes
    'pyflakes': ['findx >= 0.9.9'] + devel_deps['pyflakes'],
    # flake8
    'flake8': devel_deps['flake8'] + devel_deps['pyflakes'],
    # nose
    'nose': (devel_deps['nose'] + devel_deps['nose-detecthttp']
             + extra_deps['csv'] + devel_deps['mock']),
    # nose34
    'nose34': (extra_deps['mwparserfromhell'] + extra_deps['beautifulsoup']
               + devel_deps['nose'] + devel_deps['nose-detecthttp']
               + devel_deps['six'] + devel_deps['mock']),
    # doctest
    'doctest': devel_deps['nose'] + devel_deps['six'],
    # doc
    'docs': extra_deps['scripts'] + devel_deps['unidiff'] + extra_deps['mysql']
}


# Test dependencies
# =================
test_deps = devel_deps['mock'] + devel_deps['six'] + extra_deps['csv']

# pywinauto >= 0.4.2 which depends on pywin32 are Win32 UI
# test dependencies that are quite expensive to install,
# and they are not useful on the Appveyor Win32 builds
# since the relevant ui_tests also require accessing the menu
# of the console window to set the console font and copy and paste,
# which doesn't exist in the Appveyor environment.
# These tests may be disabled also because pywin32 depends on VC++.
# Microsoft makes available a compiler for Python 2.7:
# http://www.microsoft.com/en-au/download/details.aspx?id=44266
if os.name == 'nt' and os.environ.get('PYSETUP_TEST_NO_UI', '0') != '1':
    test_deps += ['pywin32', 'pywinauto >= 0.4.2']

# Add all dependencies as test dependencies, so all scripts
# can be compiled for script_tests, etc.
if 'PYSETUP_TEST_EXTRAS' in os.environ:
    test_deps += extra_deps_list.remove('requests[security]')


extra_deps.update(devel_deps)
extra_deps.update(tox_deps)


# Dependency links
# ================
# The main pywin32 repository contains a Python 2 only setup.py
# with a small wrapper setup3.py for Python 3.
# http://pywin32.hg.sourceforge.net:8000/hgroot/pywin32/pywin32
# The main pywinauto repository doesn't support Python 3.
# The repositories used below have a Python 3 compliant setup.py.
dependency_links = [
    'git+https://github.com/nlhepler/pydot#egg=pydot',
    'git+https://github.com/jayvdb/nosetrim@py3#egg=nosetrim',
    'hg+https://bitbucket.org/TJG/pywin32#egg=pywin32',
    'git+https://github.com/vasily-v-ryabov/pywinauto-64#egg=pywinauto'
]


if PYTHON_VERSION == (2, 7, 2):
    # work around distutils hardcoded unittest dependency
    # work around T106512
    import unittest
    _unused = unittest
    if 'test' in sys.argv:
        import unittest2
        sys.modules['unittest'] = unittest2


def get_version():
    """Get a valid Pywikibot module version string."""
    version = '3.0'
    try:
        import subprocess
        date = subprocess.check_output(
            ['git', 'log', '-1', '--format=%ci']).strip()
        date = date.decode().split(' ')[0].replace('-', '')
        version += '.' + date
        if 'sdist' not in sys.argv:
            version += '.dev0'
    except Exception as e:
        print(e)
        version += '.dev0'
    return version


def read_desc(filename):
    """Read long description.

    Combine included restructured text files which must be done before
    uploading because the source isn't available after creating the package.
    """
    desc = []
    with open(filename) as f:
        for line in f:
            if line.strip().startswith('.. include::'):
                include = os.path.relpath(line.rsplit('::')[1].strip())
                if os.path.exists(include):
                    with open(include) as g:
                        desc.append(g.read())
                else:
                    print('Cannot include {0}; file not found'.format(include))
            else:
                desc.append(line)
    return ''.join(desc)


name = 'pywikibot'
setup(
    name=name,
    version=get_version(),
    description='Python MediaWiki Bot Framework',
    long_description=read_desc('README.rst'),
    keywords=('API', 'bot', 'framework', 'mediawiki', 'pwb', 'python',
              'pywikibot', 'pywikipedia', 'pywikipediabot', 'wiki',
              'wikimedia', 'wikipedia'),
    maintainer='The Pywikibot team',
    maintainer_email='pywikibot@lists.wikimedia.org',
    license='MIT License',
    packages=[str(name)] + [package
                            for package in find_packages()
                            if package.startswith('pywikibot.')],
    python_requires='>=2.7.2, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=dependencies,
    dependency_links=dependency_links,
    extras_require=extra_deps,
    url='https://www.mediawiki.org/wiki/Manual:Pywikibot',
    download_url='https://tools.wmflabs.org/pywikibot/',
    test_suite='tests.collector',
    tests_require=test_deps,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    use_2to3=False
)
