#!/usr/bin/python
# -*- coding: utf-8 -*-
"""DEPRECATED! This script generates a family file from a given URL."""
#
# (C) Merlijn van Deen, 2010-2013
# (C) Pywikibot team, 2010-2018
#
# Distributed under the terms of the MIT license
#
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from os.path import dirname, abspath, join
from subprocess import call
from sys import argv, executable, stderr


print('generate_family_file.py script is deprecated. '
      'Please run `pywikibot generate_family_file` instead.',
      file=stderr)


def main():
    """Invoke pywikibot/_scripts/generate_family_file.py."""
    generate_family_file = join(
        dirname(abspath(__file__)), 'pywikibot', '_scripts',
        'generate_family_file.py')
    return call([executable, generate_family_file] + argv[1:])


if __name__ == '__main__':
    main()
