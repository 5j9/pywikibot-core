#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""DEPRECATED wrapper script to use Pywikibot in 'directory' mode.

Run scripts using:

    python pwb.py <name_of_script> <options>

and it will use the package directory to store all user files, will fix up
search paths so the package does not need to be installed, etc.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from os.path import dirname, abspath, join
from subprocess import call
from sys import argv, executable, stderr


print('The pwb.py script is deprecated. Please use `pywikibot` instead.',
      file=stderr)


def main():
    """Invoke pywikibot/_scripts/pwb.py."""
    _pwb_path = join(
        dirname(abspath(__file__)), 'pywikibot', '_scripts', 'pwb.py')
    return call([executable, _pwb_path] + argv[1:])


if __name__ == '__main__':
    main()
