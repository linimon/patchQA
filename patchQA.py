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
# patchQA: run a Bugzilla REST query and report results.
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

if ( len( sys.argv ) < 2 ):
    print( 'usage: ' + sys.argv[ 0 ] + ' <PR number>|<bugzilla REST query>' )
    sys.exit( 1 )
else:
    bugParms = sys.argv[ 1 ]

print( myName + ': running Bugzilla query for bugParms = ' + bugParms )

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
