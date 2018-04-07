#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Ensure the right version of Python and pip are installed on AppVeyor."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

from io import open
from os import getenv, listdir, remove
from os.path import exists
from shutil import copyfile
from subprocess import CalledProcessError, check_output
try:
    from urllib.request import urlretrieve
except ImportError:  # Python 2
    from urllib import urlretrieve


def get_installer_info(version, arch64):
    """Return the download url and filename for given version and arch."""
    # See https://www.python.org/downloads/windows/
    msi_installer = version < '3.5.0'
    filename = 'python-{version}{amd64}{extension}'.format(
        amd64=(('.' if msi_installer else '-')
               + 'amd64' if arch64 else ''),
        extension=('.msi' if msi_installer else '.exe'),
        **locals())
    url = 'https://www.python.org/ftp/python/{version}/{filename}'.format(
        **locals())
    return filename, url


def download_python(version, arch64):
    """Download Python installer and return its filename."""
    filename, download_url = get_installer_info(version, arch64)
    print('Downloading Python installer from', download_url)
    urlretrieve(download_url, filename)
    return filename


def print_python_install_log(version):
    """Print the log for Python installation."""
    # appveyor's %temp% points to "C:\Users\appveyor\AppData\Local\Temp\1"
    # but python log files are stored in "C:\Users\appveyor\AppData\Local\Temp
    temp_dir = 'C:/Users/appveyor/AppData/Local/Temp/'
    for file in listdir(temp_dir):
        if file[-4:] == '.log' and file.startswith('Python ' + version):
            with open(temp_dir + file, encoding='utf-8') as log:
                print(file + ':\n' + log.read())
            break
    else:
        print('There was no Python log file.')


def install_python(installer, python_dir, python_ver):
    """Install Python using specified installer file."""
    common_args = [
        installer, '/quiet', 'TargetDir=' + python_dir, 'AssociateFiles=0',
        'Shortcuts=0', 'Include_doc=0', 'Include_launcher=0',
        'InstallLauncherAllUsers=0', 'Include_tcltk=0', 'Include_test=0']
    try:
        if installer[-4:] == '.msi':
            check_output(['msiexec', '/norestart', '/i'] + common_args)
        else:  # executable installer
            # uninstall first, otherwise the install won't do anything
            check_output(common_args)
    except CalledProcessError:
        print_python_install_log(python_ver)
        raise SystemExit('install_python failed')


def prepare_pip(python_ver):
    """Prepare pip for older versions of python."""
    if python_ver < '2.7.9' or python_ver == '3.4.0':
        # virtualenv binds the pip of pre-installed python to current python
        # installation.
        check_output('pip install virtualenv', shell=True)
        check_output('virtualenv env', shell=True)


def main():
    python_ver = getenv('PYTHON_VERSION')
    python_dir = getenv('PYTHON')
    if not python_ver[-2:] == '.x':  # .x is for pre-installed Python versions
        arch64 = getenv('PYTHON_ARCH') == '64'
        filename = download_python(python_ver, arch64)
        install_python(filename, python_dir, python_ver)
    if not exists(python_dir + r'\python.exe'):
        print_python_install_log(python_ver)
        raise SystemExit(python_dir + r'\python.exe not found')
    prepare_pip(python_dir)


if __name__ == '__main__':
    main()
