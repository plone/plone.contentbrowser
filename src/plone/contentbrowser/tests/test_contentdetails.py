# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.interface import implements
from zope.interface import alsoProvides
from zope.component import queryAdapter
from zope.component import getAdapter
from zope.publisher.browser import TestRequest as baseRequest

from z3c.form.interfaces import IFormLayer

from Products.CMFCore.interfaces import IContentish
from Products.ATContentTypes.interfaces import IATImage
from Products.ATContentTypes.interfaces import IATFile

from ..interfaces import IContentDetails
from ..interfaces import IContentForm

from ..adapters.contentdetails import BaseContentDetails
from ..adapters.contentdetails import ImageDetails
from ..adapters.contentdetails import FileDetails

from ..testing import PLONE_CONTENTBROWSER_INTEGRATION


# dummy request
class TestRequest(baseRequest):
    implements(IFormLayer)

request = TestRequest()


class Content(object):
    # dummy content
    implements(IContentish)
    REQUEST = request

    def Title(self):
        return "Base Content"

    def Description(self):
        return "Description"

    def getPrimaryField(self):
        return ContentFileField()

    def getTypeInfo(self):
        class DummyTypeinput(object):
            def Title(self):
                return 'Dummy Content'
        return DummyTypeinput()


class ContentFileField(object):
    # pylint: disable=W0613
    size = 120101

    def get_size(self, context):
        return self.size

    def getSize(self, context):
        return self.size

    def tag(self, context, scale):
        return '<img />'

    def getContentType(self, context):
        return 'text/plain'


class TestSetup(unittest.TestCase):
    layer = PLONE_CONTENTBROWSER_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def test_filedetails(self):
        """Testing file details adapters for:
        * generic content type
        * image
        * file
        """
        content = Content()
        adapter = queryAdapter(content, IContentDetails)
        self.assertTrue(isinstance(adapter, BaseContentDetails))

        data = adapter.get_data()
        self.assertEqual([i['label'] for i in data],
            [u'Title', u'Description', u'Type'])

        image = Content()
        alsoProvides(image, IATImage)
        img_adapter = queryAdapter(image, IContentDetails)
        self.assertTrue(isinstance(img_adapter, ImageDetails))

        self.assertEqual([i['label'] for i in img_adapter.get_data()],
            [u'Title', u'Description', u'Type', u'Pixel (w, h)', u'Preview'])

        file_ = Content()
        alsoProvides(file_, IATFile)
        file_adapter = queryAdapter(file_, IContentDetails)
        self.assertTrue(isinstance(file_adapter, FileDetails))

        self.assertEqual([i['label'] for i in file_adapter.get_data()],
            [u'Title', u'Description', u'Type', u'Size', u'Content type'])

    def test_contenforms(self):
        adapter = IContentForm(self.portal)
        form = adapter(self.portal, request)
        self.assertEqual(form.content_type, u'Folder')

        adapter = getAdapter(self.portal, IContentForm, name='File')
        form = adapter(self.portal, request)
        self.assertEqual(form.content_type, u'File')

        adapter = getAdapter(self.portal, IContentForm, name='Image')
        form = adapter(self.portal, request)
        self.assertEqual(form.content_type, u'Image')

        adapter = getAdapter(self.portal, IContentForm, name='Link')
        form = adapter(self.portal, request)
        self.assertEqual(form.content_type, u'Link')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
