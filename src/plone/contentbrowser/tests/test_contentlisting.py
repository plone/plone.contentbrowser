import unittest2 as unittest
from plone.contentbrowser.testing import\
    PLONE_CONTENTBROWSER_INTEGRATION


class TestExample(unittest.TestCase):
    layer = PLONE_CONTENTBROWSER_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_listing(self):
        pass

    def test_search(self):
        pass
