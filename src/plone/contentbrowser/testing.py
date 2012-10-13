from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import plone.contentbrowser


PLONE_CONTENTBROWSER = PloneWithPackageLayer(
    zcml_package=plone.contentbrowser,
    zcml_filename='testing.zcml',
    gs_profile_id='plone.contentbrowser:testing',
    name="PLONE_CONTENTBROWSER")

PLONE_CONTENTBROWSER_INTEGRATION = IntegrationTesting(
    bases=(PLONE_CONTENTBROWSER, ),
    name="PLONE_CONTENTBROWSER_INTEGRATION")

PLONE_CONTENTBROWSER_FUNCTIONAL = FunctionalTesting(
    bases=(PLONE_CONTENTBROWSER, ),
    name="PLONE_CONTENTBROWSER_FUNCTIONAL")
