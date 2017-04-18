# -*- coding: utf-8 -*-
"""Tests for the page module."""
#
# (C) Pywikibot team, 2008-2017
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals


__version__ = '$Id$'


import pickle
import re
try:
    import unittest.mock as mock
except ImportError:
    import mock

import pywikibot
import pywikibot.page

from pywikibot import config
from pywikibot import InvalidTitle

from pywikibot.comms.http import session
from pywikibot.tools import (
    MediaWikiVersion,
    PY2,
    StringTypes as basestring,
    UnicodeType as unicode,
)

from tests.aspects import (
    unittest, TestCase, DefaultSiteTestCase, SiteAttributeTestCase,
    DefaultDrySiteTestCase, DeprecationTestCase,
)


EMPTY_TITLE_RE = r'Title must be specified and not empty if source is a Site\.'
INVALID_TITLE_RE = r'The link does not contain a page title'
NO_PAGE_RE = r"doesn't exist\."

class TestPageDeprecation(DefaultSiteTestCase, DeprecationTestCase):

    """Test deprecation of Page attributes."""

    def test_creator(self):
        """Test getCreator."""
        mainpage = self.get_mainpage()
        creator = mainpage.getCreator()
        # session.close()
        self.assertEqual(creator,
                         (mainpage.oldest_revision.user,
                          mainpage.oldest_revision.timestamp.isoformat()))
        self.assertIsInstance(creator[0], unicode)
        self.assertIsInstance(creator[1], unicode)
        self.assertDeprecation()

        self._reset_messages()
        if MediaWikiVersion(self.site.version()) >= MediaWikiVersion('1.16'):
            self.assertIsInstance(mainpage.previous_revision_id, int)
            self.assertEqual(mainpage.previous_revision_id,
                             mainpage.latest_revision.parent_id)
            self.assertDeprecation()


if __name__ == '__main__':  # pragma: no cover
    try:
        unittest.main()
    except SystemExit:
        pass
