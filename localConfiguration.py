#!/usr/bin/env python

#
# SPDX-License-Identifier: BSD-2-Clause
#
# Copyright (c) 2025 The FreeBSD Foundation
#
# This software was developed by Mark Linimon <linimon@FreeBSD.org>
# under sponsorship from the FreeBSD Foundation.
#

#
# localConfiguration: local definitions for patchQA.  Customize for your site.
#

FREEBSD_BUGZILLA                = 'https://bugs.FreeBSD.org/bugzilla'

# TODO 20250124 parameterize
SKIP_IF_ASSIGNED                = False
SKIP_IF_ASSIGNED_TO_LIST        = False    # set False to process 'assigned to mailing list'
SKIP_IF_CLOSED                  = True
SKIP_IF_IN_PROGRESS             = True


freebsdProductToLocalRepoMap = {
    'Base System' :     '/home/freebsd/freebsd-src/',
    'Documentation' :   '/home/freebsd/freebsd-doc/',
    'Ports & Packages': '/home/freebsd/freebsd-ports/',
}

def getLocalBugzillaURL():
    return FREEBSD_BUGZILLA

def getLocalProductToLocalRepoMap():
    return freebsdProductToLocalRepoMap

