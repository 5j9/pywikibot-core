#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The built-in Script runner distributed with pywikibot library."""
from os.path import dirname as _dirname, abspath as _abspath, join as _join
from subprocess import call as _call
from sys import argv as _argv, executable as _executable


def _main():
    """Invoke _scripts/pwb.py."""
    _pwb_path = _join(_dirname(_abspath(__file__)), '_scripts', 'pwb.py')
    return _call([_executable, _pwb_path] + _argv[1:])


if __name__ == '__main__':
    _main()
