#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: The module for a VSphere virtual machine or template object.

@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2025 by Frank Brehm, Berlin
"""
from __future__ import absolute_import

# Standard modules
import copy
import logging
import re
import uuid
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
from .controller import VsphereDiskController, VsphereDiskControllerList
from .disk import VsphereDisk, VsphereDiskList
from .errors import VSphereHandlerError
from .ether import VsphereEthernetcard, VsphereEthernetcardList
from .obj import DEFAULT_OBJ_STATUS
from .obj import OBJ_STATUS_GREEN
from .obj import VsphereObject
from .xlate import XLATOR

__version__ = '1.0.1'
LOG = logging.getLogger(__name__)

_ = XLATOR.gettext


# =============================================================================
class VsphereVm(VsphereObject):
    """This is a wrapper for a vim.VirtualMachine object."""

    re_vm_path_storage = re.compile(r'^\s*\[\s*([^\s\]]+)')
    re_vm_path_rel = re.compile(r'^\s*\[[^\]]*]\s*(\S.*)\s*$')

    # -------------------------------------------------------------------------
    def __init__(
        self, appname=None, verbose=0, version=__version__, base_dir=None, initialized=None,
            vsphere=None, name=None, status=DEFAULT_OBJ_STATUS, config_status=DEFAULT_OBJ_STATUS):
        """Initialize a VsphereVm object."""
        self.repr_fields = ('name', 'vsphere')
        self._vsphere = None
        self._cluster_name = None
        self._path = None
        self._template = False
        self._memory_mb = None
        self._num_cpu = None
        self._num_ethernet = None
        self._num_vdisk = None
        self._guest_fullname = None
        self._guest_id = None
        self._uuid = None
        self._instance_uuid = None
        self._host = None
        self._config_path = None
        self._config_version = None
        self.power_state = None
        self.disks = []
        self.interfaces = []
        self.controllers = []
        self.custom_data = []

        self.vm_tools = None

        super(VsphereVm, self).__init__(
            name=name, obj_type='vsphere_vm', name_prefix='vm', status=status,
            config_status=config_status, appname=appname, verbose=verbose,
            version=version, base_dir=base_dir)

        if vsphere is not None:
            self.vsphere = vsphere

        self.disks = VsphereDiskList(
            appname=appname, verbose=verbose, base_dir=base_dir, initialized=True)
        self.interfaces = VsphereEthernetcardList(
            appname=appname, verbose=verbose, base_dir=base_dir, initialized=True)
        self.controllers = VsphereDiskControllerList(
            appname=appname, verbose=verbose, base_dir=base_dir, initialized=True)

    # -----------------------------------------------------------
    @property
    def vsphere(self):
        """Return the name of the VSPhere from config, in which the VM should be existing."""
        return self._vsphere

    @vsphere.setter
    def vsphere(self, value):
        if value is None:
            self._vsphere = None
            return

        val = str(value).strip()
        if val == '':
            msg = _('The name of the vsphere may not be empty.')
            raise VSphereHandlerError(msg)

        self._vsphere = val

    # -----------------------------------------------------------
    @property
    def cluster_name(self):
        """Return the name of the compute resource, where this host is a member."""
        return self._cluster_name

    @cluster_name.setter
    def cluster_name(self, value):
        if value is None:
            self._cluster_name = None
            return
        v = str(value).strip().lower()
        if v == '':
            self._cluster_name = None
        else:
            self._cluster_name = v

    # -----------------------------------------------------------
    @property
    def host(self):
        """Return the host name, where the VM is configured."""
        return self._host

    @host.setter
    def host(self, value):
        if value is None:
            self._host = None
            return
        v = str(value).strip()
        if v == '':
            self._host = None
        else:
            self._host = v

    # -----------------------------------------------------------
    @property
    def path(self):
        """Return the path of the VM in the VM folder structure."""
        return self._path

    @path.setter
    def path(self, value):
        if value is None:
            self._path = None
            return
        v = str(value).strip()
        if v == '':
            self._path = None
        else:
            self._path = v

    # -----------------------------------------------------------
    @property
    def template(self):
        """Is this a VMWare template instead of a VM."""
        return self._template

    @template.setter
    def template(self, value):
        self._template = to_bool(value)

    # -----------------------------------------------------------
    @property
    def memory_mb(self):
        """Return the memory (RAM) of the VM in MiB."""
        return self._memory_mb

    @memory_mb.setter
    def memory_mb(self, value):
        if value is None:
            self._memory_mb = None
            return
        self._memory_mb = int(value)

    # -----------------------------------------------------------
    @property
    def memory_gb(self):
        """Return the memory (RAM) of the VM in GiB."""
        if self.memory_mb is None:
            return None
        return float(self.memory_mb) / 1024.0

    # -----------------------------------------------------------
    @property
    def num_cpu(self):
        """Return the number of CPUs of the VM."""
        return self._num_cpu

    @num_cpu.setter
    def num_cpu(self, value):
        if value is None:
            self._num_cpu = None
            return
        self._num_cpu = int(value)

    # -----------------------------------------------------------
    @property
    def num_ethernet(self):
        """Return the number of virtual ethernet network cards of the VM."""
        return self._num_ethernet

    @num_ethernet.setter
    def num_ethernet(self, value):
        if value is None:
            self._num_ethernet = None
            return
        self._num_ethernet = int(value)

    # -----------------------------------------------------------
    @property
    def num_vdisk(self):
        """Return the number of virtual disks of the VM."""
        return self._num_vdisk

    @num_vdisk.setter
    def num_vdisk(self, value):
        if value is None:
            self._num_vdisk = None
            return
        self._num_vdisk = int(value)

    # -----------------------------------------------------------
    @property
    def guest_fullname(self):
        """Return the guest Operating system name."""
        return self._guest_fullname

    @guest_fullname.setter
    def guest_fullname(self, value):
        if value is None:
            self._guest_fullname = None
            return
        v = str(value).strip()
        if v == '':
            self._guest_fullname = None
        else:
            self._guest_fullname = v

    # -----------------------------------------------------------
    @property
    def guest_id(self):
        """Return the guest Operating system identifier (shortname)."""
        return self._guest_id

    @guest_id.setter
    def guest_id(self, value):
        if value is None:
            self._guest_id = None
            return
        v = str(value).strip()
        if v == '':
            self._guest_id = None
        else:
            self._guest_id = v

    # -----------------------------------------------------------
    @property
    def uuid(self):
        """Return the Virtual machine BIOS identification."""
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        if value is None:
            self._uuid = None
            return
        v = str(value).strip()
        if v == '':
            self._uuid = None
        else:
            self._uuid = uuid.UUID(v)

    # -----------------------------------------------------------
    @property
    def instance_uuid(self):
        """Return the VC-specific identifier of the virtual machine."""
        return self._instance_uuid

    @instance_uuid.setter
    def instance_uuid(self, value):
        if value is None:
            self._instance_uuid = None
            return
        v = str(value).strip()
        if v == '':
            self._instance_uuid = None
        else:
            self._instance_uuid = uuid.UUID(v)

    # -----------------------------------------------------------
    @property
    def online(self):
        """Is this VM generally online or not."""
        if self.template:
            return False
        if self.power_state is None:
            return False
        if self.power_state.lower() in ('poweredoff', 'suspended'):
            return False
        return True

    # -----------------------------------------------------------
    @property
    def config_path(self):
        """Path name to the configuration file for the virtual machine (on storage)."""
        return self._config_path

    @config_path.setter
    def config_path(self, value):
        if value is None:
            self._config_path = None
            return
        v = str(value).strip()
        if v == '':
            self._config_path = None
        else:
            self._config_path = v

    # -----------------------------------------------------------
    @property
    def config_path_storage(self):
        """Return the name of the storage of the path of the configuration file."""
        if self.config_path is None:
            return None
        match = self.re_vm_path_storage.match(self.config_path)
        if match:
            return match.group(1)
        return None

    # -----------------------------------------------------------
    @property
    def config_path_relative(self):
        """Return the relative path of the configuration file on storage."""
        if self.config_path is None:
            return None
        match = self.re_vm_path_rel.match(self.config_path)
        if match:
            return match.group(1)
        return None

    # -----------------------------------------------------------
    @property
    def config_version(self):
        """Return the version string for this virtual machine."""
        return self._config_version

    @config_version.setter
    def config_version(self, value):
        if value is None:
            self._config_version = None
            return
        v = str(value).strip()
        if v == '':
            self._config_version = None
        else:
            self._config_version = v

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
                'vsphere': self.vsphere,
                'cluster_name': self.cluster_name,
                'config_path': self.config_path,
                'config_path_relative': self.config_path_relative,
                'config_path_storage': self.config_path_storage,
                'config_version': self.config_version,
                'host': self.host,
                'path': self.path,
                'template': self.template,
                'online': self.online,
                'memory_mb': self.memory_mb,
                'memory_gb': self.memory_gb,
                'num_cpu': self.num_cpu,
                'num_ethernet': self.num_ethernet,
                'num_vdisk': self.num_vdisk,
                'guest_fullname': self.guest_fullname,
                'guest_id': self.guest_id,
                'uuid': self.uuid,
                'instance_uuid': self.instance_uuid,
                'power_state': self.power_state,
                'disks': self.disks.as_dict(bare=True),
                'interfaces': self.interfaces.as_dict(bare=True),
                'controllers': self.controllers.as_dict(bare=True),
            }
            return res

        res = super(VsphereVm, self).as_dict(short=short)
        res['vsphere'] = self.vsphere
        res['cluster_name'] = self.cluster_name
        res['config_path'] = self.config_path
        res['config_path_relative'] = self.config_path_relative
        res['config_path_storage'] = self.config_path_storage
        res['config_version'] = self.config_version
        res['host'] = self.cluster_name
        res['path'] = self.path
        res['template'] = self.template
        res['online'] = self.online
        res['memory_mb'] = self.memory_mb
        res['memory_gb'] = self.memory_gb
        res['num_cpu'] = self.num_cpu
        res['num_ethernet'] = self.num_ethernet
        res['num_vdisk'] = self.num_vdisk
        res['guest_fullname'] = self.guest_fullname
        res['guest_id'] = self.guest_id
        res['uuid'] = self.uuid
        res['instance_uuid'] = self.instance_uuid

        return res

    # -------------------------------------------------------------------------
    def __copy__(self):
        """Return a new VsphereVm as a deep copy of the current object."""
        vm = VsphereVm(
            appname=self.appname, verbose=self.verbose, base_dir=self.base_dir,
            initialized=self.initialized, name=self.name, status=self.status,
            vsphere=self.vsphere, config_status=self.config_status)

        vm.cluster_name = self.cluster_name
        vm.config_path = self.config_path
        vm.config_version = self.config_version
        vm.host = self.host
        vm.path = self.path
        vm.template = self.template
        vm.memory_mb = self.memory_mb
        vm.num_cpu = self.num_cpu
        vm.num_ethernet = self.num_ethernet
        vm.num_vdisk = self.num_vdisk
        vm.guest_fullname = self.guest_fullname
        vm.guest_id = self.guest_id
        vm.uuid = self.uuid
        vm.instance_uuid = self.instance_uuid
        vm.power_state = self.power_state
        vm.disks = copy.copy(self.disks)
        vm.interfaces = copy.copy(self.interfaces)
        vm.controllers = copy.copy(self.controllers)

        return vm

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        """Magic method for using it as the '=='-operator."""
        if self.verbose > 4:
            LOG.debug(_('Comparing {} objects ...').format(self.__class__.__name__))

        if not isinstance(other, VsphereVm):
            return False

        if self.vsphere != other.vsphere:
            return False
        if self.name != other.name:
            return False
        if self.path != other.path:
            return False

        return True

    # -------------------------------------------------------------------------
    @classmethod
    def from_summary(
            cls, data, cur_path, vsphere=None, appname=None, verbose=0,
            base_dir=None, test_mode=False):
        """Create a new VsphereVm object based on the data given from pyvmomi."""
        if test_mode:
            cls._check_summary_data(data)
        else:
            if not isinstance(data, vim.VirtualMachine):
                msg = _('Parameter {t!r} must be a {e}, {v!r} ({vt}) was given.').format(
                    t='data', e='vim.VirtualMachine', v=data, vt=data.__class__.__name__)
                raise TypeError(msg)

        params = {
            'vsphere': vsphere,
            'appname': appname,
            'verbose': verbose,
            'base_dir': base_dir,
            'initialized': True,
            'name': data.summary.config.name,
            'status': DEFAULT_OBJ_STATUS,
            'config_status': OBJ_STATUS_GREEN,
        }

        if verbose > 2:
            LOG.debug(_('Creating {} object from:').format(cls.__name__) + '\n' + pp(params))

        vm = cls(**params)

        vm.cluster_name = None
        if data.resourcePool:
            vm.cluster_name = data.resourcePool.owner.name

        vm.host = None
        if data.runtime.host:
            vm.host = data.runtime.host

        vm.path = cur_path
        vm.template = data.summary.config.template
        vm.memory_mb = data.summary.config.memorySizeMB
        vm.num_cpu = data.summary.config.numCpu
        vm.num_ethernet = data.summary.config.numEthernetCards
        vm.num_vdisk = data.summary.config.numVirtualDisks
        vm.guest_fullname = data.summary.config.guestFullName
        vm.guest_id = data.summary.config.guestId
        vm.uuid = data.summary.config.uuid
        vm.instance_uuid = data.summary.config.instanceUuid
        vm.power_state = data.runtime.powerState
        vm.config_path = data.summary.config.vmPathName
        vm.config_version = data.config.version

        if hasattr(data.summary, 'customValue'):
            for custom_data in data.summary.customValue:
                custom_key = custom_data.key
                custom_value = ''

                if hasattr(custom_data, 'value'):
                    custom_value = custom_data.value

                vm.custom_data.append({custom_key: custom_value, })

        if data.guest:

            vm.vm_tools = {}

            vm.vm_tools['install_type'] = None
            vm.vm_tools['state'] = None
            vm.vm_tools['version'] = data.guest.toolsVersion
            vm.vm_tools['version_state'] = None

            if hasattr(data.guest, 'toolsInstallType'):
                vm.vm_tools['install_type'] = data.guest.toolsInstallType

            if hasattr(data.guest, 'toolsRunningStatus'):
                vm.vm_tools['state'] = data.guest.toolsRunningStatus
            else:
                vm.vm_tools['state'] = data.guest.toolsStatus

            if hasattr(data.guest, 'toolsVersionStatus2'):
                vm.vm_tools['version_state'] = data.guest.toolsVersionStatus2
            else:
                vm.vm_tools['version_state'] = data.guest.toolsVersionStatus

        if data.config and data.config.hardware:
            for device in data.config.hardware.device:
                if isinstance(device, vim.vm.device.VirtualDisk):
                    disk = VsphereDisk.from_summary(
                        device, appname=appname, verbose=verbose, base_dir=base_dir)
                    vm.disks.append(disk)
                elif isinstance(device, vim.vm.device.VirtualEthernetCard):
                    iface = VsphereEthernetcard.from_summary(
                        device, appname=appname, verbose=verbose, base_dir=base_dir)
                    vm.interfaces.append(iface)
                elif isinstance(device, vim.vm.device.VirtualController):
                    ctrl = VsphereDiskController.from_summary(
                        device, appname=appname, verbose=verbose, base_dir=base_dir)
                    vm.controllers.append(ctrl)
                elif verbose > 2:
                    LOG.debug(_('Unknown hardware device of type {}.').format(
                        device.__class__.__name__))
        else:
            LOG.error(_(
                'There is something wrong wit VM {n!r} in cluster {c!r} and '
                'path {p!r} ...').format(n=vm.name, c=vm.cluster_name, p=vm.path))

        if verbose > 2:
            LOG.debug(_('Created {} object:').format(cls.__name__) + '\n' + pp(vm.as_dict()))

        return vm

    # -------------------------------------------------------------------------
    @classmethod
    def _check_summary_data(cls, data):

        necessary_fields = ('summary', 'resourcePool', 'runtime', 'config', 'guest')
        summary_cfg_fields = (
            'template', 'memorySizeMB', 'numCpu', 'numEthernetCards', 'numVirtualDisks',
            'guestFullName', 'guestId', 'uuid', 'instanceUuid', 'powerState',
            'vmPathName')

        failing_fields = []

        for field in necessary_fields:
            if not hasattr(data, field):
                failing_fields.append(field)

        if hasattr(data, 'resourcePool') and data.resourcePool:
            if hasattr(data.resourcePool, 'owner'):
                if not hasattr(data.resourcePool.owner, 'name'):
                    failing_fields.append('resourcePool.owner.name')
            else:
                failing_fields.append('resourcePool.owner')

        if hasattr(data, 'runtime'):
            if not hasattr(data.runtime, 'host'):
                failing_fields.append('runtime.host')

        if hasattr(data, 'summary'):
            if hasattr(data.summary, 'config'):
                for field in summary_cfg_fields:
                    if not hasattr(data.summary.config, field):
                        failing_fields.append('summary.config.' + field)
            else:
                failing_fields.append('summary.config')

        if hasattr(data, 'config') and data.config:
            if not hasattr(data.config, 'version'):
                failing_fields.append('config.version')
            if hasattr(data.config, 'hardware'):
                if data.config.hardware:
                    if not hasattr(data.config.hardware, 'device'):
                        failing_fields.append('config.hardware.device')
            else:
                failing_fields.append('config.hardware')

        if len(failing_fields):
            msg = _(
                'The given parameter {p!r} on calling method {m}() has failing '
                'attributes').format(p='data', m='from_summary')
            msg += ': ' + format_list(failing_fields, do_repr=True)
            raise AssertionError(msg)


# =============================================================================
class VsphereVmList(FbBaseObject, MutableSequence):
    """A list containing VsphereVm objects."""

    msg_no_vm = _('Invalid type {t!r} as an item of a {c}, only {o} objects are allowed.')

    # -------------------------------------------------------------------------
    def __init__(
        self, appname=None, verbose=0, version=__version__, base_dir=None,
            initialized=None, *vms):
        """Initialize a VsphereVmList object."""
        self._list = []

        super(VsphereVmList, self).__init__(
            appname=appname, verbose=verbose, version=version, base_dir=base_dir,
            initialized=False)

        for vm in vms:
            self.append(vm)

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
            for vm in self:
                res.append(vm.as_dict(bare=True))
            return res

        res = super(VsphereVmList, self).as_dict(short=short)
        res['_list'] = []

        for vm in self:
            res['_list'].append(vm.as_dict(short=short))

        return res

    # -------------------------------------------------------------------------
    def __copy__(self):
        """Return a new VsphereVmList as a deep copy of the current object."""
        new_list = self.__class__(
            appname=self.appname, verbose=self.verbose,
            base_dir=self.base_dir, initialized=False)

        for vm in self:
            new_list.append(copy.copy(vm))

        new_list.initialized = self.initialized
        return new_list

    # -------------------------------------------------------------------------
    def index(self, vm, *args):
        """Return the numeric index of the given VM in current list."""
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
            if item == vm:
                return index

        if wrap:
            for index in list(range(len(self._list))):
                item = self._list[index]
                if index >= end:
                    break
            if item == vm:
                return index

        msg = _('VM is not in VM list.')
        raise ValueError(msg)

    # -------------------------------------------------------------------------
    def __contains__(self, vm):
        """Return whether the given VM is contained in current list."""
        if not isinstance(vm, VsphereVm):
            raise TypeError(self.msg_no_vm.format(
                t=vm.__class__.__name__, c=self.__class__.__name__, o='VsphereVm'))

        if not self._list:
            return False

        for item in self._list:
            if item == vm:
                return True

        return False

    # -------------------------------------------------------------------------
    def count(self, vm):
        """Return the number of VMs which are equal to the given one in current list."""
        if not isinstance(vm, VsphereVm):
            raise TypeError(self.msg_no_vm.format(
                t=vm.__class__.__name__, c=self.__class__.__name__, o='VsphereVm'))

        if not self._list:
            return 0

        num = 0
        for item in self._list:
            if item == vm:
                num += 1
        return num

    # -------------------------------------------------------------------------
    def __len__(self):
        """Return the number of VMs in current list."""
        return len(self._list)

    # -------------------------------------------------------------------------
    def __iter__(self):
        """Iterate through all VMs in current list."""
        for item in self._list:
            yield item

    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """Get a VM from current list by the given numeric index."""
        return self._list.__getitem__(key)

    # -------------------------------------------------------------------------
    def __reversed__(self):
        """Reverse the VMs in list in place."""
        new_list = self.__class__(
            appname=self.appname, verbose=self.verbose,
            base_dir=self.base_dir, initialized=False)

        for vm in reversed(self._list):
            new_list.append(copy.copy(vm))

        new_list.initialized = self.initialized
        return new_list

    # -------------------------------------------------------------------------
    def __setitem__(self, key, vm):
        """Replace the VM at the given numeric index by the given one."""
        if not isinstance(vm, VsphereVm):
            raise TypeError(self.msg_no_vm.format(
                t=vm.__class__.__name__, c=self.__class__.__name__, o='VsphereVm'))

        self._list.__setitem__(key, vm)

    # -------------------------------------------------------------------------
    def __delitem__(self, key):
        """Remove the VM at the given numeric index from list."""
        del self._list[key]

    # -------------------------------------------------------------------------
    def append(self, vm):
        """Append the given VM to the current list."""
        if not isinstance(vm, VsphereVm):
            raise TypeError(self.msg_no_vm.format(
                t=vm.__class__.__name__, c=self.__class__.__name__, o='VsphereVm'))

        self._list.append(vm)

    # -------------------------------------------------------------------------
    def insert(self, index, vm):
        """Insert the given VM in current list at given index."""
        if not isinstance(vm, VsphereVm):
            raise TypeError(self.msg_no_vm.format(
                t=vm.__class__.__name__, c=self.__class__.__name__, o='VsphereVm'))

        self._list.insert(index, vm)

    # -------------------------------------------------------------------------
    def clear(self):
        """Remove all items from the VsphereEthernetcardList."""
        self._list = []


# =============================================================================
if __name__ == '__main__':

    pass

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 list
