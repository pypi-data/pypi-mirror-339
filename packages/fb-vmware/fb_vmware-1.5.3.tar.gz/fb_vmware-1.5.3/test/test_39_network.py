#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: Test script (and module) for unit tests on module fb_vmware.network.

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

LOG = logging.getLogger('test-network')


# =============================================================================
class TestVMNetwork(FbVMWareTestcase):
    """Testcase for unit tests on a VsphereNetwork object."""

    # -------------------------------------------------------------------------
    def setUp(self):
        """Execute this on seting up before calling each particular test method."""
        super(TestVMNetwork, self).setUp()

    # -------------------------------------------------------------------------
    def test_import(self):
        """Test import of fb_vmware.network."""
        LOG.info(self.get_method_doc())

        import fb_vmware.network
        from fb_vmware import VsphereNetwork
        from fb_vmware import VsphereNetworkDict

        LOG.debug('Version of fb_vmware.network: {!r}.'.format(fb_vmware.network.__version__))

        doc = textwrap.dedent(VsphereNetwork.__doc__)
        LOG.debug('Description of VsphereNetwork: ' + doc)

        doc = textwrap.dedent(VsphereNetworkDict.__doc__)
        LOG.debug('Description of VsphereNetworkDict: ' + doc)

    # -------------------------------------------------------------------------
    def test_init_object(self):
        """Test init of a VsphereNetwork object."""
        LOG.info(self.get_method_doc())

        from fb_vmware import VsphereNetwork
        from fb_vmware.errors import VSphereNameError

        with self.assertRaises(VSphereNameError) as cm:

            network = VsphereNetwork(appname=self.appname)
            LOG.debug('VsphereNetwork %s:\n{}'.format(network))

        e = cm.exception
        LOG.debug('%s raised: %s', e.__class__.__qualname__, e)

        net_name = '10.12.11.0_24'

        network = VsphereNetwork(
            name=net_name,
            appname=self.appname,
            verbose=1,
        )

        LOG.debug('VsphereNetwork %r: {!r}'.format(network))
        LOG.debug('VsphereNetwork %s:\n{}'.format(network))

        self.assertIsInstance(network, VsphereNetwork)
        self.assertEqual(network.appname, self.appname)
        self.assertEqual(network.verbose, 1)
        self.assertEqual(network.name, net_name)

    # -------------------------------------------------------------------------
    def test_init_from_summary(self):
        """Test init by calling VsphereNetwork.from_summary()."""
        LOG.info(self.get_method_doc())

        from fb_vmware import VsphereNetwork

        net_name = '10.12.11.0_24'

        data = SimpleTestObject()
        data.summary = SimpleTestObject()
        data.configStatus = 'gray'

        with self.assertRaises(TypeError) as cm:

            network = VsphereNetwork.from_summary(
                data, appname=self.appname, verbose=self.verbose)
            LOG.debug('VsphereNetwork %s:\n{}'.format(network))

        e = cm.exception
        LOG.debug('%s raised: %s', e.__class__.__qualname__, e)

        with self.assertRaises((TypeError, AssertionError)) as cm:

            network = VsphereNetwork.from_summary(
                data, appname=self.appname, verbose=self.verbose, test_mode=True)
            LOG.debug('VsphereNetwork %s:\n{}'.format(network))

        e = cm.exception
        LOG.debug('%s raised: %s', e.__class__.__qualname__, e)

        data.overallStatus = 'gray'
        data.summary.name = net_name

        network = VsphereNetwork.from_summary(
            data, appname=self.appname, verbose=self.verbose, test_mode=True)
        LOG.debug('VsphereNetwork %s:\n{}'.format(network))


# =============================================================================
if __name__ == '__main__':

    verbose = get_arg_verbose()
    if verbose is None:
        verbose = 0
    init_root_logger(verbose)

    LOG.info('Starting tests ...')

    suite = unittest.TestSuite()

    suite.addTest(TestVMNetwork('test_import', verbose))
    suite.addTest(TestVMNetwork('test_init_object', verbose))
    suite.addTest(TestVMNetwork('test_init_from_summary', verbose))

    runner = unittest.TextTestRunner(verbosity=verbose)

    result = runner.run(suite)

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
