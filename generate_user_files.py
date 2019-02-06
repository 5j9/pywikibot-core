#!/usr/bin/python
# -*- coding: utf-8 -*-
"""DEPRECATED script to create user-config.py."""
#
# (C) Pywikibot team, 2010-2018
#
# Distributed under the terms of the MIT license.
#
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from os.path import dirname, abspath, join
from subprocess import call
from sys import argv, executable, stderr


print('generate_user_files.py script is deprecated. '
      'Please run `pywikibot generate_user_files` instead.',
      file=stderr)


def main():
    """Invoke pywikibot/_scripts/generate_family_file.py."""
    generate_user_files = join(
        dirname(abspath(__file__)), 'pywikibot', '_scripts',
        'generate_user_files.py')
    return call([executable, generate_user_files] + argv[1:])


if __name__ == '__main__':
    main()
