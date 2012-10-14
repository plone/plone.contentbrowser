from zope.interface import Interface


class IBrowserLayer(Interface):
    """plone.contentbrowser browser layer"""


class IContentDetails(Interface):
    """This interface provides a representation
    of a content type useful to display its details
    on reference widget
    """

    def get_data(self):
        """It returns an array of item properties
        """
