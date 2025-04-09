#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: A base module for all VMWare/VSPhere application classes.

@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2025 by Frank Brehm, Berlin
"""
from __future__ import absolute_import, print_function

# Standard modules
import copy
import logging
import random

# Third party modules
import fb_tools.spinner
from fb_tools.cfg_app import FbConfigApplication
from fb_tools.common import pp
from fb_tools.errors import FbAppError
from fb_tools.multi_config import DEFAULT_ENCODING

import pytz

# Own modules
from .. import __version__ as GLOBAL_VERSION
from ..config import VmwareConfiguration
from ..connect import VsphereConnection
from ..errors import VSphereExpectedError
from ..xlate import XLATOR

__version__ = '1.2.1'
LOG = logging.getLogger(__name__)
TZ = pytz.timezone('Europe/Berlin')

_ = XLATOR.gettext
ngettext = XLATOR.ngettext


# =============================================================================
class VmwareAppError(FbAppError):
    """Base exception class for all exceptions in all VMWare/VSPhere application classes."""

    pass


# =============================================================================
class BaseVmwareApplication(FbConfigApplication):
    """Base class for all VMWare/VSPhere application classes."""

    # -------------------------------------------------------------------------
    def __init__(
        self, appname=None, verbose=0, version=GLOBAL_VERSION, base_dir=None,
            cfg_class=VmwareConfiguration, initialized=False, usage=None, description=None,
            argparse_epilog=None, argparse_prefix_chars='-', env_prefix=None,
            append_appname_to_stems=True, config_dir=None, additional_stems=None,
            additional_cfgdirs=None, cfg_encoding=DEFAULT_ENCODING,
            use_chardet=True):
        """Initialize a BaseVmwareApplication object."""
        self.req_vspheres = None
        self.do_vspheres = []

        # Hash with all VSphere handler objects
        self.vsphere = {}

        super(BaseVmwareApplication, self).__init__(
            appname=appname, verbose=verbose, version=version, base_dir=base_dir,
            description=description, cfg_class=cfg_class,
            append_appname_to_stems=append_appname_to_stems, config_dir=config_dir,
            additional_stems=additional_stems, additional_cfgdirs=additional_cfgdirs,
            cfg_encoding=cfg_encoding, use_chardet=use_chardet, initialized=False,
        )

    # -------------------------------------------------------------------------
    def __del__(self):
        """Clean up in emergency case."""
        if self.vsphere.keys():
            self.cleaning_up()

    # -------------------------------------------------------------------------
    def post_init(self):
        """
        Execute some things before calling run().

        Here could be done some finishing actions after reading in commandline
        parameters, configuration a.s.o.

        This method could be overwritten by descendant classes, these
        methhods should allways include a call to post_init() of the
        parent class.
        """
        self.initialized = False

        super(BaseVmwareApplication, self).post_init()

        if self.verbose > 2:
            LOG.debug(_('{what} of {app} ...').format(what='post_init()', app=self.appname))

        if not self.cfg.vsphere.keys():
            msg = _('Did not found any configured Vsphere environments.')
            LOG.error(msg)
            self.exit(3)

        if self.args.req_vsphere:
            self.req_vspheres = []
            all_found = True
            for vs_name in self.args.req_vsphere:
                LOG.debug(_('Checking for configured VSPhere instance {!r} ...').format(vs_name))
                vs = vs_name.strip().lower()
                if vs not in self.cfg.vsphere.keys():
                    all_found = False
                    msg = _(
                        'VSPhere {!r} not found in list of configured VSPhere instances.').format(
                            vs_name)
                    LOG.error(msg)
                else:
                    if vs not in self.req_vspheres:
                        self.req_vspheres.append(vs)
            if not all_found:
                self.exit(1)

        if self.req_vspheres:
            self.do_vspheres = copy.copy(self.req_vspheres)
        else:
            for vs_name in self.cfg.vsphere.keys():
                self.do_vspheres.append(vs_name)

        self.init_vsphere_handlers()

    # -------------------------------------------------------------------------
    def init_arg_parser(self):
        """Initiate the argument parser."""
        super(BaseVmwareApplication, self).init_arg_parser()

        self.arg_parser.add_argument(
            '--vs', '--vsphere', dest='req_vsphere', nargs='*',
            help=_(
                'The VSPhere names from configuration, in which the VMs should be searched.')
        )

    # -------------------------------------------------------------------------
    def perform_arg_parser(self):
        """Evaluate the command line parameters. Maybe overridden."""
        if self.verbose > 2:
            LOG.debug(_('Got command line arguments:') + '\n' + pp(self.args))

    # -------------------------------------------------------------------------
    def init_vsphere_handlers(self):
        """Initialize all VSphere handlers."""
        if self.verbose > 1:
            LOG.debug(_('Initializing VSphere handlers ...'))

        try:
            for vsphere_name in self.do_vspheres:
                self.init_vsphere_handler(vsphere_name)
        except VSphereExpectedError as e:
            LOG.error(str(e))
            self.exit(7)

    # -------------------------------------------------------------------------
    def init_vsphere_handler(self, vsphere_name):
        """Initialize the given VSphere handler."""
        if self.verbose > 2:
            LOG.debug(_('Initializing handler for VSPhere {!r} ...').format(vsphere_name))

        vsphere_data = self.cfg.vsphere[vsphere_name]

        vsphere = VsphereConnection(
            vsphere_data, auto_close=True, simulate=self.simulate, force=self.force,
            appname=self.appname, verbose=self.verbose, base_dir=self.base_dir,
            terminal_has_colors=self.terminal_has_colors, initialized=False)

        if vsphere:
            self.vsphere[vsphere_name] = vsphere
            vsphere.initialized = True
        else:
            msg = _('Could not initialize {} object from:').format('VsphereConnection')
            msg += '\n' + str(vsphere_data)
            LOG.error(msg)

        vsphere._check_credentials()

    # -------------------------------------------------------------------------
    def cleaning_up(self):
        """Close all VSPhere connections and remove all VSphere handlers."""
        if self.verbose > 1:
            LOG.debug(_('Cleaning up ...'))

        for vsphere_name in self.do_vspheres:
            if vsphere_name in self.vsphere:
                LOG.debug(_('Closing VSPhere object {!r} ...').format(vsphere_name))
                self.vsphere[vsphere_name].disconnect()
                del self.vsphere[vsphere_name]

    # -------------------------------------------------------------------------
    @classmethod
    def get_random_spinner_name(cls):
        """Return a randon spinner name from fb_tools.spinner.CycleList."""
        randomizer = random.SystemRandom()

        return randomizer.choice(list(fb_tools.spinner.CycleList.keys()))


# =============================================================================
if __name__ == '__main__':

    pass

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 list
