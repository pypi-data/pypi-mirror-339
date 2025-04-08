#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: The module for a VSphere datastore object.

@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2025 by Frank Brehm, Berlin
"""
from __future__ import absolute_import

# Standard modules
import logging
import random
import re
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping

# Third party modules
from fb_tools.common import pp, to_bool
from fb_tools.obj import FbGenericBaseObject
from fb_tools.xlate import format_list

from pyVmomi import vim

# Own modules
from .obj import VsphereObject
from .xlate import XLATOR

__version__ = '1.4.4'
LOG = logging.getLogger(__name__)

_ = XLATOR.gettext


# =============================================================================
class VsphereDatastore(VsphereObject):
    """Wrapper class for a VSphere datastore object."""

    re_is_nfs = re.compile(r'(?:share[_-]*nfs|nfs[_-]*share)', re.IGNORECASE)
    re_vmcb_fs = re.compile(r'vmcb-\d+-fc-\d+', re.IGNORECASE)
    re_local_ds = re.compile(r'^local_', re.IGNORECASE)
    re_k8s_ds = re.compile(r'[_-](?:k8s|kubernetes)[_-]', re.IGNORECASE)

    # -------------------------------------------------------------------------
    def __init__(
        self, appname=None, verbose=0, version=__version__, base_dir=None, initialized=None,
            name=None, status='gray', config_status='gray', accessible=True, capacity=None,
            free_space=None, maintenance_mode=None, multiple_host_access=True, fs_type=None,
            uncommitted=None, url=None, for_k8s=None):
        """Initialize the VsphereDatastore object."""
        self.repr_fields = (
            'name', 'status', 'accessible', 'capacity', 'free_space', 'fs_type', 'storage_type',
            'appname', 'verbose', 'version')

        self._accessible = bool(accessible)
        self._capacity = int(capacity)
        self._free_space = int(free_space)
        self._maintenance_mode = 'normal'
        if maintenance_mode is not None:
            self._maintenance_mode = str(maintenance_mode)
        self._multiple_host_access = bool(multiple_host_access)
        self._fs_type = 'unknown'
        if fs_type is not None:
            self._fs_type = fs_type
        self._uncommitted = 0
        if uncommitted is not None:
            self._uncommitted = int(uncommitted)
        self._url = None
        if url is not None:
            self._url = str(url)
        self._for_k8s = False

        self._storage_type = 'unknown'

        self._calculated_usage = 0.0

        super(VsphereDatastore, self).__init__(
            name=name, obj_type='vsphere_datastore', name_prefix='ds', status=status,
            config_status=config_status, appname=appname, verbose=verbose,
            version=version, base_dir=base_dir)

        st_type = self.storage_type_by_name(self.name)
        if st_type:
            self._storage_type = st_type

        if for_k8s is not None:
            self.for_k8s = for_k8s
        else:
            self.for_k8s = self.detect_k8s(self.name)

        if initialized is not None:
            self.initialized = initialized

    # -----------------------------------------------------------
    @property
    def accessible(self):
        """Return the connectivity status of this datastore."""
        return self._accessible

    # -----------------------------------------------------------
    @property
    def capacity(self):
        """Return the maximum capacity of this datastore, in bytes."""
        return self._capacity

    # -----------------------------------------------------------
    @property
    def capacity_gb(self):
        """Return the maximum capacity of this datastore, in GiBytes."""
        return float(self.capacity) / 1024.0 / 1024.0 / 1024.0

    # -----------------------------------------------------------
    @property
    def free_space(self):
        """Return the available space of this datastore, in bytes."""
        return self._free_space

    # -----------------------------------------------------------
    @property
    def free_space_gb(self):
        """Return the vailable space of this datastore, in GiBytes."""
        return float(self._free_space) / 1024.0 / 1024.0 / 1024.0

    # -----------------------------------------------------------
    @property
    def maintenance_mode(self):
        """Return the current maintenance mode state of the datastore."""
        return self._maintenance_mode

    # -----------------------------------------------------------
    @property
    def multiple_host_access(self):
        """More than one host has been configured with access to the datastore."""
        return self._multiple_host_access

    # -----------------------------------------------------------
    @property
    def fs_type(self):
        """Return the type of file system volume, such as VMFS or NFS."""
        return self._fs_type

    # -----------------------------------------------------------
    @property
    def uncommitted(self):
        """
        Total additional storage space, in bytes.

        This is potentially used by all virtual machines on this datastore.
        """
        return self._uncommitted

    # -----------------------------------------------------------
    @property
    def uncommitted_gb(self):
        """
        Total additional storage space, in GiBytes.

        This is potentially used by all virtual machines on this datastore.
        """
        return float(self._uncommitted) / 1024.0 / 1024.0 / 1024.0

    # -----------------------------------------------------------
    @property
    def url(self):
        """Return he unique locator for the datastore."""
        return self._url

    # -----------------------------------------------------------
    @property
    def for_k8s(self):
        """Return, whther this datastore is intended to use for Kubernetes PV."""
        return self._for_k8s

    @for_k8s.setter
    def for_k8s(self, value):
        self._for_k8s = to_bool(value)

    # -----------------------------------------------------------
    @property
    def storage_type(self):
        """Return the type of storage volume, such as SAS or SATA or SSD."""
        return self._storage_type

    # -----------------------------------------------------------
    @property
    def calculated_usage(self):
        """Return the calculated additional usage of this datastore, in GiBytes."""
        return self._calculated_usage

    @calculated_usage.setter
    def calculated_usage(self, value):
        val = float(value)
        self._calculated_usage = val

    # -----------------------------------------------------------
    @property
    def avail_space_gb(self):
        """Available space of datastore in GiB in respect of calculated space."""
        if not self.free_space:
            return 0.0
        if not self.calculated_usage:
            return self.free_space_gb
        return self.free_space_gb - self.calculated_usage

    # -------------------------------------------------------------------------
    @classmethod
    def from_summary(cls, data, appname=None, verbose=0, base_dir=None, test_mode=False):
        """Create a new VsphereDatastore object based on the data given from pyvmomi module."""
        if test_mode:

            necessary_fields = ('summary', 'overallStatus', 'configStatus')
            summary_fields = ('capacity', 'freeSpace', 'name', 'type', 'url')

            failing_fields = []

            for field in necessary_fields:
                if not hasattr(data, field):
                    failing_fields.append(field)

            if hasattr(data, 'summary') and data.summary:
                summary = data.summary
                for field in summary_fields:
                    if not hasattr(summary, field):
                        failing_fields.append('summary.' + field)

            if len(failing_fields):
                msg = _(
                    'The given parameter {p!r} on calling method {m}() has failing '
                    'attributes').format(p='data', m='from_summary')
                msg += ': ' + format_list(failing_fields, do_repr=True)
                raise AssertionError(msg)

        else:

            if not isinstance(data, vim.Datastore):
                msg = _('Parameter {t!r} must be a {e}, {v!r} was given.').format(
                    t='data', e='vim.Datastore', v=data)
                raise TypeError(msg)

        params = {
            'appname': appname,
            'verbose': verbose,
            'base_dir': base_dir,
            'initialized': True,
            'capacity': data.summary.capacity,
            'free_space': data.summary.freeSpace,
            'name': data.summary.name,
            'fs_type': data.summary.type,
            'url': data.summary.url,
            'status': data.overallStatus,
            'config_status': data.configStatus,
        }

        if hasattr(data.summary, 'accessible'):
            params['accessible'] = data.summary.accessible

        if hasattr(data.summary, 'maintenanceMode'):
            params['maintenance_mode'] = data.summary.maintenanceMode

        if hasattr(data.summary, 'multipleHostAccess'):
            params['multiple_host_access'] = data.summary.multipleHostAccess

        if hasattr(data.summary, 'uncommitted'):
            params['uncommitted'] = data.summary.uncommitted

        if verbose > 2:
            LOG.debug(_('Creating {} object from:').format(cls.__name__) + '\n' + pp(params))

        ds = cls(**params)
        return ds

    # -------------------------------------------------------------------------
    @classmethod
    def storage_type_by_name(cls, name):
        """Guess the storage type by its name. May be overridden in descentant classes."""
        if cls.re_is_nfs.search(name):
            return 'NFS'

        if '-sas-' in name.lower():
            return 'SAS'

        if '-ssd-' in name.lower():
            return 'SSD'

        if '-sata-' in name.lower():
            return 'SATA'

        if cls.re_vmcb_fs.search(name):
            return 'SATA'

        if cls.re_local_ds.search(name):
            return 'LOCAL'

        return None

    # -------------------------------------------------------------------------
    @classmethod
    def detect_k8s(cls, name):
        """
        Is the datastore intended to use as PV in Kubernetes or not.

        This detection is made on evaluating the datastore name.
        """
        if cls.re_k8s_ds.search(name):
            return True
        return False

    # -------------------------------------------------------------------------
    def as_dict(self, short=True):
        """
        Transform the elements of the object into a dict.

        @param short: don't include local properties in resulting dict.
        @type short: bool

        @return: structure as dict
        @rtype:  dict
        """
        res = super(VsphereDatastore, self).as_dict(short=short)
        res['accessible'] = self.accessible
        res['capacity'] = self.capacity
        res['capacity_gb'] = self.capacity_gb
        res['free_space'] = self.free_space
        res['free_space_gb'] = self.free_space_gb
        res['maintenance_mode'] = self.maintenance_mode
        res['multiple_host_access'] = self.multiple_host_access
        res['fs_type'] = self.fs_type
        res['for_k8s'] = self.for_k8s
        res['uncommitted'] = self.uncommitted
        res['uncommitted_gb'] = self.uncommitted_gb
        res['url'] = self.url
        res['storage_type'] = self.storage_type
        res['calculated_usage'] = self.calculated_usage
        res['avail_space_gb'] = self.avail_space_gb

        return res

    # -------------------------------------------------------------------------
    def __copy__(self):
        """Return a new VsphereDatastore object with data from current object copied in."""
        return VsphereDatastore(
            appname=self.appname, verbose=self.verbose, base_dir=self.base_dir,
            initialized=self.initialized, name=self.name, accessible=self.accessible,
            capacity=self.capacity, free_space=self.free_space, for_k8s=self.for_k8s,
            maintenance_mode=self.maintenance_mode, multiple_host_access=self.multiple_host_access,
            fs_type=self.fs_type, uncommitted=self.uncommitted, url=self.url,
            status=self.status, config_status=self.config_status)

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        """Magic method for using it as the '=='-operator."""
        if self.verbose > 4:
            LOG.debug(_('Comparing {} objects ...').format(self.__class__.__name__))

        if not isinstance(other, VsphereDatastore):
            return False

        if self.name != other.name:
            return False

        return True


# =============================================================================
class VsphereDatastoreDict(MutableMapping, FbGenericBaseObject):
    """
    A dictionary containing VsphereDatastore objects.

    It works like a dict.
    """

    msg_invalid_ds_type = _('Invalid item type {{!r}} to set, only {} allowed.').format(
        'VsphereDatastore')
    msg_key_not_name = _('The key {k!r} must be equal to the datastore name {n!r}.')
    msg_none_type_error = _('None type as key is not allowed.')
    msg_empty_key_error = _('Empty key {!r} is not allowed.')
    msg_no_ds_dict = _('Object {{!r}} is not a {} object.').format('VsphereDatastoreDict')

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Initialize a VsphereDatastoreDict object."""
        self._map = {}

        for arg in args:
            self.append(arg)

    # -------------------------------------------------------------------------
    def _set_item(self, key, ds):

        if not isinstance(ds, VsphereDatastore):
            raise TypeError(self.msg_invalid_ds_type.format(ds.__class__.__name__))

        ds_name = ds.name
        if ds_name != key:
            raise KeyError(self.msg_key_not_name.format(k=key, n=ds_name))

        self._map[ds_name] = ds

    # -------------------------------------------------------------------------
    def append(self, ds):
        """Set the given datastore in the current dict with its name as key."""
        if not isinstance(ds, VsphereDatastore):
            raise TypeError(self.msg_invalid_ds_type.format(ds.__class__.__name__))
        self._set_item(ds.name, ds)

    # -------------------------------------------------------------------------
    def _get_item(self, key):

        if key is None:
            raise TypeError(self.msg_none_type_error)

        ds_name = str(key).strip()
        if ds_name == '':
            raise ValueError(self.msg_empty_key_error.format(key))

        return self._map[ds_name]

    # -------------------------------------------------------------------------
    def get(self, key):
        """Get the datastore from dict by its name."""
        return self._get_item(key)

    # -------------------------------------------------------------------------
    def _del_item(self, key, strict=True):

        if key is None:
            raise TypeError(self.msg_none_type_error)

        ds_name = str(key).strip()
        if ds_name == '':
            raise ValueError(self.msg_empty_key_error.format(key))

        if not strict and ds_name not in self._map:
            return

        del self._map[ds_name]

    # -------------------------------------------------------------------------
    # The next five methods are requirements of the ABC.
    def __setitem__(self, key, value):
        """Set the given datastore in the current dict by key."""
        self._set_item(key, value)

    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """Get the datastore from dict by the key."""
        return self._get_item(key)

    # -------------------------------------------------------------------------
    def __delitem__(self, key):
        """Remove the datastore from dict by the key."""
        self._del_item(key)

    # -------------------------------------------------------------------------
    def __iter__(self):
        """Iterate through datastore names as keys."""
        for ds_name in self.keys():
            yield ds_name

    # -------------------------------------------------------------------------
    def __len__(self):
        """Return the number of datastores in current dict."""
        return len(self._map)

    # -------------------------------------------------------------------------
    # The next methods aren't required, but nice for different purposes:
    def __str__(self):
        """Return a simple dict representation of the mapping."""
        return str(self._map)

    # -------------------------------------------------------------------------
    def __repr__(self):
        """Transform into a string for reproduction."""
        return '{}, {}({})'.format(
            super(VsphereDatastoreDict, self).__repr__(),
            self.__class__.__name__,
            self._map)

    # -------------------------------------------------------------------------
    def __contains__(self, key):
        """Return whether the given datastore name is contained in current dict as a key."""
        if key is None:
            raise TypeError(self.msg_none_type_error)

        ds_name = str(key).strip()
        if ds_name == '':
            raise ValueError(self.msg_empty_key_error.format(key))

        return ds_name in self._map

    # -------------------------------------------------------------------------
    def keys(self):
        """Return all datastore names of this dict in a sorted manner."""
        return sorted(self._map.keys(), key=str.lower)

    # -------------------------------------------------------------------------
    def items(self):
        """Return tuples (datastore name + object as tuple) of this dict in a sorted manner."""
        item_list = []

        for ds_name in self.keys():
            item_list.append((ds_name, self._map[ds_name]))

        return item_list

    # -------------------------------------------------------------------------
    def values(self):
        """Return all datastore objects of this dict."""
        value_list = []
        for ds_name in self.keys():
            value_list.append(self._map[ds_name])
        return value_list

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        """Magic method for using it as the '=='-operator."""
        if not isinstance(other, VsphereDatastoreDict):
            raise TypeError(self.msg_no_ds_dict.format(other))

        return self._map == other._map

    # -------------------------------------------------------------------------
    def __ne__(self, other):
        """Magic method for using it as the '!='-operator."""
        if not isinstance(other, VsphereDatastoreDict):
            raise TypeError(self.msg_no_ds_dict.format(other))

        return self._map != other._map

    # -------------------------------------------------------------------------
    def pop(self, key, *args):
        """Get the datastore by its name and remove it in dict."""
        if key is None:
            raise TypeError(self.msg_none_type_error)

        ds_name = str(key).strip()
        if ds_name == '':
            raise ValueError(self.msg_empty_key_error.format(key))

        return self._map.pop(ds_name, *args)

    # -------------------------------------------------------------------------
    def popitem(self):
        """Remove and return a arbitrary (datastore name and object) pair from the dictionary."""
        if not len(self._map):
            return None

        ds_name = self.keys()[0]
        ds = self._map[ds_name]
        del self._map[ds_name]
        return (ds_name, ds)

    # -------------------------------------------------------------------------
    def clear(self):
        """Remove all items from the dictionary."""
        self._map = {}

    # -------------------------------------------------------------------------
    def setdefault(self, key, default):
        """
        Return the datastore, if the key is in dict.

        If not, insert key with a value of default and return default.
        """
        if key is None:
            raise TypeError(self.msg_none_type_error)

        ds_name = str(key).strip()
        if ds_name == '':
            raise ValueError(self.msg_empty_key_error.format(key))

        if not isinstance(default, VsphereDatastore):
            raise TypeError(self.msg_invalid_ds_type.format(default.__class__.__name__))

        if ds_name in self._map:
            return self._map[ds_name]

        self._set_item(ds_name, default)
        return default

    # -------------------------------------------------------------------------
    def update(self, other):
        """Update the dict with the key/value pairs from other, overwriting existing keys."""
        if isinstance(other, VsphereDatastoreDict) or isinstance(other, dict):
            for ds_name in other.keys():
                self._set_item(ds_name, other[ds_name])
            return

        for tokens in other:
            key = tokens[0]
            value = tokens[1]
            self._set_item(key, value)

    # -------------------------------------------------------------------------
    def as_dict(self, short=True):
        """Transform the elements of the object into a dict."""
        res = {}
        for ds_name in self._map:
            res[ds_name] = self._map[ds_name].as_dict(short)
        return res

    # -------------------------------------------------------------------------
    def as_list(self, short=True):
        """Return a list with all datastores transformed to a dict."""
        res = []
        for ds_name in self.keys():
            res.append(self._map[ds_name].as_dict(short))
        return res

    # -------------------------------------------------------------------------
    def find_ds(self, needed_gb, ds_type='sata', reserve_space=True, use_ds=None, no_k8s=False):
        """Find a datastore in dict with the given minimum free space and the given type."""
        search_chains = {
            'sata': ('sata', 'sas', 'ssd'),
            'sas': ('sas', 'sata', 'ssd'),
            'ssd': ('ssd', 'sas', 'sata'),
        }

        if ds_type not in search_chains:
            raise ValueError(_('Could not handle datastore type {!r}.').format(ds_type))
        for dstp in search_chains[ds_type]:
            ds_name = self._find_ds(
                needed_gb, dstp, reserve_space, use_ds=use_ds, no_k8s=no_k8s)
            if ds_name:
                return ds_name

        LOG.error(_('Could not found a datastore for {c:0.1f} GiB of type {t!r}.').format(
            c=needed_gb, t=ds_type))
        return None

    # -------------------------------------------------------------------------
    def _find_ds(self, needed_gb, ds_type, reserve_space=True, use_ds=None, no_k8s=False):

        LOG.debug(_('Searching datastore for {c:0.1f} GiB of type {t!r}.').format(
            c=needed_gb, t=ds_type))

        avail_ds_names = []
        for (ds_name, ds) in self.items():
            if use_ds:
                if ds.name not in use_ds:
                    continue
            if ds.storage_type.lower() != ds_type.lower():
                continue
            if no_k8s and ds.for_k8s:
                continue
            if ds.avail_space_gb >= needed_gb:
                avail_ds_names.append(ds_name)

        if not avail_ds_names:
            return None

        ds_name = random.choice(avail_ds_names)
        if reserve_space:
            ds = self[ds_name]
            ds.calculated_usage += needed_gb

        return ds_name


# =============================================================================
if __name__ == '__main__':

    pass

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 list
