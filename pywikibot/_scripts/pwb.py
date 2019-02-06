#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Wrapper script to use Pywikibot in 'directory' mode.

Run scripts using:

    python pwb.py <name_of_script> <options>

and it will use the package directory to store all user files, will fix up
search paths so the package does not need to be installed, etc.
"""
# (C) Pywikibot team, 2012-2018
#
# Distributed under the terms of the MIT license.
#
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import sys
import types

from os.path import dirname, join, exists, relpath, abspath
from warnings import warn


pwb = None


def remove_modules():
    """Remove pywikibot modules."""
    for name in list(sys.modules):
        if name.startswith('pywikibot'):
            del sys.modules[name]


def tryimport_pwb():
    """Try to import pywikibot.

    If so, we need to patch pwb.argvu, too.
    If pywikibot is not available, we create a mock object to remove the
    need for if statements further on.
    """
    global pwb
    try:
        import pywikibot
    except RuntimeError:
        remove_modules()
        os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '2'
        import pywikibot
    pwb = pywikibot


# The following snippet was developed by Ned Batchelder (and others)
# for coverage [1], with python 3 support [2] added later,
# and is available under the BSD license (see [3])
# [1]
# https://bitbucket.org/ned/coveragepy/src/b5abcee50dbe/coverage/execfile.py
# [2]
# https://bitbucket.org/ned/coveragepy/src/fd5363090034/coverage/execfile.py
# [3]
# https://bitbucket.org/ned/coveragepy/src/2c5fb3a8b81c/setup.py?at=default#cl-31

def run_python_file(filename, argv, argvu, package=None):
    """Run a python file as if it were the main program on the command line.

    `filename` is the path to the file to execute, it need not be a .py file.
    `args` is the argument array to present as sys.argv, as unicode strings.

    """
    tryimport_pwb()

    # Create a module to serve as __main__
    old_main_mod = sys.modules['__main__']
    # it's explicitly using str() to bypass unicode_literals in Python 2
    main_mod = types.ModuleType(str('__main__'))
    sys.modules['__main__'] = main_mod
    main_mod.__file__ = filename
    if sys.version_info[0] > 2:
        main_mod.__builtins__ = sys.modules['builtins']
    else:
        main_mod.__builtins__ = sys.modules['__builtin__']
    if package:
        # it's explicitly using str() to bypass unicode_literals in Python 2
        main_mod.__package__ = str(package)

    # Set sys.argv and the first path element properly.
    old_argv = sys.argv
    old_argvu = pwb.argvu
    old_path0 = sys.path[0]

    sys.argv = argv
    pwb.argvu = argvu
    sys.path[0] = dirname(filename)

    try:
        with open(filename, 'rb') as f:
            source = f.read()
        exec(compile(source, filename, 'exec', dont_inherit=True),
             main_mod.__dict__)
    finally:
        # Restore the old __main__
        sys.modules['__main__'] = old_main_mod

        # Restore the old argv and path
        sys.argv = old_argv
        sys.path[0] = old_path0
        pwb.argvu = old_argvu

# end of snippet from coverage


# Establish a normalised path for the directory containing pwb.py.
# Either it is '.' if the user's current working directory is the same,
# or it is the absolute path for the directory of pwb.py
absolute_path = abspath(dirname(sys.argv[0]))
rewrite_path = absolute_path

sys.path = [sys.path[0], rewrite_path,
            join(rewrite_path, 'pywikibot', 'compat'),
            ] + sys.path[1:]

if len(sys.argv) > 1 and sys.argv[1][0] != '-':
    target_script = sys.argv[1]
    if not target_script.endswith('.py'):
        target_script += '.py'
else:
    target_script = None

# Skip the filename if one was given
args = sys.argv[(2 if target_script else 1):]


_scripts_dir = dirname(__file__)
pywikibot_dir = dirname(_scripts_dir)
pywikibot_parent_dir = dirname(pywikibot_dir)
# Search for user-config.py before creating one.
# Use env var to communicate to config2.py pwb.py location (bug T74918).
if sys.platform == 'win32' and sys.version_info[0] < 3:
    pywikibot_parent_dir = str(pywikibot_parent_dir)
os.environ['PYWIKIBOT_DIR_PWB'] = pywikibot_parent_dir
try:
    # If successful, user-config.py already exists in one of the candidate
    # directories. See config2.py for details on search order.
    import pywikibot
    pwb = pywikibot
except RuntimeError:
    # user-config.py to be created
    if target_script is not None and not (target_script.startswith('generate_')
                                          or target_script == 'version.py'):
        print("NOTE: 'user-config.py' was not found!")
        print('Please follow the prompts to create it:')
        run_python_file(join(_scripts_dir, 'generate_user_files.py'),
                        ['generate_user_files.py'],
                        ['generate_user_files.py'])
        # because we have loaded pywikibot without user-config.py loaded,
        # we need to re-start the entire process. Ask the user to do so.
        print('Now, you have to re-execute the command to start your script.')
        sys.exit(1)


def main():
    """Command line entry point."""
    global target_script
    if target_script:
        script_dir = None
        tryimport_pwb()
        argvu = pwb.argvu[1:]
        if not exists(target_script):
            script_paths = [
                'scripts', 'scripts.maintenance', 'scripts.archive',
                'scripts.userscripts', 'pywikibot._scripts',
            ]
            from pywikibot import config
            if config.user_script_paths:
                if isinstance(config.user_script_paths, (tuple, list)):
                    script_paths = config.user_script_paths + script_paths
                else:
                    warn("'user_script_paths' must be a list or tuple,\n"
                         'found: {0}. Ignoring this setting.'
                         ''.format(type(config.user_script_paths)))
            for script_dir in script_paths:
                paths = script_dir.split('.') + [target_script]
                testpath = join(pywikibot_parent_dir, *paths)
                if exists(testpath):
                    target_script = testpath
                    break
            else:
                print(
                    'ERROR: {} not found! Misspelling?'.format(target_script),
                    file=sys.stderr)
                return True

        # When both pwb.py and the filename to run are within the current
        # working directory:
        # a) set __package__ as if called using python -m scripts.blah.foo
        # b) set __file__ to be relative, so it can be relative in backtraces,
        #    and __file__ *appears* to be an unstable path to load data from.
        # This is a rough (and quick!) emulation of 'package name' detection.
        # a much more detailed implementation is in coverage's find_module.
        # https://bitbucket.org/ned/coveragepy/src/default/coverage/execfile.py
        cwd = abspath(os.getcwd())
        if absolute_path == cwd:
            absolute_filename = abspath(target_script)[:len(cwd)]
            if absolute_filename == cwd:
                relative_filename = relpath(target_script)
                # remove the filename, and use '.' instead of path separator.
                script_dir = dirname(relative_filename).replace(os.sep, '.')
                target_script = join(os.curdir, relative_filename)

        if script_dir and script_dir not in sys.modules:
            try:
                __import__(script_dir)
            except ImportError as e:
                warn('Parent module %s not found: %s'
                     % (script_dir, e), ImportWarning)

        run_python_file(target_script, [target_script] + args, argvu, script_dir)
        return True
    else:
        return False


if __name__ == '__main__':
    if not main():
        print(__doc__)
