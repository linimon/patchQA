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
# testPatchQA: test code for patchQA developer.
#
# Most likely not of interest to general users.
#

import sys

import doOneBugQuery
import globalConfiguration

verbose = False

myName = ''
try:
    myName = sys.argv[ 0 ]
except Exception as exception:
    print( 'exception: problem with sys.argv[ 0 ]: ' + str( exception ) + '\n' )
    sys.exit( 1 )

# test harness for URL getter

if ( False ):
    bugQuery = None
    print( globalConfiguration.getBugzillaRestURL( bugQuery ) )
    bugQuery = ''
    print( globalConfiguration.getBugzillaRestURL( bugQuery ) )
    bugQuery = '283810'
    print( globalConfiguration.getBugzillaRestURL( bugQuery ) )
    bugQuery = '281294,282904'
    print( globalConfiguration.getBugzillaRestURL( bugQuery ) )
    bugQuery = \
        'product=Base%20System' + \
        '&component=kern' + \
        '&f1=attachments.ispatch' + \
        '&f2=creation_ts&o1=equals&o2=greaterthaneq' + \
        '&v1=1&v2=2025-01-01' + \
        '&query_format=advanced' + \
        '&resolution=---'
    print( globalConfiguration.getBugzillaRestURL( bugQuery ) )

# test harness for various Problem Report cases.  These are in no
# particular order.

# 20250214: ok after rewrite.
#bugParms = '281294'
#
# 20250214: ok after rewrite.
#bugParms = '281294,282904'
#
# 20250211: patch reports as success even though the result is mangled TODO
#bugParms = '282904'
#
# 20250214: mostly right
#bugParms = \
#'product=Base%20System' \
#'&component=kern' \
#'&f1=attachments.ispatch' \
#'&v1=1' \
#'&f2=creation_ts' \
#'&o1=equals' \
#'&o2=greaterthaneq' \
#'&v2=2024-01-01' \
#'&query_format=advanced' \
#'&resolution=---'
#
# 20250218: output for kern was doit4.kern.forever.out
#bugParms = \
#'product=Base%20System' \
#'&component=bin' \
#'&f1=attachments.ispatch' \
#'&v1=1' \
#'&f2=creation_ts' \
#'&o1=equals' \
#'&o2=greaterthaneq' \
#'&v2=2000-01-01' \
#'&query_format=advanced' \
#'&resolution=---'
#
# 20250209: Base System/conf/isPatch is a bridge too far TODO
#bugParms = \
#'&product=Base%20System' \
#'component=conf' \
#'&f1=attachments.ispatch' \
#'&o1=equals' \
#'&v1=1' \
#'&f2=creation_ts' \
#'&o1=equals' \
#'&o2=greaterthaneq' \
#'&v2=2025-01-01' \
#'&query_format=advanced' \
#'&resolution=---'
#
# 20250211: well, it makes a *lot* of output vs. the 170 PRs
#bugParms = 'component=Individual%20Port%28s%29&f1=attachments.ispatch&f2=creation_ts&o1=equals&o2=greaterthaneq&product=Ports%20%26%20Packages&query_format=advanced&resolution=---&v1=1&v2=2025-01-01'
#
# 20250216: only 7: mostly right
#bugParms = 'component=kern&f1=attachments.ispatch&f2=creation_ts&o1=equals&o2=greaterthaneq&product=Base%20System&query_format=advanced&resolution=---&v1=1&v2=2025-01-01'
#
# 20250211: doOneBugReport: 'bool' object is not iterable: (had to hack return value from fromstring() )
# 20250214: after rewrite: cannot figure out filename.
# this PR is now fixed/closed.
#bugParms = '76491'
#
# 20250214: ok after rewrite.
#bugParms = '284283'
#
# 20250211: ERROR - premature end of source file b'lang/gauche/Makefile' at hunk 2
#bugParms = '283810'
#
# 20250214: after rewrite, has multiple attachments, some are patches, and some of those are obsolete: still
# can't figure out how to patch options.c.
# is now fixed/closed
#bugParms = '218980'
#
# 20250216: all 2025: test manual pages fix: looks ok
# 20250216: all 2025: test 'new port' fixes: looks ok
# 20250218: all 2025: rerun with latest changes.
# 20250226: all 2025: rerun with latest changes.  "did not apply" = 12/225
#bugParms = \
#'&f1=attachments.ispatch' \
#'&v1=1' \
#'&f2=creation_ts' \
#'&o1=equals' \
#'&o2=greaterthaneq' \
#'&v2=2025-01-01' \
#'&query_format=advanced' \
#'&resolution=---'
#
# just one year.  already done as doit.2024.out.
# https://bugs.freebsd.org/bugzilla/buglist.cgi?chfield=%5BBug%20creation%5D&chfieldto=Now&f1=attachments.ispatch&f2=creation_ts&f3=creation_ts&list_id=811267&o1=equals&o2=greaterthaneq&o3=lessthan&order=Importance&query_format=advanced&resolution=---&v1=1&v2=2024-01-01&v3=2025-01-01
bugParms = \
'&f1=attachments.ispatch' \
'&v1=1' \
'&f2=creation_ts' \
'&o1=equals' \
'&o2=greaterthaneq' \
'&v2=2023-01-01' \
'&f3=creation_ts' \
'&o3=lessthan' \
'&v3=2024-01-01' \
'&query_format=advanced' \
'&resolution=---'
#
# 20250216: new port with devel/Makefile: devel/Makefile not patched TODO
#bugParms = '284703'
#
# 20250216: existing Makefile and distinfo: had "dash problem".  should be fixed.
#bugParms = '197538'
#
# 20250216: one single Makefile
# edited PR, s/sysutils/filesystems/, but even so:
# zsh: no matches found: */*fuse*nt*
# TODO fix this ailing PR.
#bugParms = '206978'
#
# 20250217: missapplied ports patch
#bugParms = '284094'
#
# 20250218: was: dash problem: now, patch does not apply
#bugParms = '197538'
#
# 20250218: was: dash problem: believed fixed
#bugParms = '276675'
#
# 20250218: was: 'group': believed fixed
#bugParms = '284434'
#
# 20250218: 'empty patchSets': correctly handled but not yet understood.
#bugParms = '284321'
#
# 20250218: 'empty patchSets': correctly handled but not yet understood.
#bugParms = '283785'
#
# 20250218: 'empty patchSets': correctly handled but not yet understood.
#bugParms = '280809'
#
# 20250218: 'empty patchSets': this is a shar.
#bugParms = '279849'
#
# 20250218: 'empty patchSets': no valid patches left
#bugParms = '278518'
#
# 20250218: 'empty patchSets': bad patch
#bugParms = '277126'
#
# 20250220: empty patchset: all patches are obsolete
#bugParms = '281612'
#
# 20250220: empty patchset: I had submitted a bogus diff for devel/bugzilla50; hand edited; fixed!
#bugParms = '283897'
#
# 20250220: poor-quality patch; hand edited; fixed!
#bugParms = '280202'
#
# 20250223: has stupid datestamp after whitespace.  fixed.
#bugParms = '167822'
#
# 20250223: etc/rc.d/blah: TODO NOTYET
#bugParms = '145440' 

print( myName + ': running query for bugParms = ' + bugParms )

try:
    result = doOneBugQuery.doOneBugQuery( bugParms, verbose )
    if ( result == True ):
        print( myName + ': finished.' )
    else:
        print( myName + ': failure.' )

except Exception as exception:
    print( myName + ': exception: ' + str( exception ) + '\n' )
    sys.exit( 1 )

sys.exit( 0 )
