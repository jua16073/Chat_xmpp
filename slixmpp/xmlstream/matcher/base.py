# -*- coding: utf-8 -*-
"""
    slixmpp.xmlstream.matcher.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Part of Slixmpp: The Slick XMPP Library

    :copyright: (c) 2011 Nathanael C. Fritz
    :license: MIT, see LICENSE for more details
"""


class MatcherBase(object):

    """
    Base class for stanza matchers. Stanza matchers are used to pick
    stanzas out of the XML stream and pass them to the appropriate
    stream handlers.

    :param criteria: Object to compare some aspect of a stanza against.
    """

    def __init__(self, criteria):
        self._criteria = criteria

    def match(self, xml):
        """Check if a stanza matches the stored criteria.

        Meant to be overridden.
        """
        return False
