#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: Mdule for capsulating a VSphere disk object, which can be assigned to a VM.

@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2025 by Frank Brehm, Berlin
"""
from __future__ import absolute_import

# Standard modules
import logging
import re
import uuid
try:
    from collections.abc import MutableSequence
except ImportError:
    from collections import MutableSequence

# Third party modules
from fb_tools.common import pp
from fb_tools.obj import FbBaseObject
from fb_tools.xlate import format_list

from pyVmomi import vim

# Own modules
from .xlate import XLATOR

__version__ = '1.0.1'
LOG = logging.getLogger(__name__)

_ = XLATOR.gettext


# =============================================================================
class VsphereDisk(FbBaseObject):
    """Encapsulation of a VSphere disk object, which can be assigned to a VM."""

    re_file_storage = re.compile(r'^\s*\[\s*([^\s\]]+)')
    re_file_rel = re.compile(r'^\s*\[[^\]]*]\s*(\S.*)\s*$')

    # -------------------------------------------------------------------------
    def __init__(
        self, appname=None, verbose=0, version=__version__, base_dir=None, initialized=None,
            uuid=None, file_name=None, unit_nr=None, label=None, key=None, controller_key=None,
            size=None, disk_id=None, summary=None):
        """Initialize a VsphereDisk object."""
        # self.repr_fields = (
        #     'uuid', 'file_name', 'unit_nr', 'label', 'key', 'controller_key',
        #     'size', 'disk_id', 'appname', 'verbose')
        self._uuid = None
        self._file_name = None
        self._unit_nr = None
        self._label = None
        self._summary = None
        self._key = None
        self._controller_key = None
        self._size = None
        self._disk_id = None

        super(VsphereDisk, self).__init__(
            appname=appname, verbose=verbose, version=version,
            base_dir=base_dir, initialized=False)

        self.uuid = uuid
        self.file_name = file_name
        self.unit_nr = unit_nr
        self.label = label
        self.summary = summary
        self.key = key
        self.controller_key = controller_key
        self.size = size
        self.disk_id = disk_id

        if initialized is not None:
            self.initialized = initialized

    # -----------------------------------------------------------
    @property
    def uuid(self):
        """Return the UUID of the disk."""
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        if value is None:
            self._uuid = None
            return
        v = str(value).strip()
        if v == '':
            self._uuid = None
            return
        try:
            self._uuid = uuid.UUID(v)
        except Exception:
            self._uuid = v

    # -----------------------------------------------------------
    @property
    def file_name(self):
        """Return the name of the backing device on the host system."""
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        if value is None:
            self._file_name = None
            return
        v = str(value).strip()
        if v == '':
            self._file_name = None
            return
        self._file_name = v

    # -----------------------------------------------------------
    @property
    def file_storage(self):
        """Return the name of the storage of the backing device on the host system."""
        if self.file_name is None:
            return None
        match = self.re_file_storage.match(self.file_name)
        if match:
            return match.group(1)
        return None

    # -----------------------------------------------------------
    @property
    def file_rel(self):
        """Return the relative path of the backing device on the host system."""
        if self.file_name is None:
            return None
        match = self.re_file_rel.match(self.file_name)
        if match:
            return match.group(1)
        return None

    # -----------------------------------------------------------
    @property
    def unit_nr(self):
        """
        Return the unit number of this device on its controller.

        This property is None if the controller property is None
        (for example, when the device is not attached to a specific controller object).
        """
        return self._unit_nr

    @unit_nr.setter
    def unit_nr(self, value):
        if value is None:
            self._unit_nr = None
            return
        self._unit_nr = int(value)

    # -----------------------------------------------------------
    @property
    def label(self):
        """Return the display label of the disk."""
        return self._label

    @label.setter
    def label(self, value):
        if value is None:
            self._label = None
            return
        v = str(value).strip()
        if v == '':
            self._label = None
            return
        self._label = v

    # -----------------------------------------------------------
    @property
    def summary(self):
        """Return a summary description of the disk."""
        return self._summary

    @summary.setter
    def summary(self, value):
        if value is None:
            self._summary = None
            return
        v = str(value).strip()
        if v == '':
            self._summary = None
            return
        self._summary = v

    # -----------------------------------------------------------
    @property
    def key(self):
        """Return a unique key that distinguishes this device from other devices in the same VM."""
        return self._key

    @key.setter
    def key(self, value):
        if value is None:
            self._key = None
            return
        self._key = int(value)

    # -----------------------------------------------------------
    @property
    def size(self):
        """Return the size of the disk in Bytes."""
        return self._size

    @size.setter
    def size(self, value):
        if value is None:
            self._size = None
            return
        self._size = int(value)

    # -----------------------------------------------------------
    @property
    def size_kb(self):
        """Return the size of the disk in KiBytes."""
        if self.size is None:
            return None
        return int(self.size / 1024)

    # -----------------------------------------------------------
    @property
    def size_mb(self):
        """Return the size of the disk in MiBytes."""
        if self.size is None:
            return None
        return int(self.size / 1024 / 1024)

    # -----------------------------------------------------------
    @property
    def size_gb(self):
        """Return the size of the disk in GiBytes as a float value."""
        if self.size_mb is None:
            return None
        return float(self.size_mb) / 1024.0

    # -----------------------------------------------------------
    @property
    def controller_key(self):
        """Object key for the controller object for this device."""
        return self._controller_key

    @controller_key.setter
    def controller_key(self, value):
        if value is None:
            self._controller_key = None
            return
        self._controller_key = int(value)

    # -----------------------------------------------------------
    @property
    def disk_id(self):
        """TODO whatever."""
        return self._disk_id

    @disk_id.setter
    def disk_id(self, value):
        if value is None:
            self._disk_id = None
            return
        v = str(value).strip()
        if v == '':
            self._disk_id = None
            return
        self._disk_id = v

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        """Magic method for using it as the '=='-operator."""
        if self.verbose > 4:
            LOG.debug(_('Comparing {} objects ...').format(self.__class__.__name__))

        if not isinstance(other, VsphereDisk):
            return False

        if self.uuid != other.uuid:
            return False
        if self.file_name != other.file_name:
            return False
        if self.unit_nr != other.unit_nr:
            return False
        if self.label != other.label:
            return False
        if self.summary != other.summary:
            return False
        if self.key != other.key:
            return False
        if self.size != other.size:
            return False
        if self.controller_key != other.controller_key:
            return False
        if self.disk_id != other.disk_id:
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
                'uuid': self.uuid,
                'file_name': self.file_name,
                'file_rel': self.file_rel,
                'file_storage': self.file_storage,
                'unit_nr': self.unit_nr,
                'label': self.label,
                'summary': self.summary,
                'key': self.key,
                'size': self.size,
                'size_kb': self.size_kb,
                'size_mb': self.size_mb,
                'size_gb': self.size_gb,
                'controller_key': self.controller_key,
                'disk_id': self.disk_id,
            }
            return res

        res = super(VsphereDisk, self).as_dict(short=short)
        res['uuid'] = self.uuid
        res['file_name'] = self.file_name
        res['file_rel'] = self.file_rel
        res['file_storage'] = self.file_storage
        res['unit_nr'] = self.unit_nr
        res['label'] = self.label
        res['summary'] = self.summary
        res['key'] = self.key
        res['size'] = self.size
        res['size_kb'] = self.size_kb
        res['size_mb'] = self.size_mb
        res['size_gb'] = self.size_gb
        res['controller_key'] = self.controller_key
        res['disk_id'] = self.disk_id

        return res

    # -------------------------------------------------------------------------
    def __copy__(self):
        """Return a new VsphereDisk as a deep copy of the current object."""
        disk = VsphereDisk(
            appname=self.appname, verbose=self.verbose, base_dir=self.base_dir,
            initialized=self.initialized, uuid=self.uuid, file_name=self.file_name,
            unit_nr=self.unit_nr, label=self.label, key=self.key, size=self.size,
            controller_key=self.controller_key, disk_id=self.disk_id, summary=self.summary)

        return disk

    # -------------------------------------------------------------------------
    @classmethod
    def from_summary(cls, data, appname=None, verbose=0, base_dir=None, test_mode=False):
        """Create a new VsphereDisk object based on the data given from pyvmomi."""
        if test_mode:

            necessary_fields = (
                'unitNumber', 'deviceInfo', 'capacityInBytes', 'key', 'backing',
                'controllerKey', 'vDiskId')

            failing_fields = []

            for field in necessary_fields:
                if not hasattr(data, field):
                    failing_fields.append(field)

            if hasattr(data, 'deviceInfo'):
                dev_info = data.deviceInfo
                for field in ('label', 'summary'):
                    if not hasattr(dev_info, field):
                        failing_fields.append('deviceInfo.' + field)

            if hasattr(data, 'backing') and not hasattr(data.backing, 'fileName'):
                failing_fields.append('backing.fileName')

            if len(failing_fields):
                msg = _(
                    'The given parameter {p!r} on calling method {m}() has failing '
                    'attributes').format(p='data', m='from_summary')
                msg += ': ' + format_list(failing_fields, do_repr=True)
                raise AssertionError(msg)

        else:

            if not isinstance(data, vim.vm.device.VirtualDisk):
                msg = _(
                    'Parameter {t!r} must be a {e} object, a {v} object was given '
                    'instead.').format(
                        t='data', e='vim.vm.device.VirtualDisk', v=data.__class__.__qualname__)
                raise TypeError(msg)

        params = {
            'appname': appname,
            'verbose': verbose,
            'base_dir': base_dir,
            'initialized': True,
            'unit_nr': data.unitNumber,
            'label': data.deviceInfo.label,
            'summary': data.deviceInfo.summary,
            'size': data.capacityInBytes,
            'key': data.key,
            'file_name': data.backing.fileName,
            'controller_key': data.controllerKey,
            'disk_id': data.vDiskId,
        }

        if verbose > 2:
            LOG.debug(_('Creating {} object from:').format(cls.__name__) + '\n' + pp(params))

        disk = cls(**params)

        if verbose > 2:
            LOG.debug(_('Created {} object:').format(cls.__name__) + '\n' + pp(disk.as_dict()))

        return disk


# =============================================================================
class VsphereDiskList(FbBaseObject, MutableSequence):
    """A list containing VsphereDisk objects."""

    msg_no_disk = _('Invalid type {t!r} as an item of a {c}, only {o} objects are allowed.')

    # -------------------------------------------------------------------------
    def __init__(
        self, appname=None, verbose=0, version=__version__, base_dir=None,
            initialized=None, *disks):
        """Initialize a VsphereDiskList object."""
        self._list = []

        super(VsphereDiskList, self).__init__(
            appname=appname, verbose=verbose, version=version, base_dir=base_dir,
            initialized=False)

        for disk in disks:
            self.append(disk)

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
            for disk in self:
                res.append(disk.as_dict(bare=True))
            return res

        res = super(VsphereDiskList, self).as_dict(short=short)
        res['_list'] = []

        for disk in self:
            res['_list'].append(disk.as_dict(short=short))

        return res

    # -------------------------------------------------------------------------
    def __copy__(self):
        """Return a new VsphereDiskList as a deep copy of the current object."""
        new_list = self.__class__(
            appname=self.appname, verbose=self.verbose,
            base_dir=self.base_dir, initialized=False)

        for disk in self:
            new_list.append(disk)

        new_list.initialized = self.initialized
        return new_list

    # -------------------------------------------------------------------------
    def index(self, disk, *args):
        """Return the numeric index of the given disk in current list."""
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
            if item == disk:
                return index

        if wrap:
            for index in list(range(len(self._list))):
                item = self._list[index]
                if index >= end:
                    break
            if item == disk:
                return index

        msg = _('Disk is not in disk list.')
        raise ValueError(msg)

    # -------------------------------------------------------------------------
    def __contains__(self, disk):
        """Return whether the given disk is contained in current list."""
        if not isinstance(disk, VsphereDisk):
            raise TypeError(self.msg_no_disk.format(
                t=disk.__class__.__name__, c=self.__class__.__name__, o='VsphereDisk'))

        if not self._list:
            return False

        for item in self._list:
            if item == disk:
                return True

        return False

    # -------------------------------------------------------------------------
    def count(self, disk):
        """Return the number of disks which are equal to the given one in current list."""
        if not isinstance(disk, VsphereDisk):
            raise TypeError(self.msg_no_disk.format(
                t=disk.__class__.__name__, c=self.__class__.__name__, o='VsphereDisk'))

        if not self._list:
            return 0

        num = 0
        for item in self._list:
            if item == disk:
                num += 1
        return num

    # -------------------------------------------------------------------------
    def __len__(self):
        """Return the number of disks in current list."""
        return len(self._list)

    # -------------------------------------------------------------------------
    def __iter__(self):
        """Iterate through all disks in current list."""
        for item in self._list:
            yield item

    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """Get a disk from current list by the given numeric index."""
        return self._list.__getitem__(key)

    # -------------------------------------------------------------------------
    def __reversed__(self):
        """Reverse the disks in list in place."""
        return reversed(self._list)

    # -------------------------------------------------------------------------
    def __setitem__(self, key, disk):
        """Replace the disk at the given numeric index by the given one."""
        if not isinstance(disk, VsphereDisk):
            raise TypeError(self.msg_no_disk.format(
                t=disk.__class__.__name__, c=self.__class__.__name__, o='VsphereDisk'))

        self._list.__setitem__(key, disk)

    # -------------------------------------------------------------------------
    def __delitem__(self, key):
        """Remove the disk at the given numeric index from list."""
        del self._list[key]

    # -------------------------------------------------------------------------
    def append(self, disk):
        """Append the given disk to the current list."""
        if not isinstance(disk, VsphereDisk):
            raise TypeError(self.msg_no_disk.format(
                t=disk.__class__.__name__, c=self.__class__.__name__, o='VsphereDisk'))

        self._list.append(disk)

    # -------------------------------------------------------------------------
    def insert(self, index, disk):
        """Insert the given disk in current list at given index."""
        if not isinstance(disk, VsphereDisk):
            raise TypeError(self.msg_no_disk.format(
                t=disk.__class__.__name__, c=self.__class__.__name__, o='VsphereDisk'))

        self._list.insert(index, disk)

    # -------------------------------------------------------------------------
    def clear(self):
        """Remove all items from the VsphereDiskList."""
        self._list = []


# =============================================================================
if __name__ == '__main__':

    pass

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 list
