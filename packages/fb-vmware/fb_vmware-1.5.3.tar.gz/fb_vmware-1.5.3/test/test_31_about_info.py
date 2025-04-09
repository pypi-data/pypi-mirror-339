#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: Test script (and module) for unit tests on module fb_vmware.about.

@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2025 Frank Brehm, Berlin
@license: GPL3
"""

import logging
import os
import sys
import textwrap

try:
    import unittest2 as unittest
except ImportError:
    import unittest

libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.insert(0, libdir)

from general import FbVMWareTestcase, get_arg_verbose, init_root_logger
from general import SimpleTestObject

LOG = logging.getLogger('test-aboutinfo')


# =============================================================================
class TestVMAboutInfo(FbVMWareTestcase):
    """Testcase for unit tests on a VsphereAboutInfo object."""

    # -------------------------------------------------------------------------
    def setUp(self):
        """Execute this on seting up before calling each particular test method."""
        super(TestVMAboutInfo, self).setUp()

    # -------------------------------------------------------------------------
    def test_import(self):
        """Test import of fb_vmware.about."""
        LOG.info(self.get_method_doc())

        import fb_vmware.about
        from fb_vmware import VsphereAboutInfo

        LOG.debug('Version of fb_vmware.about: {!r}.'.format(fb_vmware.about.__version__))

        doc = textwrap.dedent(VsphereAboutInfo.__doc__)
        LOG.debug('Description of VsphereAboutInfo: ' + doc)

    # -------------------------------------------------------------------------
    def test_init_object(self):
        """Test init of a VsphereAboutInfo object."""
        LOG.info(self.get_method_doc())

        from fb_vmware import VsphereAboutInfo

        about_info = VsphereAboutInfo(
            appname=self.appname,
            verbose=1,
        )

        LOG.debug('VsphereAboutInfo %r: {!r}'.format(about_info))
        LOG.debug('VsphereAboutInfo %s:\n{}'.format(about_info))

        self.assertIsInstance(about_info, VsphereAboutInfo)
        self.assertEqual(about_info.appname, self.appname)
        self.assertEqual(about_info.verbose, 1)

    # -------------------------------------------------------------------------
    def test_init_from_summary(self):
        """Test init by calling VsphereAboutInfo.from_summary()."""
        LOG.info(self.get_method_doc())

        from fb_vmware import VsphereAboutInfo

        api_type = 'VirtualCenter'
        api_version = '6.5'
        full_name = 'VMware vCenter Server 6.5.0 build-8024368'
        instance_uuid = 'ea1b28ca-0d17-4292-ab04-189e57ec9629'
        lic_prodname = 'VMware VirtualCenter Server'
        lic_prodversion = '6.0'
        name = 'VMware vCenter Server'
        os_version = '6.5.0'
        os_type = 'linux-x64'
        vendor = 'VMware, Inc.'

        data = SimpleTestObject()
        data.apiType = api_type
        data.apiVersion = api_version
        data.fullName = full_name
        data.instanceUuid = instance_uuid
        data.licenseProductName = lic_prodname
        data.licenseProductVersion = lic_prodversion
        data.name = name

        with self.assertRaises(TypeError) as cm:

            about_info = VsphereAboutInfo.from_summary(
                data, appname=self.appname, verbose=self.verbose)
            LOG.debug('VsphereAboutInfo %s:\n{}'.format(about_info))

        e = cm.exception
        LOG.debug('%s raised: %s', e.__class__.__qualname__, e)

        with self.assertRaises(AssertionError) as cm:

            about_info = VsphereAboutInfo.from_summary(
                data, appname=self.appname, verbose=self.verbose, test_mode=True)
            LOG.debug('VsphereAboutInfo %s:\n{}'.format(about_info))

        e = cm.exception
        LOG.debug('%s raised: %s', e.__class__.__qualname__, e)

        data.version = os_version
        data.osType = os_type
        data.vendor = vendor

        about_info = VsphereAboutInfo.from_summary(
            data, appname=self.appname, verbose=self.verbose, test_mode=True)
        LOG.debug('VsphereAboutInfo %s:\n{}'.format(about_info))


# =============================================================================
if __name__ == '__main__':

    verbose = get_arg_verbose()
    if verbose is None:
        verbose = 0
    init_root_logger(verbose)

    LOG.info('Starting tests ...')

    suite = unittest.TestSuite()

    suite.addTest(TestVMAboutInfo('test_import', verbose))
    suite.addTest(TestVMAboutInfo('test_init_object', verbose))
    suite.addTest(TestVMAboutInfo('test_init_from_summary', verbose))

    runner = unittest.TextTestRunner(verbosity=verbose)

    result = runner.run(suite)

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
