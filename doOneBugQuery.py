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
# doOneBugQuery: wrapper for the parts of patchQA that do the real work.
#

import os
import re

import doOneBugReport
import getMetadataFromBugzilla

# TODO rework
gmfbVerbose = False
dobrVerbose = True

def doOneBugQuery( bugQuery, verbose ):

    bugsDict = None
    try:
        if ( verbose ):
            print( 'about to go fetch metadata for bugQuery ' + bugQuery + ' from Bugzilla\n' )

        # only pass True as verbose here if you want to get a dump of all progress
        bugsDict = getMetadataFromBugzilla.getMetadataFromBugzilla( bugQuery, gmfbVerbose )

        if bugsDict == None:
            return None
        else:
            if ( verbose ):
                print ( 'got bugsDict:\n' + str( bugsDict ) )

            for bugDict in bugsDict:
                if ( verbose ):
                    print( 'bugDict: ' + str( bugDict ) )
                doOneBugReport.doOneBugReport( bugDict, dobrVerbose )
            return True

    except Exception as exception:
        print( 'metadata evaluation failed: ' + str( exception ) + '\n' )
        return False

