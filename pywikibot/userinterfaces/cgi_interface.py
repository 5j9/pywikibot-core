# -*- coding: utf-8 -*-
"""CGI user interface."""
#
# (C) Pywikibot team, 2007-2015
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

import sys

from pywikibot.tools import deprecated_args


class UI(object):

    """CGI user interface."""

    @deprecated_args(toStdout='to_stdout')
    def output(self, text, colors=None, newline=True, to_stdout=False):
        """Output text to CGI stream if to_stdout is True."""
        if not to_stdout:
            return
        sys.stdout.write(text.encode('UTF-8', 'replace'))

    def input(self, question, colors=None):
        """Output question to CGI stream."""
        self.output(question + ' ', newline=False, to_stdout=True)
