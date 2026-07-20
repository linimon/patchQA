#!/usr/bin/env python

#
# SPDX-License-Identifier: BSD-2-Clause
#
# Copyright (c) 2025-2006, The FreeBSD Foundation
#
# This software was developed by Mark Linimon <linimon@FreeBSD.org>
# under sponsorship from the FreeBSD Foundation.
#

#
# patchQA: run a Bugzilla REST query and report results.
#

import argparse
import sys

import doOneBugQuery
import globalConfiguration

#verbose = False

parser = argparse.ArgumentParser(
    description='run a Bugzilla REST query and report results.'
)
parser.add_argument('bugParms', metavar='bugParms', type=str, nargs=1,
                    help='PR number or REST query')
parser.add_argument('--verbose', action='store_true',
                    help='set verbose mode for metadata')
args = parser.parse_args()
bugParms = str(args.bugParms[0])

#myName = ''
#try:
#    myName = sys.argv[ 0 ]
#except Exception as exception:
#    print( 'exception: problem with sys.argv[ 0 ]: ' + str( exception ) + '\n' )
#    sys.exit( 1 )
#
#if ( len( sys.argv ) < 2 ):
#    print( 'usage: ' + sys.argv[ 0 ] + ' <PR number>|<bugzilla REST query>' )
#    sys.exit( 1 )
#else:
#    bugParms = sys.argv[ 1 ]

#myName = parser.prog
print( parser.prog + ': running Bugzilla query for bugParms = ' + bugParms )

try:
    result = doOneBugQuery.doOneBugQuery( bugParms, verbose=args.verbose )
    if ( result == True ):
        print( parser.prog + ': finished.' )
    else:
        print( parser.prog + ': failure.' )

except Exception as exception:
    print( parser.prog + ': exception: ' + str( exception ) + '\n' )
    sys.exit( 1 )

sys.exit( 0 )
