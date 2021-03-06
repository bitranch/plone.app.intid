# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.intid.interfaces import IIntIds
from zope.component import getUtility

from plone.app.testing import applyProfile
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from ..setuphandlers import add_intids
from ..testing import SETUP_TESTING


class TestSetup(unittest.TestCase):
    layer = SETUP_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def tearDown(self):
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def test_install(self):
        """When p.app.intid is intalled it registers some utility
        from zope.intid and five.intid and search in portal_catalog
        all contents in order to register them in these utilities.

        This test checks that all pre existing contents
        are registered correctly
        """

        # we create a folder before the intallation of plone.app.intid
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        folder_id = self.portal.invokeFactory('Folder', 'folder')
        folder = self.portal[folder_id]

        # now we install manually the intid utilities
        add_intids(self.portal)
        intids = getUtility(IIntIds)

        # this folder is not referenced by intid utility
        self.assertRaises(KeyError, intids.getId, folder)

        # when we install p.app.intid our folder is referencend by intid
        applyProfile(self.portal, 'plone.app.intid:default')
        self.assertIsNotNone(intids.getId(folder))
