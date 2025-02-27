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
# doOneBugReport: do an individual bug report.
#
# TODO: refactor out FreeBSD-specific "business logic".
#

import os
import re

import globalConfiguration
import localConfiguration
import getAttachmentsFromBugzilla
import getMetadataFromBugzilla

subdirectoryRegex = globalConfiguration.getSubdirectoryRegex()
A_B_PATTERN = '^[ab]/'
A_B_REGEX = re.compile( '^[ab]/' )

# TODO NOTYET
# if starts with etc/, try:
#   prepend libexec/rc
#   prepend usr.sbin/periodic

# TODO rework
gppVerbose   = True
attVerbose   = False
glrVerbose   = False

def getLocalRepo( product, component, verbose ):

    localRepo = None
    try:
        # TODO parameterize
        if ( component == 'Manual Pages' ):
            product = 'Base System'
        localRepo = localConfiguration.getLocalProductToLocalRepoMap()[ product ]
        if ( verbose ):
            print( 'repo: ' + str( localRepo ) + '\n' )
    except Exception as exception:
        print( 'there is no repository for Product ' + str( exception ) + '\n' )
        return None

    return localRepo


def getPossiblePath( initialGuess, patchSet, verbose ):

    possiblePath = initialGuess
    patchIterator = iter( patchSet )

    # look for a target filename inside each patch.
    while True:
        try:
            patch = next( patchIterator )

            target = patch.target.decode( "utf-8" )
            if ( target == None ):
                # should not happen.
                continue
            else:
                # ignore anything (e.g. datestamp) after whitespace
                if target.find( ' ' )  != -1:
                    target = target.split( maxsplit=1 )[0]

            if ( verbose ):
                print( 'got target: ' + target )

            # throw out obvious scapegoats (usually produced by git diff)
            target = re.sub( A_B_REGEX, '', target, count=1 )

            possibleFilename = os.path.join( possiblePath, target )
            if ( verbose ):
                print( 'possibleFilename: ' + str( possibleFilename ) )

            if (os.path.isfile( possibleFilename ) ):
                # it's likely that we do not need to qualify the path.
                return possiblePath
            else:
                # that's not enough, so continue; may have to use Summary
                if ( verbose ):
                    print( 'not os.path.isfile( ' + str( possibleFilename ) + ' )\n' )

            # >= 2 slashes?  probably a full path
            # TODO only for Ports & Packages?
            slashes =  target.count( '/' )
            if ( slashes >= 2 ):
                if ( verbose ):
                    print( 'slashes >= 2: return PossiblePath' )
                # XXX MCL TODO 20250224
                return possiblePath

            # TODO factor out magic constants
            if ( target.endswith( 'Makefile' ) ):
                # can be ambiguous.  Keep looking through patches.
                if ( verbose ):
                    print( 'target endswith Makefile.  Keep looking.' )
                continue

        except StopIteration:
            break

        except Exception as exception:
            # probably will never get here.
            print( 'getPossiblePath: unable to reason about patches: ' + str( exception ) + '\n' )
            return None

        return possiblePath


