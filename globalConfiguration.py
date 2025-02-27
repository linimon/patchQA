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
# globalConfiguration: global definitions for patchQA.  Customize for your site.
#

import re

import localConfiguration

# definitions for parsing JSON REST return values
REST_LEVEL1_KEY_BUGS            = 'bugs'
#
REST_LEVEL2_KEY_ASSIGNEE        = 'assigned_to'
REST_LEVEL2_KEY_BUG_ID          = 'id'
REST_LEVEL2_KEY_COMPONENT       = 'component'
REST_LEVEL2_KEY_PRODUCT         = 'product'
REST_LEVEL2_KEY_STATUS          = 'status'
REST_LEVEL2_KEY_SUMMARY         = 'summary'
REST_LEVEL2_KEY_VERSION         = 'version'
#
# example: (((jsondict['bugs'][bug_id][n]['data'])))
REST_LEVEL3_KEY_DATA            = 'data'

# <anything><alphanum><slash><alphanum>><anything>
SUBDIRECTORY_REGEX              = re.compile( '[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-]+' )


def getBugzillaURL():
    return localConfiguration.getLocalBugzillaURL()


def getBugzillaRestURL( parm ):

    restURL = getBugzillaURL() + '/rest/bug' ;

    if ( parm != None and len( parm ) > 0 ):
        if ( parm.isnumeric () ):
            # e.g. /rest/bug/284073
            return restURL + '/' + str( parm )
        else:
            if ( parm.replace( ',', '' ).isnumeric() ):
                # e.g. /rest/bug?id=281294,282904
                return restURL + '?id=' + str( parm )
            else:
                # all others
                return restURL + '?=' + str( parm )

    return restURL


def getSubdirectoryRegex():
    return SUBDIRECTORY_REGEX

