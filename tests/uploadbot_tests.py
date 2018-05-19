# -*- coding: utf-8 -*-
"""
UploadRobot test.

These tests write to the wiki.
"""
#
# (C) Pywikibot team, 2015
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

import os

from scripts import upload

from tests import join_images_path
from tests.aspects import unittest, TestCase


class TestUploadbot(TestCase):

    """Test cases for upload."""

    write = True

    family = 'wikipedia'
    code = 'test'

    def test_png_list(self):
        """Test uploading a list of pngs using upload.py."""
        image_list = []
        for directory_info in os.walk(join_images_path()):
            for dir_file in directory_info[2]:
                image_list.append(os.path.join(directory_info[0], dir_file))
        bot = upload.UploadRobot(
            url=image_list, description="pywikibot upload.py script test",
            use_filename=None, keep_filename=True, verify_description=True,
            aborts=set(), ignore_warning=True, target_site=self.get_site())
        bot.run()

    def test_png(self):
        """Test uploading a png using upload.py."""
        bot = upload.UploadRobot(
            url=[join_images_path("MP_sounds.png")],
            description="pywikibot upload.py script test", use_filename=None,
            keep_filename=True, verify_description=True, aborts=set(),
            ignore_warning=True, target_site=self.get_site())
        bot.run()

    def test_png_url(self):
        """Test uploading a png from url using upload.py."""
        bot = upload.UploadRobot(
            url=['https://upload.wikimedia.org/wikipedia/commons/f/fc/'
                 'MP_sounds.png'],
            description="pywikibot upload.py script test", use_filename=None,
            keep_filename=True, verify_description=True, aborts=set(),
            ignore_warning=True, target_site=self.get_site())
        bot.run()


if __name__ == '__main__':  # pragma: no cover
    try:
        unittest.main()
    except SystemExit:
        pass
