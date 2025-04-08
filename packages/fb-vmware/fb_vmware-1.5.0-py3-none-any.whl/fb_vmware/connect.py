#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: The module for a VSphere connection object.

@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2025 by Frank Brehm, Berlin
"""
from __future__ import absolute_import

# Standard modules
import datetime
import logging
import re
import socket
import time
import uuid
try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence
from numbers import Number

# Third party modules
from fb_tools.common import RE_TF_NAME, pp
from fb_tools.common import is_sequence
from fb_tools.errors import HandlerError

from pyVmomi import vim, vmodl

import requests

import urllib3

# Own modules
from .about import VsphereAboutInfo
from .base import BaseVsphereHandler, DEFAULT_TZ_NAME
from .cluster import VsphereCluster
from .config import DEFAULT_VSPHERE_CLUSTER
from .controller import VsphereDiskController
from .datastore import VsphereDatastore, VsphereDatastoreDict
from .dc import VsphereDatacenter
from .ds_cluster import VsphereDsCluster, VsphereDsClusterDict
from .dvs import VsphereDVS, VsphereDvPortGroup
from .errors import TimeoutCreateVmError
from .errors import VSphereDatacenterNotFoundError
from .errors import VSphereExpectedError
from .errors import VSphereNoDatastoresFoundError
from .errors import VSphereVmNotFoundError
from .host import VsphereHost
from .iface import VsphereVmInterface
from .network import VsphereNetwork, VsphereNetworkDict
from .vm import VsphereVm, VsphereVmList
from .xlate import XLATOR

__version__ = '2.2.2'
LOG = logging.getLogger(__name__)

DEFAULT_OS_VERSION = 'rhel9_64Guest'
DEFAULT_VM_CFG_VERSION = 'vmx-19'

_ = XLATOR.gettext
ngettext = XLATOR.ngettext


# =============================================================================
class VsphereConnection(BaseVsphereHandler):
    """Class for a VSphere connection handler object."""

    re_local_ds = re.compile(r'^local[_-]', re.IGNORECASE)
    vmw_api_version_to_hw_version = {
        '5.0': 8,
        '5.1': 9,
        '5.5': 10,
        '6.0': 11,
        '6.5': 13,
        '6.7': 14,
        '6.7 u2': 15,
        '7.0.0-0': 17,
        '7.0 u1': 18,
        '7.0 u2': 19,
    }

    # -------------------------------------------------------------------------
    def __init__(
        self, connect_info, appname=None, verbose=0, version=__version__, base_dir=None,
            cluster=DEFAULT_VSPHERE_CLUSTER, auto_close=True, simulate=None,
            force=None, terminal_has_colors=False, tz=DEFAULT_TZ_NAME, initialized=False):
        """Initialize a VsphereConnection object."""
        self.datastores = VsphereDatastoreDict()
        self.ds_clusters = VsphereDsClusterDict()
        self.networks = VsphereNetworkDict()
        self.dv_portgroups = VsphereNetworkDict()
        self.about = None
        self.dc_obj = None
        self.dvs = {}

        self.ds_mapping = {}
        self.ds_cluster_mapping = {}
        self.network_mapping = {}

        self.clusters = []
        self.hosts = {}
        self.custom_fields = None

        super(VsphereConnection, self).__init__(
            connect_info=connect_info, appname=appname, verbose=verbose, version=version,
            base_dir=base_dir, cluster=cluster, simulate=simulate, force=force,
            auto_close=auto_close, terminal_has_colors=terminal_has_colors, tz=tz,
            initialized=False,
        )

        self.initialized = initialized

    # -------------------------------------------------------------------------
    def __repr__(self):
        """Typecasting into a string for reproduction."""
        return self._repr()

    # -------------------------------------------------------------------------
    def get_about(self, disconnect=False):
        """Get the 'about' information from VSphere as a VsphereAboutInfo object."""
        LOG.debug(_("Trying to get some 'about' information from VSphere."))

        try:

            if not self.service_instance:
                self.connect()

            self.about = VsphereAboutInfo.from_summary(
                self.service_instance.content.about,
                appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)

        except (
                socket.timeout, urllib3.exceptions.ConnectTimeoutError,
                urllib3.exceptions.MaxRetryError,
                requests.exceptions.ConnectTimeout) as e:
            msg = _(
                "Got a {c} on requesting 'about' information from VSPhere {url}: {e}").format(
                c=e.__class__.__name__, url=self.connect_info.url, e=e)
            raise VSphereExpectedError(msg)

        finally:
            if disconnect:
                self.disconnect()

        if self.verbose:
            LOG.info(_('VSphere version: {!r}').format(self.about.os_version))
        if self.verbose > 1:
            LOG.debug(_('Found VSphere about-information:') + '\n' + pp(self.about.as_dict()))

    # -------------------------------------------------------------------------
    def get_datacenter(self, disconnect=False):
        """Get the datacenter from VSphere as a VsphereDatacenter object."""
        LOG.debug(_('Trying to get datacenter from VSphere ...'))

        try:

            if not self.service_instance:
                self.connect()

            content = self.service_instance.RetrieveContent()
            dc_obj = self.get_obj(content, [vim.Datacenter], self.dc)
            if not dc_obj:
                raise VSphereDatacenterNotFoundError(self.dc)

            self.dc_obj = VsphereDatacenter.from_summary(
                dc_obj, appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)
            LOG.debug(_('Found VSphere datacenter {!r}.').format(self.dc_obj.name))
            if self.verbose > 2:
                LOG.debug(_('Info about datacenter:') + '\n' + str(self.dc_obj))

        finally:
            if disconnect:
                self.disconnect()

        return

    # -------------------------------------------------------------------------
    def get_clusters(self, disconnect=False):
        """Get all clusters from VSphere as VsphereCluster objects."""
        LOG.debug(_('Trying to get all clusters from VSphere ...'))

        self.clusters = []

        try:

            if not self.service_instance:
                self.connect()

            content = self.service_instance.RetrieveContent()
            dc = self.get_obj(content, [vim.Datacenter], self.dc)
            if not dc:
                raise VSphereDatacenterNotFoundError(self.dc)
            for child in dc.hostFolder.childEntity:
                self._get_clusters(child)

        finally:
            if disconnect:
                self.disconnect()

        if self.verbose > 2:
            out = []
            for cluster in self.clusters:
                out.append(cluster.as_dict())
            LOG.debug(_('Found clusters:') + '\n' + pp(out))
        elif self.verbose:
            out = []
            for cluster in self.clusters:
                out.append(cluster.name)
            LOG.debug(_('Found clusters:') + '\n' + pp(out))

    # -------------------------------------------------------------------------
    def _get_clusters(self, child, depth=1):

        if hasattr(child, 'childEntity'):
            if depth > self.max_search_depth:
                return
            for sub_child in child.childEntity:
                self._get_clusters(sub_child, depth + 1)
            return

        if isinstance(child, (vim.ClusterComputeResource, vim.ComputeResource)):
            cluster = VsphereCluster.from_summary(
                child, appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)
            if self.verbose > 1:
                obj_name = _('Found standalone host')
                if isinstance(child, vim.ClusterComputeResource):
                    obj_name = _('Found cluster')
                host_label = ngettext('host', 'hosts', cluster.hosts_total)
                cpus_label = ngettext('CPU', 'CPUs', cluster.cpu_cores)
                thr_label = ngettext('thread', 'threads', cluster.cpu_threads)
                nw_label = ngettext('network', 'networks', len(cluster.networks))
                ds_label = ngettext('datastore', 'datastores', len(cluster.datastores))
                LOG.debug(_(
                    '{on} {cl!r}, {h} {h_l}, {cpu} {cpu_l}, {thr} {t_l}, '
                    '{mem:0.1f} GiB Memory, {net} {nw_l} and {ds} {ds_l}.').format(
                    on=obj_name, cl=cluster.name, h=cluster.hosts_total, h_l=host_label,
                    cpu=cluster.cpu_cores, cpu_l=cpus_label, thr=cluster.cpu_threads,
                    t_l=thr_label, mem=cluster.mem_gb_total, net=len(cluster.networks),
                    nw_l=nw_label, ds=len(cluster.datastores), ds_l=ds_label))
            self.clusters.append(cluster)

        return

    # -------------------------------------------------------------------------
    def get_cluster_by_name(self, cl_name):
        """Return a VsphereCluster from cluster list by the given cluster name."""
        for cluster in self.clusters:
            if cluster.name.lower() == cl_name.lower():
                return cluster

        return None

    # -------------------------------------------------------------------------
    def get_datastores(self, disconnect=False):
        """Get all datastores from VSphere as VsphereDatastore objects."""
        LOG.debug(_('Trying to get all datastores from VSphere ...'))
        self.datastores = VsphereDatastoreDict()
        self.ds_mapping = {}

        try:

            if not self.service_instance:
                self.connect()

            content = self.service_instance.RetrieveContent()
            dc = self.get_obj(content, [vim.Datacenter], self.dc)
            if not dc:
                raise VSphereDatacenterNotFoundError(self.dc)
            for child in dc.datastoreFolder.childEntity:
                self._get_datastores(child)

        finally:
            if disconnect:
                self.disconnect()

        if self.datastores:
            if self.verbose > 1:
                if self.verbose > 2:
                    LOG.debug(_('Found datastores:') + '\n' + pp(self.datastores.as_list()))
                else:
                    LOG.debug(_('Found datastores:') + '\n' + pp(list(self.datastores.keys())))
        else:
            raise VSphereNoDatastoresFoundError()

        for (ds_name, ds) in self.datastores.items():
            self.ds_mapping[ds_name] = ds.tf_name

        if self.verbose > 2:
            LOG.debug(_('Datastore mappings:') + '\n' + pp(self.ds_mapping))

    # -------------------------------------------------------------------------
    def _get_datastores(self, child, depth=1):

        if hasattr(child, 'childEntity'):
            if depth > self.max_search_depth:
                return
            for sub_child in child.childEntity:
                self._get_datastores(sub_child, depth + 1)
            return

        if isinstance(child, vim.Datastore):
            if self.re_local_ds.match(child.summary.name):
                if self.verbose > 2:
                    LOG.debug(_('Datastore {!r} seems to be local.').format(child.summary.name))
                return
            ds = VsphereDatastore.from_summary(
                child, appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)
            if self.verbose > 2:
                LOG.debug(
                    _('Found datastore {ds!r} of type {t!r}, capacity {c:0.1f} GByte.').format(
                        ds=ds.name, t=ds.storage_type, c=ds.capacity_gb))
            self.datastores.append(ds)

        return

    # -------------------------------------------------------------------------
    def get_ds_clusters(self, disconnect=False):
        """Get all datastores clusters from VSphere as VsphereDsCluster objects."""
        LOG.debug(_('Trying to get all datastore clusters from VSphere ...'))
        self.ds_clusters = VsphereDsClusterDict()
        self.ds_cluster_mapping = {}

        try:

            if not self.service_instance:
                self.connect()

            content = self.service_instance.RetrieveContent()
            dc = self.get_obj(content, [vim.Datacenter], self.dc)
            if not dc:
                raise VSphereDatacenterNotFoundError(self.dc)
            for child in dc.datastoreFolder.childEntity:
                self._get_ds_clusters(child)

        finally:
            if disconnect:
                self.disconnect()

        if self.ds_clusters:
            if self.verbose > 1:
                if self.verbose > 3:
                    LOG.debug(
                        _('Found datastore clusters:') + '\n' + pp(self.ds_clusters.as_list()))
                else:
                    LOG.debug(
                        _('Found datastore clusters:') + '\n' + pp(list(self.ds_clusters.keys())))
        else:
            LOG.warning(_('No VSphere datastore clusters found.'))

        for (dsc_name, dsc) in self.ds_clusters.items():
            self.ds_cluster_mapping[dsc_name] = dsc.tf_name

        if self.verbose > 2:
            LOG.debug(_('Datastore cluster mappings:') + '\n' + pp(self.ds_cluster_mapping))

    # -------------------------------------------------------------------------
    def _get_ds_clusters(self, child, depth=1):

        if self.verbose > 3:
            LOG.debug(_('Found a {} child.').format(child.__class__.__name__))

        if hasattr(child, 'childEntity'):
            if depth > self.max_search_depth:
                return
            for sub_child in child.childEntity:
                self._get_ds_clusters(sub_child, depth + 1)

        if isinstance(child, vim.StoragePod):
            ds = VsphereDsCluster.from_summary(
                child, appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)
            self.ds_clusters.append(ds)

        return

    # -------------------------------------------------------------------------
    def get_networks(self, disconnect=False):
        """Get all networks from VSphere as VsphereNetwork objects."""
        LOG.debug(_('Trying to get all networks from VSphere ...'))
        self.dv_portgroups = VsphereNetworkDict()
        self.networks = VsphereNetworkDict()
        self.network_mapping = {}

        try:

            if not self.service_instance:
                self.connect()

            content = self.service_instance.RetrieveContent()
            dc = self.get_obj(content, [vim.Datacenter], self.dc)
            if not dc:
                raise VSphereDatacenterNotFoundError(self.dc)
            for child in dc.networkFolder.childEntity:
                self._get_networks(child)

        finally:
            if disconnect:
                self.disconnect()

        if self.dv_portgroups:
            msg = ngettext(
                'Found one Distributed Virtual Port Group.',
                'Found {n} Distributed Virtual Port Groups.',
                len(self.dv_portgroups))
            LOG.debug(msg.format(n=len(self.dv_portgroups)))
            if self.verbose > 2:
                msg = _('Found Distributed Virtual Port Groups:') + '\n'
                if self.verbose > 3:
                    msg += pp(self.dv_portgroups.as_list())
                else:
                    msg += pp(list(self.dv_portgroups.keys()))
                LOG.debug(msg)
        else:
            if self.verbose:
                LOG.info(_('No Distributed Virtual Port Groups found.'))

        if self.networks:
            msg = ngettext(
                'Found one Virtual Network.',
                'Found {n} Virtual Networks.',
                len(self.networks))
            LOG.debug(msg.format(n=len(self.networks)))
            if self.verbose > 2:
                if self.verbose > 3:
                    LOG.debug(_('Found Virtual Networks:') + '\n' + pp(self.networks.as_list()))
                else:
                    LOG.debug(_('Found Virtual Networks:') + '\n' + pp(list(self.networks.keys())))
        else:
            LOG.info(_('No Virtual Networks found.'))

        for (net_name, dvpg) in self.dv_portgroups.items():
            self.network_mapping[net_name] = dvpg.tf_name
        for (net_name, net) in self.networks.items():
            if net_name not in self.network_mapping:
                self.network_mapping[net_name] = net.tf_name

        if self.verbose > 2:
            LOG.debug(_('Network mappings:') + '\n' + pp(self.network_mapping))

    # -------------------------------------------------------------------------
    def _get_networks(self, child, depth=1):

        if self.verbose > 3:
            LOG.debug(_('Found a {} child.').format(child.__class__.__name__))

        if hasattr(child, 'childEntity'):
            if depth > self.max_search_depth:
                return
            for sub_child in child.childEntity:
                self._get_networks(sub_child, depth + 1)

        if isinstance(child, vim.DistributedVirtualSwitch):
            dvs = VsphereDVS.from_summary(
                child, appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)
            uuid = dvs.uuid
            self.dvs[uuid] = dvs
        elif isinstance(child, vim.Network):
            if isinstance(child, vim.dvs.DistributedVirtualPortgroup):
                portgroup = VsphereDvPortGroup.from_summary(
                    child, appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)
                self.dv_portgroups.append(portgroup)
            elif isinstance(child, vim.OpaqueNetwork):
                LOG.debug('Evaluating Opaque Network later ...')
            else:
                network = VsphereNetwork.from_summary(
                    child, appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)
                self.networks.append(network)

        return

    # -------------------------------------------------------------------------
    def get_hosts(self, re_name=None, vsphere_name=None, disconnect=False):
        """Get all physical hosts from VSphere as VsphereHost objects."""
        if re_name is not None:
            if not hasattr(re_name, 'match'):
                msg = _('Parameter {p!r} => {r!r} seems not to be a regex object.').format(
                    p='re_name', r=re_name)
                raise TypeError(msg)
            LOG.debug(_(
                'Trying to get all host systems from VSphere with name pattern {!r} ...').format(
                re_name.pattern))
        else:
            LOG.debug(_('Trying to get all host systems from VSphere ...'))

        self.clusters = []
        self.hosts = {}

        try:

            if not self.service_instance:
                self.connect()

            content = self.service_instance.RetrieveContent()
            dc = self.get_obj(content, [vim.Datacenter], self.dc)
            if not dc:
                raise VSphereDatacenterNotFoundError(self.dc)

            for child in dc.hostFolder.childEntity:
                self._get_hosts(child, re_name=re_name, vsphere_name=vsphere_name)

        finally:
            if disconnect:
                self.disconnect()

        if self.verbose > 2:
            out = []
            for host_name in self.hosts.keys():
                host = self.hosts[host_name]
                out.append(host.as_dict())
            LOG.debug(_('Found hosts:') + '\n' + pp(out))
        elif self.verbose:
            out = []
            for host_name in self.hosts.keys():
                out.append(host_name)
            LOG.debug(_('Found hosts:') + '\n' + pp(out))

    # -------------------------------------------------------------------------
    def _get_hosts(self, child, depth=1, re_name=None, vsphere_name=None, cluster_name=None):

        if self.verbose > 3:
            LOG.debug(_('Checking {o}-object in cluster {c!r} ...').format(
                o=child.__class__.__name__, c=cluster_name))

        if isinstance(child, (vim.ClusterComputeResource, vim.ComputeResource)):
            cluster = VsphereCluster.from_summary(
                child, appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)
            cluster_name = cluster.name
            if self.verbose > 1:
                obj_name = _('Found standalone host')
                if isinstance(child, vim.ClusterComputeResource):
                    obj_name = _('Found cluster')
                host_label = ngettext('host', 'hosts', cluster.hosts_total)
                cpus_label = ngettext('CPU', 'CPUs', cluster.cpu_cores)
                thr_label = ngettext('thread', 'threads', cluster.cpu_threads)
                nw_label = ngettext('network', 'networks', len(cluster.networks))
                ds_label = ngettext('datastore', 'datastores', len(cluster.datastores))
                LOG.debug(_(
                    '{on} {cl!r}, {h} {h_l}, {cpu} {cpu_l}, {thr} {t_l}, '
                    '{mem:0.1f} GiB Memory, {net} {nw_l} and {ds} {ds_l}.').format(
                    on=obj_name, cl=cluster.name, h=cluster.hosts_total, h_l=host_label,
                    cpu=cluster.cpu_cores, cpu_l=cpus_label, thr=cluster.cpu_threads,
                    t_l=thr_label, mem=cluster.mem_gb_total, net=len(cluster.networks),
                    nw_l=nw_label, ds=len(cluster.datastores), ds_l=ds_label))

            self.clusters.append(cluster)

            for host_def in child.host:

                hostname = host_def.summary.config.name

                if re_name is not None:
                    if not re_name.search(hostname):
                        continue

                LOG.debug(_('Found host {h!r} in cluster {c!r}.').format(
                    h=hostname, c=cluster_name))
                host = VsphereHost.from_summary(
                    host_def, vsphere=vsphere_name, cluster_name=cluster_name,
                    appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)
                self.hosts[host.name] = host

        return

    # -------------------------------------------------------------------------
    def get_vm(
            self, vm_name, vsphere_name=None, no_error=False, disconnect=False, as_vmw_obj=False,
            as_obj=False, name_only=False):
        """Get a virtual machine from VSphere as VsphereVm object by its name."""
        pattern_name = r'^\s*' + re.escape(vm_name) + r'\s*$'
        LOG.debug(_('Searching for VM {n!r} (pattern: {p!r}) in VSPhere {v!r} ...').format(
            n=vm_name, p=pattern_name, v=vsphere_name))
        re_name = re.compile(pattern_name, re.IGNORECASE)
        vmlist = self.get_vms(
            re_name, vsphere_name=vsphere_name, disconnect=disconnect, as_vmw_obj=as_vmw_obj,
            as_obj=as_obj, name_only=name_only, stop_at_found=True)

        if not vmlist:
            msg = _('VSphere VM {!r} not found.').format(vm_name)
            if no_error:
                LOG.debug(msg)
            else:
                LOG.error(msg)
            return None

        return vmlist[0]

    # -------------------------------------------------------------------------
    def _dict_from_vim_obj(self, vm, cur_path):

        if not isinstance(vm, vim.VirtualMachine):
            msg = _('Parameter {t!r} must be a {e}, {v!r} was given.').format(
                t='vm', e='vim.VirtualMachine', v=vm)
            raise TypeError(msg)

        summary = vm.summary
        vm_config = summary.config

        vm_info = {}
        vm_info['name'] = vm_config.name
        vm_info['tf_name'] = 'vm_' + RE_TF_NAME.sub('_', vm_config.name.lower())
        vm_info['cluster'] = None
        if vm.resourcePool:
            vm_info['cluster'] = vm.resourcePool.owner.name
        vm_info['path'] = cur_path
        vm_info['memorySizeMB'] = vm_config.memorySizeMB
        vm_info['numCpu'] = vm_config.numCpu
        vm_info['numEthernetCards'] = vm_config.numEthernetCards
        vm_info['numVirtualDisks'] = vm_config.numVirtualDisks
        vm_info['template'] = vm_config.template
        vm_info['guestFullName'] = vm_config.guestFullName
        vm_info['guestId'] = vm_config.guestId
        vm_info['vm_tools'] = {}
        if vm.guest:
            vm_info['vm_tools']['install_type'] = None
            if hasattr(vm.guest, 'toolsInstallType'):
                vm_info['vm_tools']['install_type'] = vm.guest.toolsInstallType
            vm_info['vm_tools']['state'] = None
            if hasattr(vm.guest, 'toolsRunningStatus'):
                vm_info['vm_tools']['state'] = vm.guest.toolsRunningStatus
            else:
                vm_info['vm_tools']['state'] = vm.guest.toolsStatus
            vm_info['vm_tools']['version'] = vm.guest.toolsVersion
            vm_info['vm_tools']['version_state'] = None
            if hasattr(vm.guest, 'toolsVersionStatus2'):
                vm_info['vm_tools']['version_state'] = vm.guest.toolsVersionStatus2
            else:
                vm_info['vm_tools']['version_state'] = vm.guest.toolsVersionStatus
        vm_info['host'] = None
        if vm.runtime.host:
            vm_info['host'] = vm.runtime.host.name
        vm_info['instanceUuid'] = vm_config.instanceUuid
        vm_info['power_state'] = vm.runtime.powerState
        if vm_config.instanceUuid:
            vm_info['instanceUuid'] = uuid.UUID(vm_config.instanceUuid)
        vm_info['uuid'] = vm_config.uuid
        if vm_config.uuid:
            vm_info['uuid'] = uuid.UUID(vm_config.uuid)
        vm_info['vmPathName'] = vm_config.vmPathName
        vm_info['cfg_version'] = vm.config.version
        vm_info['disks'] = {}
        for device in vm.config.hardware.device:
            if not isinstance(device, vim.vm.device.VirtualDisk):
                continue
            unit_nr = device.unitNumber
            disk = {
                'label': device.deviceInfo.label,
                'unitNumber': unit_nr,
                'capacityInKB': device.capacityInKB,
                'capacityInBytes': device.capacityInBytes,
                'uuid': device.backing.uuid,
                'fileName': device.backing.fileName
            }
            disk['capacityInGB'] = device.capacityInKB / 1024 / 1024
            if device.backing.uuid:
                disk['uuid'] = uuid.UUID(device.backing.uuid)
            vm_info['disks'][unit_nr] = disk
        vm_info['interfaces'] = {}
        for device in vm.config.hardware.device:
            if not isinstance(device, vim.vm.device.VirtualEthernetCard):
                continue
            unit_nr = device.unitNumber
            iface = {
                'unitNumber': unit_nr,
                'class': device.__class__.__name__,
                'addressType': device.addressType,
                'macAddress': device.macAddress,
                'backing_device': device.backing.deviceName,
                'connected': device.connectable.connected,
                'status': device.connectable.status,
            }
            vm_info['interfaces'][unit_nr] = iface
        return vm_info

    # -------------------------------------------------------------------------
    def get_vms(
            self, re_name, vsphere_name=None, is_template=None, disconnect=False, as_vmw_obj=False,
            as_obj=False, name_only=False, stop_at_found=False):
        """Get all virtual machines from VSphere as VsphereVm objects."""
        if not hasattr(re_name, 'match'):
            msg = _('Parameter {p!r} => {r!r} seems not to be a regex object.').format(
                p='re_name', r=re_name)
            raise TypeError(msg)
        if as_vmw_obj and as_obj:
            msg = _('Parameter {p1!r} and {p2!r} may not be {w!r} at the same time.').format(
                p1='as_vmw_obj', p2='as_obj', w=True)
            raise ValueError(msg)

        LOG.debug(_('Trying to get list of VMs with name pattern {!r} ...').format(
            re_name.pattern))
        vm_list = []
        if as_obj:
            vm_list = VsphereVmList(
                appname=self.appname, verbose=self.verbose, base_dir=self.base_dir,
                initialized=True)

        try:
            if not self.service_instance:
                self.connect()

            content = self.service_instance.RetrieveContent()
            dc = self.get_obj(content, [vim.Datacenter], self.dc)
            if not dc:
                raise VSphereDatacenterNotFoundError(self.dc)

            for child in dc.vmFolder.childEntity:
                path = child.name
                if self.verbose > 1:
                    LOG.debug(_('Searching in path {!r} ...').format(path))
                vms = self._get_vms(
                    child, re_name, vsphere_name=vsphere_name, is_template=is_template,
                    as_vmw_obj=as_vmw_obj, as_obj=as_obj, name_only=name_only,
                    stop_at_found=stop_at_found)
                if vms:
                    vm_list += vms

        finally:
            if disconnect:
                self.disconnect()

        msg = ngettext(
            'Found one VM with pattern {p!r}.', 'Found {no} VMs with pattern {p!r}.', len(vm_list))
        LOG.debug(msg.format(no=len(vm_list), p=re_name.pattern))

        return vm_list

    # -------------------------------------------------------------------------
    def _get_vms(
            self, child, re_name, cur_path='', vsphere_name=None, is_template=None, depth=1,
            as_vmw_obj=False, as_obj=False, name_only=False, stop_at_found=False):

        vm_list = []
        if as_obj:
            vm_list = VsphereVmList(
                appname=self.appname, verbose=self.verbose, base_dir=self.base_dir,
                initialized=True)

        # if self.verbose > 3:
        #     LOG.debug(_("Searching in path {!r} ...").format(cur_path))
        #     LOG.debug(_("Found a {} child.").format(child.__class__.__name__))

        if hasattr(child, 'childEntity'):
            if depth > self.max_search_depth:
                return vm_list
            return self._get_vm_childs(
                child, re_name, cur_path=cur_path, vsphere_name=vsphere_name,
                is_template=is_template, depth=depth, as_vmw_obj=as_vmw_obj,
                as_obj=as_obj, name_only=name_only, stop_at_found=stop_at_found)

        if isinstance(child, vim.VirtualMachine):

            summary = child.summary
            vm_config = summary.config
            vm_name = vm_config.name

            if self.verbose > 3:
                LOG.debug(_('Checking VM {!r} ...').format(vm_name))
            if is_template is not None:
                if self.verbose > 3:
                    msg = _('Checking VM {!r} for being a template ...')
                    if not is_template:
                        msg = _('Checking VM {!r} for being not a template ...')
                    LOG.debug(msg.format(vm_name))
                if is_template and not vm_config.template:
                    return []
                if not is_template and vm_config.template:
                    return []

            if self.verbose > 3:
                LOG.debug(_('Checking VM {!r} for pattern.').format(vm_name))
            if re_name.search(vm_name):
                if self.verbose > 2:
                    LOG.debug(_('Found VM {!r}.').format(vm_name))
                if name_only:
                    vm_list.append((vm_name, cur_path))
                elif as_obj:
                    if self.verbose > 1:
                        LOG.debug(f'Get VM {vm_name!r} as an object.')
                    vm = VsphereVm.from_summary(
                        child, cur_path, vsphere=vsphere_name,
                        appname=self.appname, verbose=self.verbose, base_dir=self.base_dir)
                    vm_list.append(vm)
                elif as_vmw_obj:
                    vm_list.append(child)
                else:
                    vm_data = self._dict_from_vim_obj(child, cur_path)
                    vm_list.append(vm_data)

        return vm_list

    # -------------------------------------------------------------------------
    def _get_vm_childs(
            self, child, re_name, cur_path='', vsphere_name=None, is_template=None, depth=1,
            as_vmw_obj=False, as_obj=False, name_only=False, stop_at_found=False):

        vm_list = []
        if as_obj:
            vm_list = VsphereVmList(
                appname=self.appname, verbose=self.verbose, base_dir=self.base_dir,
                initialized=True)

        for sub_child in child.childEntity:

            child_path = ''
            if cur_path:
                child_path = cur_path + '/' + child.name
            else:
                child_path = child.name

            vms = self._get_vms(
                sub_child, re_name, cur_path=child_path, vsphere_name=vsphere_name,
                is_template=is_template, depth=(depth + 1), as_vmw_obj=as_vmw_obj,
                as_obj=as_obj, name_only=name_only, stop_at_found=stop_at_found)
            if vms:
                vm_list += vms
            if stop_at_found and vm_list:
                break

        return vm_list

    # -------------------------------------------------------------------------
    def poweron_vm(self, vm, max_wait=20, disconnect=False):
        """Power on the given virtual machine."""
        try:

            if not self.service_instance:
                self.connect()

            if isinstance(vm, vim.VirtualMachine):
                vm_obj = vm
                vm_name = vm.summary.config.name
            else:
                vm_name = vm
                vm_obj = self.get_vm(vm, as_vmw_obj=True)
                if not vm_obj:
                    raise VSphereVmNotFoundError(vm)

            if vm_obj.runtime.powerState.lower() == 'poweredon':
                LOG.info(_('VM {!r} is already powered on.').format(vm_name))
                return

            LOG.info(_('Powering on VM {!r} ...').format(vm_name))

            task = vm_obj.PowerOnVM_Task()
            self.wait_for_tasks([task], max_wait=max_wait)
            LOG.debug(_('VM {!r} successful powered on.').format(vm_name))

        finally:
            if disconnect:
                self.disconnect()

    # -------------------------------------------------------------------------
    def poweroff_vm(self, vm, max_wait=20, disconnect=False):
        """Power off the given virtual machine."""
        try:

            if not self.service_instance:
                self.connect()

            if isinstance(vm, vim.VirtualMachine):
                vm_obj = vm
                vm_name = vm.summary.config.name
            else:
                vm_name = vm
                vm_obj = self.get_vm(vm, as_vmw_obj=True)
                if not vm_obj:
                    raise VSphereVmNotFoundError(vm)

            if vm_obj.runtime.powerState.lower() == 'poweredoff':
                LOG.info(_('VM {!r} is already powered off.').format(vm_name))
                return

            LOG.info(_('Powering off VM {!r} ...').format(vm_name))

            task = vm_obj.PowerOffVM_Task()
            self.wait_for_tasks([task], max_wait=max_wait)
            LOG.debug(_('VM {!r} successful powered off.').format(vm_name))

        finally:
            if disconnect:
                self.disconnect()

    # -------------------------------------------------------------------------
    def ensure_vm_folders(self, folders, disconnect=False):
        """Ensure existence of the given VSphere VM folders."""
        LOG.debug(_('Ensuring existence of VSphere VM folders:') + '\n' + pp(folders))
        try:

            if not self.service_instance:
                self.connect()

            for folder in folders:
                self.ensure_vm_folder(folder, disconnect=False)

        finally:
            if disconnect:
                self.disconnect()

    # -------------------------------------------------------------------------
    def get_vm_folder(self, folder, disconnect=False):
        """Get the given VSphere VM folder as a vim.Folder object."""
        if self.verbose > 1:
            LOG.debug(_('Trying to get VM folder object for path {!r}.').format(folder))

        paths = []
        parts = folder.split('/')
        for i in range(0, len(parts)):
            path = '/'.join(parts[0:i + 1])
            paths.append(path)

        try:

            if not self.service_instance:
                self.connect()

            content = self.service_instance.RetrieveContent()
            dc = self.get_obj(content, [vim.Datacenter], self.dc)
            if not dc:
                raise VSphereDatacenterNotFoundError(self.dc)
            parent_folder = dc.vmFolder
            folder_object = None

            index = 0
            last = False
            for part in parts:
                abs_path = '/' + paths[index]
                if self.verbose > 1:
                    LOG.debug(_('Checking single VM folder {i}: {f!r}.').format(
                        i=index, f=abs_path))
                if index == len(parts) - 1:
                    last = True

                for child in parent_folder.childEntity:
                    if not isinstance(child, vim.Folder):
                        continue
                    if child.name != part:
                        continue
                    if self.verbose > 1:
                        LOG.debug(_('Found VM folder {n}, parent: {p}').format(
                            n=child.name, p=parent_folder.name))
                    parent_folder = child
                    if last:
                        folder_object = child
                index += 1
                if last:
                    break

            return folder_object

        finally:
            if disconnect:
                self.disconnect()

    # -------------------------------------------------------------------------
    def ensure_vm_folder(self, folder, disconnect=False):
        """Ensure existence of the given VSphere VM folder."""
        LOG.debug(_('Ensuring existence of VSphere VM folder {!r}.').format(folder))

        paths = []
        parts = folder.split('/')
        for i in range(0, len(parts)):
            path = '/'.join(parts[0:i + 1])
            paths.append(path)

        try:

            if not self.service_instance:
                self.connect()

            content = self.service_instance.RetrieveContent()
            dc = self.get_obj(content, [vim.Datacenter], self.dc)
            if not dc:
                raise VSphereDatacenterNotFoundError(self.dc)
            root_folder = dc.vmFolder

            index = 0
            for part in parts:

                abs_path = '/' + paths[index]
                folder_object = self.get_vm_folder(paths[index], disconnect=False)
                if folder_object:
                    LOG.debug(_('VM Folder {!r} already exists.').format(abs_path))
                else:
                    LOG.info(_('Creating VM folder {!r} ...').format(abs_path))
                    if self.simulate:
                        LOG.debug(_("Simulation mode, don't creating it."))
                        break
                    parent_folder = root_folder
                    if index != 0:
                        parent_folder = self.get_vm_folder(paths[index - 1], disconnect=False)
                    parent_folder.CreateFolder(part)
                index += 1

        finally:
            if disconnect:
                self.disconnect()

    # -------------------------------------------------------------------------
    def wait_for_tasks(
            self, tasks, poll_time=0.1, disconnect=False, max_wait=None, start_time=None):
        """Wat for finishing the given VSPhere task."""
        LOG.debug(_('Waiting for tasks to finish ...'))
        if not start_time:
            start_time = time.time()

        try:

            if not self.service_instance:
                self.connect()

            property_collector = self.service_instance.content.propertyCollector
            task_list = [str(task) for task in tasks]
            if max_wait:
                LOG.debug(_('Waiting at most {m} seconds for tasks {t} to finish ...').format(
                    m=max_wait, t=task_list))
            else:
                LOG.debug(_('Waiting for tasks {} to finish ...').format(task_list))
            # Create filter
            obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task) for task in tasks]
            property_spec = vmodl.query.PropertyCollector.PropertySpec(
                type=vim.Task, pathSet=[], all=True)
            filter_spec = vmodl.query.PropertyCollector.FilterSpec()
            filter_spec.objectSet = obj_specs
            filter_spec.propSet = [property_spec]
            pcfilter = property_collector.CreateFilter(filter_spec, True)
            try:
                version, state = None, None
                # Loop looking for updates till the state moves to a completed state.
                while len(task_list):
                    update = property_collector.WaitForUpdates(version)
                    for filter_set in update.filterSet:
                        if max_wait is not None and max_wait > 0:
                            time_diff = time.time() - start_time
                            if time_diff >= max_wait:
                                return False
                        time.sleep(poll_time)
                        LOG.debug(_('Waiting ...'))
                        for obj_set in filter_set.objectSet:
                            task = obj_set.obj
                            for change in obj_set.changeSet:
                                if change.name == 'info':
                                    state = change.val.state
                                elif change.name == 'info.state':
                                    state = change.val
                                else:
                                    continue

                                if not str(task) in task_list:
                                    continue

                                if state == vim.TaskInfo.State.success:
                                    # Remove task from taskList
                                    task_list.remove(str(task))
                                elif state == vim.TaskInfo.State.error:
                                    raise task.info.error
                        # Move to next version
                    version = update.version
            finally:
                if pcfilter:
                    pcfilter.Destroy()

        finally:
            if disconnect:
                self.disconnect()

        return True

    # -------------------------------------------------------------------------
    def create_vm(self, name, vm_folder, vm_config_spec, pool, max_wait=5):
        """Create the VM with a given name, VM folder an specification."""
        LOG.info(_('Creating VM {!r} ...').format(name))

        if self.simulate:
            LOG.info(_('Simulation mode - VM {!r} will not be created.').format(name))
            return

        start_time = time.time()

        task = vm_folder.CreateVM_Task(config=vm_config_spec, pool=pool)

        if not self.wait_for_tasks(
                [task], poll_time=0.2, max_wait=max_wait, start_time=start_time):
            time_diff = time.time() - start_time
            raise TimeoutCreateVmError(name, time_diff)

    # -------------------------------------------------------------------------
    def generate_vm_create_spec(
        self, name, datastore, disks=None, nw_interfaces=None, graphic_ram_mb=256,
            videao_ram_mb=32, boot_delay_secs=3, ram_mb=1024, num_cpus=1, ds_with_timestamp=False,
            os_version=DEFAULT_OS_VERSION, cfg_version=DEFAULT_VM_CFG_VERSION,
            enable_disk_uuid=True, disk_ctrl_type=None):
        """Create a specification for creating a virtual machine."""
        LOG.debug(_('Generating create spec for VM {!r} ...').format(name))

        # File definitions
        datastore_path = '[{ds}] {name}'.format(ds=datastore, name=name)
        if ds_with_timestamp:
            tstamp = datetime.datetime.now(tz=self.tz).strftime('%Y-%m-%d_%H-%M')
            datastore_path += '-' + tstamp
        datastore_path += '/'
        LOG.debug(_('Datastore path: {!r}').format(datastore_path))

        vm_path_name = datastore_path + name + '.vmx'
        LOG.debug(_('VM path name: {!r}').format(vm_path_name))

        vm_file_info = vim.vm.FileInfo(
            logDirectory=datastore_path, snapshotDirectory=datastore_path,
            suspendDirectory=datastore_path, vmPathName=vm_path_name)

        # Device definitions
        dev_changes = []

        dev_changes += self.generate_disk_spec(datastore_path, disks, disk_ctrl_type)
        dev_changes += self.generate_if_create_spec(nw_interfaces)

        # Graphic Card
        video_spec = vim.vm.device.VirtualDeviceSpec()
        video_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        video_spec.device = vim.vm.device.VirtualVideoCard()
        video_spec.device.enable3DSupport = False
        video_spec.device.graphicsMemorySizeInKB = graphic_ram_mb * 1024
        video_spec.device.numDisplays = 1
        video_spec.device.use3dRenderer = 'automatic'
        video_spec.device.videoRamSizeInKB = videao_ram_mb * 1024

        dev_changes.append(video_spec)

        # Some other flags
        vm_flags = vim.vm.FlagInfo()
        vm_flags.diskUuidEnabled = True

        # Some extra options and properties
        extra_opts = []

        created_opt = vim.option.OptionValue()
        created_opt.key = 'created'
        created_opt.value = int(time.time())
        extra_opts.append(created_opt)

        if enable_disk_uuid:
            enable_disk_uuid_option = vim.option.OptionValue()
            enable_disk_uuid_option.key = 'disk.EnableUUID'
            enable_disk_uuid_option.value = 'TRUE'
            extra_opts.append(enable_disk_uuid_option)

        # Set waiting for 3 second in BIOS before booting
        boot_opts = vim.vm.BootOptions()
        boot_opts.bootDelay = boot_delay_secs * 1000
        boot_opts.bootRetryEnabled = False
        boot_opts.enterBIOSSetup = False

        # Creating ConfigSpec
        config = vim.vm.ConfigSpec(
            name=name, deviceChange=dev_changes, flags=vm_flags, extraConfig=extra_opts,
            memoryMB=ram_mb, memoryHotAddEnabled=True, numCPUs=num_cpus,
            cpuHotAddEnabled=True, cpuHotRemoveEnabled=True, files=vm_file_info,
            guestId=os_version, version=cfg_version, bootOptions=boot_opts,
        )

        if self.verbose > 1:
            LOG.debug(_('Generated VM config:') + '\n' + pp(config))

        return config

    # -------------------------------------------------------------------------
    def generate_disk_spec(self, datastore_path, disks=None, disk_ctrl_type=None):
        """Create a specification for creating a virtual disk."""
        disk_sizes2create = []
        if disks:
            err_msg_tpl = _('Given disksize {!r} must be greater than zero.')
            if isinstance(disks, Number):
                if disks <= 0:
                    raise ValueError(err_msg_tpl.format(disks))
                disk_sizes2create.append(int(disks))
            elif isinstance(disks, Sequence):
                if isinstance(disks, str):
                    size = int(disks)
                    if size <= 0:
                        raise ValueError(err_msg_tpl.format(disks))
                    disk_sizes2create.append(size)
                else:
                    if len(disks) > 6:
                        msg = _('There may be created at most 6 disks, but {} were given.').format(
                            len(disks))
                        raise HandlerError(msg)
                    for disk in disks:
                        size = int(disk)
                        if size <= 0:
                            raise ValueError(err_msg_tpl.format(disk))
                        disk_sizes2create.append(size)

        if self.verbose > 1:
            if disk_sizes2create:
                msg = ngettext(
                    'Generating spec for SCSI controller and one disk: {d}',
                    'Generating spec for SCSI controller and {n} disks: {d}',
                    len(disk_sizes2create))
                LOG.debug(msg.format(n=len(disk_sizes2create), d=pp(disk_sizes2create)))
            else:
                LOG.debug(_('Generating spec for SCSI controller without disks.'))

        dev_changes = []

        # Creating SCSI Controller
        (ctrl_class, ctrl_desc, ctrl_name) = VsphereDiskController.get_disk_controller_class(
            disk_ctrl_type)
        LOG.debug(_('Using a {name!r} disk controller ({desc}).').format(
            name=ctrl_name, desc=ctrl_desc))

        scsi_ctr_spec = vim.vm.device.VirtualDeviceSpec()
        scsi_ctr_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        scsi_ctr_spec.device = ctrl_class()
        scsi_ctr_spec.device.key = 0
        scsi_ctr_spec.device.unitNumber = 1
        scsi_ctr_spec.device.sharedBus = 'noSharing'
        controller = scsi_ctr_spec.device

        dev_changes.append(scsi_ctr_spec)

        # Creating disks

        i = 0
        letter = 'a'

        for size in disk_sizes2create:

            size_kb = size * 1024 * 1024
            if self.verbose > 1:
                dname = 'sd{}'.format(letter)
                LOG.debug(_('Adding spec for disk {n!r} with {gb} GiB => {kb} KiByte.').format(
                    n=dname, gb=size, kb=size_kb))

            disk_spec = vim.vm.device.VirtualDeviceSpec()
            disk_spec.fileOperation = 'create'
            disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            disk_spec.device = vim.vm.device.VirtualDisk()
            disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
            disk_spec.device.backing.diskMode = 'persistent'
            disk_spec.device.backing.fileName = '{p}template-sd{ltr}.vmdk'.format(
                p=datastore_path, ltr=letter)
            disk_spec.device.unitNumber = i
            # disk_spec.device.key = 1
            disk_spec.device.capacityInKB = size_kb
            disk_spec.device.controllerKey = controller.key

            dev_changes.append(disk_spec)

            i += 1
            letter = chr(ord(letter) + 1)

        return dev_changes

    # -------------------------------------------------------------------------
    def generate_if_create_spec(self, nw_interfaces=None):
        """Create a specification for creating a virtual interface."""
        if not nw_interfaces:
            return []

        ifaces = []
        if isinstance(nw_interfaces, VsphereVmInterface):
            ifaces.append(nw_interfaces)
        elif is_sequence(nw_interfaces):
            for iface in nw_interfaces:
                if not isinstance(iface, VsphereVmInterface):
                    msg = _('Invalid Interface description {!r} given.').format(iface)
                    raise TypeError(msg)
                ifaces.append(iface)
        else:
            msg = _('Invalid Interface description {!r} given.').format(nw_interfaces)
            raise TypeError(msg)

        if not len(self.dv_portgroups) and not len(self.networks):
            self.get_networks()

        dev_changes = []
        dev_name = 'eth{}'
        i = -1

        for iface in ifaces:

            if self.verbose > 2:
                LOG.debug(_('Defined interface:') + '\n' + pp(iface.as_dict()))

            i += 1
            dname = dev_name.format(i)

            nic_spec = self._generate_if_create_spec(iface, dname)
            dev_changes.append(nic_spec)

        return dev_changes

    # -------------------------------------------------------------------------
    def _generate_if_create_spec(self, interface, dev_name):

        if self.verbose > 1:
            LOG.debug(_(
                'Adding spec for network interface {d!r} (Network {n!r}, '
                'MAC: {m!r}, summary: {s!r}).').format(
                d=dev_name, n=interface.network_name, m=interface.mac_address,
                s=interface.summary))

        nic_spec = vim.vm.device.VirtualDeviceSpec()

        nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        nic_spec.device = vim.vm.device.VirtualVmxnet3()
        nic_spec.device.deviceInfo = vim.Description()
        nic_spec.device.deviceInfo.label = dev_name
        if interface.summary:
            nic_spec.device.deviceInfo.summary = interface.summary

        if interface.network_name in self.dv_portgroups:
            portgroup = self.dv_portgroups[interface.network_name]
            dvs = self.dvs[portgroup.dvs_uuid]
            port_keys = dvs.search_port_keys(portgroup.key)
            port = dvs.find_port_by_portkey(port_keys[0])
            backing_device = portgroup.get_if_backing_device(port)
        elif interface.network_name in self.networks:
            network = self.networks[interface.network_name]
            backing_device = network.get_if_backing_device()
        else:
            msg = _(
                'Did not found neither a Distributed Virtual Port group nor a '
                'Virtual Network for network name {!r}.').format(interface.network_name)
            LOG.error(msg)
            return None

        nic_spec.device.backing = backing_device

        nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        nic_spec.device.connectable.startConnected = True
        nic_spec.device.connectable.allowGuestControl = True
        nic_spec.device.wakeOnLanEnabled = True
        if interface.mac_address:
            nic_spec.device.addressType = 'assigned'
            nic_spec.device.macAddress = interface.mac_address
        else:
            nic_spec.device.addressType = 'generated'

        if self.verbose > 3:
            LOG.debug(_('Networking device creation specification:') + ' ' + pp(nic_spec))

        return nic_spec

    # -------------------------------------------------------------------------
    def purge_vm(self, vm, max_wait=20, disconnect=False):
        """Purge a vitual machine completely from VSPhere."""
        try:

            if not self.service_instance:
                self.connect()

            if isinstance(vm, vim.VirtualMachine):
                vm_obj = vm
                vm_name = vm.summary.config.name
            else:
                vm_name = vm
                vm_obj = self.get_vm(vm, as_vmw_obj=True)
                if not vm_obj:
                    raise VSphereVmNotFoundError(vm)

            self.poweroff_vm(vm_obj)

            LOG.info(_('Purging VM {!r} ...').format(vm_name))

            task = vm_obj.Destroy_Task()
            self.wait_for_tasks([task], max_wait=max_wait)
            LOG.debug(_('VM {!r} successful removed.').format(vm_name))

        finally:
            if disconnect:
                self.disconnect()

    # -------------------------------------------------------------------------
    def set_mac_of_nic(self, vm, new_mac, nic_nr=0):
        """Set a virtual network interface to a new MAC address."""
        if not self.service_instance:
            self.connect()

        if isinstance(vm, vim.VirtualMachine):
            vm_obj = vm
            vm_name = vm.summary.config.name
        else:
            vm_name = vm
            vm_obj = self.get_vm(vm, as_vmw_obj=True)
            if not vm_obj:
                raise VSphereVmNotFoundError(vm)

        i = 0
        virtual_nic_device = None
        for dev in vm_obj.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                if i == nic_nr:
                    virtual_nic_device = dev
                    break
                i += 1

        if not virtual_nic_device:
            msg = _(
                'Did not found virtual ethernet device No. {no} ('
                'found {count} devices).').format(no=nic_nr, count=i)
            raise HandlerError(msg)

        virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
        virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        virtual_nic_spec.device = virtual_nic_device
        virtual_nic_spec.device.macAddress = new_mac
        virtual_nic_spec.device.backing = virtual_nic_device.backing
        virtual_nic_spec.device.wakeOnLanEnabled = virtual_nic_device.wakeOnLanEnabled
        virtual_nic_spec.device.connectable = virtual_nic_device.connectable

        dev_changes = []
        dev_changes.append(virtual_nic_spec)
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = dev_changes

        if self.verbose > 2:
            LOG.debug(_('Changes of MAC address:') + '\n' + pp(spec))

        task = vm_obj.ReconfigVM_Task(spec=spec)
        self.wait_for_tasks([task])
        LOG.debug(_('Successful changed MAC address of VM {v!r} to {m!r}.').format(
            v=vm_name, m=new_mac))

    # -------------------------------------------------------------------------
    def custom_field_name(self, key_id):
        """
        Try to evaluate the verbose custom field name by the given key ID.

        On the first attempt to get a lib/fb_vmware/ all available field
        names are cached in the dict self.custom_fields from the customFieldsManager.
        If the key could not be detected, None is returned.
        """
        if self.custom_fields is None:

            if self.verbose > 1:
                msg = _('Trying to detect all field names of custom field definitions.')

            self.custom_fields = {}

            try:
                if not self.service_instance:
                    self.connect()
                content = self.service_instance.RetrieveContent()
                cfm = content.customFieldsManager

                for custom_field in cfm.field:
                    self.custom_fields[custom_field.key] = custom_field.name

            except (
                    socket.timeout, urllib3.exceptions.ConnectTimeoutError,
                    urllib3.exceptions.MaxRetryError,
                    requests.exceptions.ConnectTimeout) as e:
                msg = _(
                    'Got a {c} on requesting custom field names from VSPhere {url}: {e}').format(
                    c=e.__class__.__name__, url=self.connect_info.url, e=e)
                raise VSphereExpectedError(msg)

            if self.verbose > 2:
                msg = _('Got custom field names from VSPhere {}:').format(self.connect_info.url)
                msg += '\n' + pp(self.custom_fields)
                LOG.debug(msg)

        if key_id in self.custom_fields:
            return self.custom_fields[key_id]

        return None


# =============================================================================

if __name__ == '__main__':

    pass

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 list