def doOneBugReport( bugDict, verbose ):

    bug_id = None
    product = None
    component = None
    summary = None

    # begin REST-specific work

    bug_id = str( bugDict[ globalConfiguration.REST_LEVEL2_KEY_BUG_ID ] )
    if ( verbose ):
        print( '\ndoOneBugReport:' )
        print( 'got bug_id: ' + bug_id )
    product = bugDict[ globalConfiguration.REST_LEVEL2_KEY_PRODUCT ]
    if ( verbose ):
        print( 'got product: ' + str( product ) )
    component = bugDict[ globalConfiguration.REST_LEVEL2_KEY_COMPONENT ]
    if ( verbose ):
        print( 'got component: ' + str( component ) )
    summary = bugDict[ globalConfiguration.REST_LEVEL2_KEY_SUMMARY ]
    if ( verbose ):
        print( 'got summary: ' + str( summary ) )

    # begin FreeBSD-specific "business logic"

    assignee = False
    try:
        assignee = bugDict[ globalConfiguration.REST_LEVEL2_KEY_ASSIGNEE ]
        if ( verbose ):
            print( 'got assignee: ' + str( assignee ) )
        if ( str.find( assignee, 'bugs@FreeBSD.org' ) != -1 ):
            if ( verbose ):
                print( 'bug ' + str( bug_id ) + ' is unassigned.' )
        else: 
            if ( str.find( assignee, '@FreeBSD.org' ) != -1 ):
                # TODO figure out if mailing list.
                if ( localConfiguration.SKIP_IF_ASSIGNED ):
                    print( 'bug ' + str( bug_id ) + ' is already assigned to a non-default user; skipping.' )
                    return True
                else:
                    print( 'bug ' + str( bug_id ) + ' is already assigned, but ignoring that for now.' )
    except Exception as exception:
        print( 'doOneBugReport: assignee lookup failed: ' + str( exception ) + '\n' )
        return False

    status = None
    try:
        status = bugDict[ globalConfiguration.REST_LEVEL2_KEY_STATUS ]
        if ( status == 'Closed' ):
            if ( localConfiguration.SKIP_IF_CLOSED ):
                print( str( bug_id ) + ' is already closed; there is nothing to do.' )
                return True
            else:
                print( 'bug ' + str( bug_id ) + ' is already closed, but ignoring that for now.' )
        else:
            if ( status == 'In Progress' ):
                if ( localConfiguration.SKIP_IF_IN_PROGRESS ):
                    print( 'bug ' + str( bug_id ) + ' is already In Progress; skipping.' )
                    return True
                else:
                    print( 'bug ' + str( bug_id ) + ' is already In Progress, but ignoring that for now.' )
            else:
                if ( status == 'New' or status == 'Open' ):
                    print( 'bug ' + str( bug_id ) + ' is available to be worked on.' )
                else:
                    raise Exception( "unknown Status " + status)
    except Exception as exception:
        print( 'status lookup failed: ' + str( exception ) + '\n' )
        return False

    localRepo = getLocalRepo( product, component, glrVerbose )
    if localRepo == None:
        print( 'there is no repository for Product ' + str( product ) + '\n' )
        return False

    patchSets = None
    try:
        patchSets = getAttachmentsFromBugzilla.getAttachmentsFromBugzilla( bug_id, attVerbose )
        # if there was nothing to do, I guess it "succeeds"
        if ( patchSets == None ):
            return True
        else:
            if ( False ):
                print( 'got patchSets:\n' + str( patchSets ) )
    except Exception as exception:
        print( 'fetch failed: ' + str( exception ) + '\n' )
        return False

    patchSetsIterator = iter( patchSets )
    patchSet = None

    # now you have an iterator of patchSets.  Examine each one.
    while True:
        try:
            patchSet = next( patchSetsIterator )
            if ( patchSet == None or len( patchSet ) == 0 ):
                if ( verbose ):
                    print( 'patchSet is empty.' )
                continue

            # preen the patch by trying to figure out the possible path.
            # upstream code assumes only one repo, so we have to do some duplicate work here.
            likelyPath = localRepo
        
            try: 

                likelyPath = getPossiblePath( likelyPath, patchSet, gppVerbose )
                if ( likelyPath != None ):
                    break
                else:
                    if ( verbose ):
                        print( 'unable to determine possible path to the patch, case 1.' )
                    try:
                        # TODO possibly only applicable for ports?
                        possibleSubdirectory = re.search( subdirectoryRegex, summary ).group( 0 )
                        if ( possibleSubdirectory != None ):
                            if ( verbose ):
                                print( 'possibleSubdirectory: ' + possibleSubdirectory )
                            likelyPath = os.path.join( localRepo, possibleSubdirectory )
                            break
                        else:
                            pass
                    except Exception as exception:
                        pass

                    # TODO wrong for new port?
                    if ( likelyPath == None ):
                        if ( verbose ):
                            print( 'unable to determine possible path to the patch, case 2.' )
                        return False
                    else:
                        if ( verbose ):
                            print( 'likelyPath: ' + likelyPath )

            except Exception as exception:
                print( 'doOneBugReport: ' + str( exception ) + '\n' )
                return False
        
        except StopIteration:
            break

    # end outer 'while True'

    # number of prefixes to strip
    strip = 0
    # fuzziness
    fuzz = True
    patchApplied = False

    if ( patchSet == None or len( patchSet ) == 0 ):
        print( 'doOneBugReport: no valid patches were found.' )
        return False

    try:
        # TODO this code does not throw Exceptions, it just logs!
        patchApplied = patchSet.apply( strip, likelyPath, fuzz )
        # non-fatal error.  try to keep going.
        if ( not patchApplied ):
            if ( verbose ):
                print( 'doOneBugReport: patch did not apply.' )
        else:
            if ( verbose ):
                print( 'doOneBugReport: patch applied.' )

    except Exception as exception:
        # probably never reached
        print( 'doOneBugReport: unable to reason about patches: ' + str( exception ) + '\n' )
        return False

    # return True if all patches were examined
    return True

