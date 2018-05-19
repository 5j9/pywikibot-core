# -*- coding: utf-8 -*-
"""
WARNING: THIS MODULE EXISTS SOLELY TO PROVIDE BACKWARDS-COMPATIBILITY.

Do not use in new scripts; use the source to find the appropriate
function/method instead.

"""
#
# (C) Pywikibot team, 2008
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

from pywikibot import Category
from pywikibot.tools import ModuleDeprecationWrapper, deprecated_args


@deprecated_args(
    oldCat='old_cat', newCat='new_cat', sortKey='sort_key', inPlace='in_place')
def change_category(article, old_cat, new_cat, comment=None, sort_key=None,
                    in_place=True):
    """Change the category of the article."""
    return article.change_category(
        old_cat, new_cat, comment, sort_key, in_place)


__all__ = ('Category', 'change_category',)

wrapper = ModuleDeprecationWrapper(__name__)
wrapper._add_deprecated_attr('Category', replacement_name='pywikibot.Category')
wrapper._add_deprecated_attr('change_category', replacement_name='Page.change_category')
