# -*- coding: utf-8 -*-
"""Tests for http module."""
#
# (C) Pywikibot team, 2014-2017
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

__version__ = '$Id$'

import json
import re
import warnings

import requests

import pywikibot

from pywikibot import config2 as config
from pywikibot.comms import http, threadedhttp
from pywikibot.tools import (
    PYTHON_VERSION,
    UnicodeType as unicode,
)

from tests import join_images_path
from tests.aspects import (
    unittest,
    TestCase,
    DeprecationTestCase,
    HttpbinTestCase,
    require_modules,
)


class HttpsCertificateTestCase(TestCase):

    """HTTPS certificate test."""

    CERT_VERIFY_FAILED_RE = 'certificate verify failed'
    hostname = 'testssl-expire-r2i2.disig.sk'

    def test_https_cert_error(self):
        """Test if http.fetch respects disable_ssl_certificate_validation."""
        self.assertRaisesRegex(pywikibot.FatalServerError, self.CERT_VERIFY_FAILED_RE,
                               http.fetch,
                               uri='https://testssl-expire-r2i2.disig.sk/index.en.html')
        http.session.close()  # clear the connection

        with warnings.catch_warnings(record=True) as warning_log:
            response = http.fetch(
                uri='https://testssl-expire-r2i2.disig.sk/index.en.html',
                disable_ssl_certificate_validation=True)
        r = response.content
        self.assertIsInstance(r, unicode)
        self.assertTrue(re.search(r'<title>.*</title>', r))
        http.session.close()  # clear the connection

        # Verify that it now fails again
        try:
            http.fetch(uri='https://testssl-expire-r2i2.disig.sk/index.en.html')
        except http.FatalServerError:
            pass
        http.session.close()  # clear the connection

        # Verify that the warning occurred
        from pprint import pprint
        pprint([w.__dict__ for w in warning_log])
        self.assertEqual(len(warning_log), 1)
        self.assertEqual(warning_log[0].category.__name__,
                         'InsecureRequestWarning')

