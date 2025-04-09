#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: The module for a VSphere disk controller object.

@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2025 by Frank Brehm, Berlin
"""
from __future__ import absolute_import

# Standard modules
import copy
import logging
try:
    from collections.abc import MutableSequence
except ImportError:
    from collections import MutableSequence

# Third party modules
from fb_tools.common import pp, to_bool
from fb_tools.obj import FbBaseObject
from fb_tools.xlate import format_list

from pyVmomi import vim

# Own modules
from .errors import VSphereDiskCtrlrTypeNotFoudError
from .xlate import XLATOR

__version__ = '1.1.0'
LOG = logging.getLogger(__name__)

_ = XLATOR.gettext


# =============================================================================
class VsphereDiskController(FbBaseObject):
    """This is a wrapper for a vim.vm.device.VirtualController object."""

    ctrl_types = (
        (vim.vm.device.VirtualIDEController, 'ide'),
        (vim.vm.device.VirtualNVMEController, 'nvme'),
        (vim.vm.device.VirtualPCIController, 'pci'),
        (vim.vm.device.VirtualPS2Controller, 'ps2'),
        (vim.vm.device.VirtualAHCIController, 'ahci'),
        (vim.vm.device.VirtualSATAController, 'sata'),
        (vim.vm.device.ParaVirtualSCSIController, 'para_virt_scsi'),
        (vim.vm.device.VirtualBusLogicController, 'bus_logic'),
        (vim.vm.device.VirtualLsiLogicController, 'lsi_logic'),
        (vim.vm.device.VirtualLsiLogicSASController, 'lsi_logic_sas'),
        (vim.vm.device.VirtualSCSIController, 'scsi'),
        (vim.vm.device.VirtualSIOController, 'sio'),
        (vim.vm.device.VirtualUSBController, 'usb'),
        (vim.vm.device.VirtualUSBXHCIController, 'usb_xhci'),
    )
    type_names = {
        'ide': _('Virtual IDE controller'),
        'nvme': _('Virtual VNME controller'),
        'pci': _('Virtual PCI controller'),
        'ps2': _('Virtual controller for keyboards and mice'),
        'ahci': _('Virtual AHCI SATA controller'),
        'sata': _('Virtual SATA controller'),
        'para_virt_scsi': _('Virtual paravirtualized SCSI controller'),
        'bus_logic': _('Virtual BusLogic SCSI controller'),
        'lsi_logic': _('Virtual LSI SCSI controller'),
        'lsi_logic_sas': _('Virtual LSI Logic SAS SCSI controller'),
        'scsi': _('Virtual SCSI controller'),
        'sio': _(
            'Virtual Super IO Controller for floppy drives, parallel ports, and serial ports'),
        'usb': _('Virtual USB controller (USB 1.1 and 2.0)'),
        'usb_xhci': _('Virtual USB Extensible Host Controller Interface (USB 3.0)'),
        'unknown': _('Unknown virtual controller'),
    }

    default_conroller_type = 'para_virt_scsi'

    # -------------------------------------------------------------------------
    @classmethod
    def get_disk_controller_class(cls, type_name=None):
        """Search the PyVmomi class for the DiskController by the given type name."""
        if not type_name:
            type_name = cls.default_conroller_type

        ctrl_class = None

        for pair in cls.ctrl_types:
            if pair[1] == type_name:
                ctrl_class = pair[0]
                break

        if not ctrl_class:
            raise VSphereDiskCtrlrTypeNotFoudError(type_name)

        desc = type_name
        if type_name in cls.type_names:
            desc = cls.type_names[type_name]

        return (ctrl_class, desc, type_name)

    # -------------------------------------------------------------------------
    def __init__(
        self, appname=None, verbose=0, version=__version__, base_dir=None, initialized=None,
            ctrl_type='unknown', bus_nr=None, devices=None, hot_add_remove=False,
            scsi_ctrl_nr=None, sharing=None):
        """Initialize a VsphereDiskController object."""
        self._ctrl_type = 'unknown'
        self._bus_nr = None
        self.devices = []
        self._hot_add_remove = False
        self._scsi_ctrl_nr = None
        self._sharing = None

        super(VsphereDiskController, self).__init__(
            appname=appname, verbose=verbose, version=version,
            base_dir=base_dir, initialized=False)

        self.ctrl_type = ctrl_type
        self.bus_nr = bus_nr
        if devices:
            for dev_nr in devices:
                self.devices.append(int(dev_nr))
        self.hot_add_remove = hot_add_remove
        self.scsi_ctrl_nr = scsi_ctrl_nr
        self.sharing = sharing

        if initialized is not None:
            self.initialized = initialized

    # -----------------------------------------------------------
    @property
    def ctrl_type(self):
        """Return the type of this virtual disk controller."""
        return self._ctrl_type

    @ctrl_type.setter
    def ctrl_type(self, value):
        if value is None:
            self._ctrl_type = None
            return
        v = str(value).strip()
        if v == '':
            self._ctrl_type = None
            return
        self._ctrl_type = v

    # -----------------------------------------------------------
    @property
    def ctrl_type_name(self):
        """Return the verbose name of the controller type."""
        if self.ctrl_type is None:
            return None
        if self.ctrl_type not in self.type_names:
            return self.type_names['unknown']
        return self.type_names[self.ctrl_type]

    # -----------------------------------------------------------
    @property
    def bus_nr(self):
        """Bus number associated with this controller."""
        return self._bus_nr

    @bus_nr.setter
    def bus_nr(self, value):
        if value is None:
            self._bus_nr = None
            return
        self._bus_nr = int(value)

    # -----------------------------------------------------------
    @property
    def hot_add_remove(self):
        """All SCSI controllers support hot adding and removing of devices."""
        return self._hot_add_remove

    @hot_add_remove.setter
    def hot_add_remove(self, value):
        self._hot_add_remove = to_bool(value)

    # -----------------------------------------------------------
    @property
    def scsi_ctrl_nr(self):
        """Return the unit number of the SCSI controller."""
        return self._scsi_ctrl_nr

    @scsi_ctrl_nr.setter
    def scsi_ctrl_nr(self, value):
        if value is None:
            self._scsi_ctrl_nr = None
            return
        self._scsi_ctrl_nr = int(value)

    # -----------------------------------------------------------
    @property
    def sharing(self):
        """Mode for sharing the SCSI bus."""
        return self._sharing

    @sharing.setter
    def sharing(self, value):
        if value is None:
            self._sharing = None
            return
        v = str(value).strip()
        if v == '':
            self._sharing = None
            return
        self._sharing = v

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        """Magic method for using it as the '=='-operator."""
        if self.verbose > 4:
            LOG.debug(_('Comparing {} objects ...').format(self.__class__.__name__))

        if not isinstance(other, VsphereDiskController):
            return False

        if self.ctrl_type != other.ctrl_type:
            return False
        if self.bus_nr != other.bus_nr:
            return False
        if self.hot_add_remove != other.hot_add_remove:
            return False
        if self.scsi_ctrl_nr != other.scsi_ctrl_nr:
            return False

        return True

    # -------------------------------------------------------------------------
    def as_dict(self, short=True, bare=False):
        """
        Transform the elements of the object into a dict.

        @param short: don't include local properties in resulting dict.
        @type short: bool
        @param bare: don't include generic fields in returning dict
        @type bare: bool

        @return: structure as dict
        @rtype:  dict
        """
        if bare:
            res = {
                'ctrl_type': self.ctrl_type,
                'ctrl_type_name': self.ctrl_type_name,
                'bus_nr': self.bus_nr,
                'hot_add_remove': self.hot_add_remove,
                'scsi_ctrl_nr': self.scsi_ctrl_nr,
                'sharing': self.sharing,
                'devices': copy.copy(self.devices),
            }
            return res

        res = super(VsphereDiskController, self).as_dict(short=short)
        res['ctrl_type'] = self.ctrl_type
        res['ctrl_type_name'] = self.ctrl_type_name
        res['bus_nr'] = self.bus_nr
        res['hot_add_remove'] = self.hot_add_remove
        res['scsi_ctrl_nr'] = self.scsi_ctrl_nr
        res['sharing'] = self.sharing
        res['devices'] = copy.copy(self.devices),

        return res

    # -------------------------------------------------------------------------
    def __copy__(self):
        """Return a new VsphereDiskController as a deep copy of the current object."""
        ctrl = VsphereDiskController(
            appname=self.appname, verbose=self.verbose, base_dir=self.base_dir,
            initialized=self.initialized, ctrl_type=self.ctrl_type, bus_nr=self.bus_nr,
            hot_add_remove=self.hot_add_remove, scsi_ctrl_nr=self.scsi_ctrl_nr,
            sharing=self.sharing, devices=self.devices)

        return ctrl

    # -------------------------------------------------------------------------
    @classmethod
    def from_summary(cls, data, appname=None, verbose=0, base_dir=None, test_mode=False):
        """Create a new VsphereDiskController object based on the data given from pyvmomi."""
        if test_mode:

            necessary_fields = ('busNumber', 'disk')

            failing_fields = []

            for field in necessary_fields:
                if not hasattr(data, field):
                    failing_fields.append(field)

            if len(failing_fields):
                msg = _(
                    'The given parameter {p!r} on calling method {m}() has failing '
                    'attributes').format(p='data', m='from_summary')
                msg += ': ' + format_list(failing_fields, do_repr=True)
                raise AssertionError(msg)

        else:

            if not isinstance(data, vim.vm.device.VirtualController):
                msg = _('Parameter {t!r} must be a {e}, {v!r} ({vt}) was given.').format(
                    t='data', e='vim.vm.device.VirtualController',
                    v=data, vt=data.__class__.__name__)
                raise TypeError(msg)

        params = {
            'appname': appname,
            'verbose': verbose,
            'base_dir': base_dir,
            'initialized': True,
            'bus_nr': data.busNumber,
            'devices': [],
            'ctrl_type': 'unknown',
        }
        for disk_id in data.device:
            params['devices'].append(disk_id)
        if isinstance(data, vim.vm.device.VirtualSCSIController):
            params['hot_add_remove'] = data.hotAddRemove
            params['scsi_ctrl_nr'] = data.scsiCtlrUnitNumber
            params['sharing'] = data.sharedBus

        if verbose > 2:
            LOG.debug(_('Checking class of controller: {!r}').format(data.__class__.__name__))

        try:
            for pair in cls.ctrl_types:
                if isinstance(data, pair[0]):
                    params['ctrl_type'] = pair[1]
                    break
        except Exception:
            pass

        if verbose > 2:
            LOG.debug(_('Creating {} object from:').format(cls.__name__) + '\n' + pp(params))

        ctrl = cls(**params)

        if verbose > 2:
            LOG.debug(_('Created {} object:').format(cls.__name__) + '\n' + pp(ctrl.as_dict()))

        return ctrl


# =============================================================================
class VsphereDiskControllerList(FbBaseObject, MutableSequence):
    """A list containing VsphereDiskController objects."""

    msg_no_controller = _('Invalid type {t!r} as an item of a {c}, only {o} objects are allowed.')

    # -------------------------------------------------------------------------
    def __init__(
        self, appname=None, verbose=0, version=__version__, base_dir=None,
            initialized=None, *ctrls):
        """Initialize a VsphereDiskControllerList object."""
        self._list = []

        super(VsphereDiskControllerList, self).__init__(
            appname=appname, verbose=verbose, version=version, base_dir=base_dir,
            initialized=False)

        for ctrl in ctrls:
            self.append(ctrl)

        if initialized is not None:
            self.initialized = initialized

    # -------------------------------------------------------------------------
    def as_dict(self, short=True, bare=False):
        """
        Transform the elements of the object into a dict.

        @param short: don't include local properties in resulting dict.
        @type short: bool
        @param bare: don't include generic fields in returning dict
        @type bare: bool

        @return: structure as dict or list
        @rtype:  dict or list
        """
        if bare:
            res = []
            for ctrl in self:
                res.append(ctrl.as_dict(bare=True))
            return res

        res = super(VsphereDiskControllerList, self).as_dict(short=short)
        res['_list'] = []

        for ctrl in self:
            res['_list'].append(ctrl.as_dict(short=short))

        return res

    # -------------------------------------------------------------------------
    def __copy__(self):
        """Return a new VsphereDiskControllerList as a deep copy of the current object."""
        new_list = VsphereDiskControllerList(
            appname=self.appname, verbose=self.verbose,
            base_dir=self.base_dir, initialized=False)

        for ctrl in self:
            new_list.append(ctrl)

        new_list.initialized = self.initialized
        return new_list

    # -------------------------------------------------------------------------
    def index(self, ctrl, *args):
        """Return the numeric index of the given controller in current list."""
        i = None
        j = None

        if len(args) > 0:
            if len(args) > 2:
                raise TypeError(_('{m} takes at most {max} arguments ({n} given).').format(
                    m='index()', max=3, n=len(args) + 1))
            i = int(args[0])
            if len(args) > 1:
                j = int(args[1])

        index = 0
        start = 0
        if i is not None:
            start = i
            if i < 0:
                start = len(self._list) + i

        wrap = False
        end = len(self._list)
        if j is not None:
            if j < 0:
                end = len(self._list) + j
                if end < index:
                    wrap = True
            else:
                end = j
        for index in list(range(len(self._list))):
            item = self._list[index]
            if index < start:
                continue
            if index >= end and not wrap:
                break
            if item == ctrl:
                return index

        if wrap:
            for index in list(range(len(self._list))):
                item = self._list[index]
                if index >= end:
                    break
            if item == ctrl:
                return index

        msg = _('Controller is not in controller list.')
        raise ValueError(msg)

    # -------------------------------------------------------------------------
    def __contains__(self, ctrl):
        """Return whether the given controller is contained in current list."""
        if not isinstance(ctrl, VsphereDiskController):
            raise TypeError(self.msg_no_controller.format(
                t=ctrl.__class__.__name__, c=self.__class__.__name__, o='VsphereDiskController'))

        if not self._list:
            return False

        for item in self._list:
            if item == ctrl:
                return True

        return False

    # -------------------------------------------------------------------------
    def count(self, ctrl):
        """Return the number of controllers which are equal to the given one in current list."""
        if not isinstance(ctrl, VsphereDiskController):
            raise TypeError(self.msg_no_controller.format(
                t=ctrl.__class__.__name__, c=self.__class__.__name__, o='VsphereDiskController'))

        if not self._list:
            return 0

        num = 0
        for item in self._list:
            if item == ctrl:
                num += 1
        return num

    # -------------------------------------------------------------------------
    def __len__(self):
        """Return the number of controllers in current list."""
        return len(self._list)

    # -------------------------------------------------------------------------
    def __iter__(self):
        """Iterate through all controllers in current list."""
        for item in self._list:
            yield item

    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """Get a controller from current list by the given numeric index."""
        return self._list.__getitem__(key)

    # -------------------------------------------------------------------------
    def __reversed__(self):
        """Reverse the controllers in list in place."""
        return reversed(self._list)

    # -------------------------------------------------------------------------
    def __setitem__(self, key, ctrl):
        """Replace the controller at the given numeric index by the given one."""
        if not isinstance(ctrl, VsphereDiskController):
            raise TypeError(self.msg_no_controller.format(
                t=ctrl.__class__.__name__, c=self.__class__.__name__, o='VsphereDiskController'))

        self._list.__setitem__(key, ctrl)

    # -------------------------------------------------------------------------
    def __delitem__(self, key):
        """Remove the controller at the given numeric index from list."""
        del self._list[key]

    # -------------------------------------------------------------------------
    def append(self, ctrl):
        """Append the given controller to the current list."""
        if not isinstance(ctrl, VsphereDiskController):
            raise TypeError(self.msg_no_controller.format(
                t=ctrl.__class__.__name__, c=self.__class__.__name__, o='VsphereDiskController'))

        self._list.append(ctrl)

    # -------------------------------------------------------------------------
    def insert(self, index, ctrl):
        """Insert the given controller in current list at given index."""
        if not isinstance(ctrl, VsphereDiskController):
            raise TypeError(self.msg_no_controller.format(
                t=ctrl.__class__.__name__, c=self.__class__.__name__, o='VsphereDiskController'))

        self._list.insert(index, ctrl)

    # -------------------------------------------------------------------------
    def clear(self):
        """Remove all items from the VsphereDiskControllerList."""
        self._list = []


# =============================================================================
if __name__ == '__main__':

    pass

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 list
