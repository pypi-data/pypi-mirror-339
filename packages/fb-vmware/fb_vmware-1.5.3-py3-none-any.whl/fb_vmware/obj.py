#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: The module for a base VSphere class.

@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2025 by Frank Brehm, Berlin
"""
from __future__ import absolute_import

# Standard modules
import copy
import logging
import re

# Third party modules
from fb_tools.common import RE_TF_NAME
from fb_tools.common import pp
from fb_tools.obj import FbBaseObject

# Own modules
from .errors import VSphereNameError
from .xlate import XLATOR

__version__ = '1.3.5'
LOG = logging.getLogger(__name__)

_ = XLATOR.gettext

DEFAULT_OBJ_STATUS = 'gray'
OBJ_STATUS_GREEN = 'green'


# =============================================================================
class VsphereObject(FbBaseObject):
    """
    A base class for some other VSphere classes.

    It is especially intended for classes mapping other classes from the pyVmomi package.
    """

    re_ws = re.compile(r'\s+')

    repr_fields = (
        'name', 'obj_type', 'name_prefix', 'status', 'config_status',
        'appname', 'verbose', 'version')
    available_status_color = ['red', 'yellow', 'green', 'gray']

    # -------------------------------------------------------------------------
    def __init__(
        self, name=None, obj_type=None, name_prefix='unknown', status=DEFAULT_OBJ_STATUS,
            config_status=DEFAULT_OBJ_STATUS, appname=None, verbose=0, version=__version__,
            base_dir=None, initialized=None):
        """Initialize a VsphereObject object."""
        self._name = None
        self._obj_type = None
        self._name_prefix = None
        self._status = None
        self._config_status = None

        super(VsphereObject, self).__init__(
            appname=appname, verbose=verbose, version=version, base_dir=base_dir)

        self.status = status
        self.config_status = config_status
        self.obj_type = obj_type
        self.name_prefix = name_prefix
        self.name = name

        if initialized is not None:
            self.initialized = initialized

    # -----------------------------------------------------------
    @property
    def obj_type(self):
        """Return the type of the VSphere object."""
        return self._obj_type

    @obj_type.setter
    def obj_type(self, value):

        if value is None:
            msg = _('The type of a {} may not be None.').format('VsphereObject')
            raise TypeError(msg)

        val = self.re_ws.sub('', str(value))
        if val == '':
            msg = _('Invalid {w}.{p} {v!r}.').format(
                w='VsphereObject', p='type', v=value)
            raise ValueError(msg)

        self._obj_type = val

    # -----------------------------------------------------------
    @property
    def status(self):
        """Overall alarm status of the object."""
        return self._status

    @status.setter
    def status(self, value):
        if value is None:
            self._status = 'gray'
            return

        val = str(value).strip().lower()
        if val == '':
            self._status = 'gray'
            return
        if val not in self.available_status_color:
            msg = _('Invalid {w}.{p} {v!r}.').format(
                w='VsphereObject', p='status', v=value)
            raise ValueError(msg)

        self._status = val

    # -----------------------------------------------------------
    @property
    def config_status(self):
        """Overall config status of the object."""
        return self._config_status

    @config_status.setter
    def config_status(self, value):
        if value is None:
            self._config_status = 'gray'
            return

        val = str(value).strip().lower()
        if val == '':
            self._config_status = 'gray'
            return
        if val not in self.available_status_color:
            msg = _('Invalid {w}.{p} {v!r}.').format(
                w='VsphereObject', p='config_status', v=value)
            raise ValueError(msg)

        self._config_status = val

    # -----------------------------------------------------------
    @property
    def name_prefix(self):
        """Return the prefix for the terraform name."""
        return self._name_prefix

    @name_prefix.setter
    def name_prefix(self, value):

        if value is None:
            raise TypeError(_('The name prefix of a {} may not be None.').format('VsphereObject'))

        val = self.re_ws.sub('', str(value))
        if val == '':
            msg = _('Invalid name prefix {p!r} for a {o}.').format(p=value, o='VsphereObject')
            raise ValueError(msg)

        self._name_prefix = val

    # -----------------------------------------------------------
    @property
    def name(self):
        """Return the name of the object."""
        return self._name

    @name.setter
    def name(self, value):

        if value is None:
            raise VSphereNameError(value, self.obj_type)

        val = self.re_ws.sub('_', str(value).strip())
        if val == '':
            raise VSphereNameError(value, self.obj_type)

        self._name = val

    # -----------------------------------------------------------
    @property
    def qual_name(self):
        """Return the qualified name of the object, including object_type and name."""
        if self.obj_type is None:
            if self.name is None:
                return ''
            else:
                return self.name.lower()
        if self.name is None:
            return self.obj_type.lower() + '.'
        return self.obj_type.lower() + '.' + self.name.lower()

    # -----------------------------------------------------------
    @property
    def tf_name(self):
        """Return the name of the bject how used in terraform."""
        if self.name is None:
            return None
        return self.name_prefix + '_' + RE_TF_NAME.sub('_', self.name.lower())

    # -----------------------------------------------------------
    @property
    def var_name(self):
        """Return the name of the variable used in terraform definitions."""
        return self.obj_type + '_' + RE_TF_NAME.sub('_', self.name.lower())

    # -------------------------------------------------------------------------
    def as_dict(self, short=True):
        """
        Transform the elements of the object into a dict.

        @param short: don't include local properties in resulting dict.
        @type short: bool

        @return: structure as dict
        @rtype:  dict
        """
        res = super(VsphereObject, self).as_dict(short=short)

        res['name'] = self.name
        res['qual_name'] = self.qual_name
        res['obj_type'] = self.obj_type
        res['name_prefix'] = self.name_prefix
        res['tf_name'] = self.tf_name
        res['var_name'] = self.var_name
        res['status'] = self.status
        res['config_status'] = self.config_status

        if self.verbose > 3:
            res['repr_fields'] = copy.copy(self.repr_fields)

        return res

    # -------------------------------------------------------------------------
    def __str__(self):
        """
        Typecast function for translating object structure into a string.

        @return: structure as string
        @rtype:  str
        """
        return pp(self.as_dict(short=True))

    # -------------------------------------------------------------------------
    def __repr__(self):
        """Typecast into a string for reproduction."""
        out = '<%s(' % (self.__class__.__name__)

        fields = []
        for field in self.repr_fields:
            token = '{f}={v!r}'.format(f=field, v=getattr(self, field))
            fields.append(token)

        out += ', '.join(fields) + ')>'
        return out

    # -------------------------------------------------------------------------
    def __lt__(self, other):
        """Magic method for using it as the '<'-operator."""
        if not isinstance(other, VsphereObject):
            msg = _('Object {{!r}} is not a {} object.').format('VsphereObject')
            raise TypeError(msg.format(other))

        return self.qual_name < other.qual_name

    # -------------------------------------------------------------------------
    def __gt__(self, other):
        """Magic method for using it as the '>'.operator."""
        if not isinstance(other, VsphereObject):
            msg = _('Object {{!r}} is not a {} object.').format('VsphereObject')
            raise TypeError(msg.format(other))

        return self.qual_name > other.qual_name

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        """Magic method for using it as the '=='-operator."""
        if self.verbose > 4:
            LOG.debug(_('Comparing {} objects ...').format(self.__class__.__name__))

        if not isinstance(other, VsphereObject):
            return False

        return self.qual_name == other.qual_name

    # -------------------------------------------------------------------------
    def __le__(self, other):
        """Magic method for using it as the '<='-operator."""
        if not isinstance(other, VsphereObject):
            msg = _('Object {{!r}} is not a {} object.').format('VsphereObject')
            raise TypeError(msg.format(other))

        if self == other:
            return True

        return self.qual_name < other.qual_name

    # -------------------------------------------------------------------------
    def __ge__(self, other):
        """Magic method for using it as the '>='-operator."""
        if not isinstance(other, VsphereObject):
            msg = _('Object {{!r}} is not a {} object.').format('VsphereObject')
            raise TypeError(msg.format(other))

        if self == other:
            return True

        return self.qual_name > other.qual_name


# =============================================================================

if __name__ == '__main__':

    pass

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 list
