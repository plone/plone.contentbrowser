from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate

from Products.CMFCore.utils import getToolByName
from ..interfaces import IContentDetails

from .. import messageFactory as _


PLMF = MessageFactory('plone')


class BaseContentDetails(object):
    implements(IContentDetails)

    def __init__(self, context):
        self.context = context

    @property
    def _typeinfo(self):
        return self.context.getTypeInfo()

    def translate(self, value):
        return translate(value, context=self.context.REQUEST)

    def get_data(self):
        return [
            {'label': self.translate(_(u'Title')),
             'value': self.context.Title()},
            {'label': self.translate(_(u'Description')),
             'value': self.context.Description()},
            {'label': self.translate(_(u'Type')),
             'value': self.translate(PLMF(self._typeinfo.Title()))},
        ]


class ImageDetails(BaseContentDetails):
    """Adapter for ATImage
    """

    extra_data = [
        (_(u'Pixel (w, h)'), lambda f, c: str(f.getSize(c))),
        (_(u'Preview'), lambda f, c: f.tag(c, scale='thumb')),
    ]

    @property
    def mtr(self):
        return getToolByName(self.context, 'mimetypes_registry')

    @property
    def field(self):
        return self.context.getPrimaryField()

    def get_data(self):
        data = super(ImageDetails, self).get_data()
        for label, value in self.extra_data:
            data.append({
                'label': self.translate(label),
                'value': value(self.field, self.context),
                })
        return data


class FileDetails(ImageDetails):
    """Adapter for ATFile
    """

    extra_data = [
        (_(u'Size'), lambda f, c: '%dKb' % (f.get_size(c) / 1024)),
    ]

    def get_data(self):
        data = super(FileDetails, self).get_data()

        value = self.field.getContentType(self.context)
        mime = self.mtr.lookup(value)
        if len(mime) > 0:
            # get the first mimetype found
            value = mime[0].name()
        data.append({
            'label': self.translate(_(u'Content type')),
            'value': value
        })

        return data
