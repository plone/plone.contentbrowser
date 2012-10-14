import json
from Products.Five.browser import BrowserView
from interfaces import IContentDetails


class ContentDetails(BrowserView):

    def __call__(self):
        adpt = IContentDetails(self.context)
        self.context.REQUEST.response.setHeader("Content-type",
                                                "application/json")
        return json.dumps(adpt.get_data())
