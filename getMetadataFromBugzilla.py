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
# getMetadataFromBugzilla: extract metadata from a Bugzilla instance via REST.
#

import base64
import json
import requests
import sys

import localConfiguration
import globalConfiguration

def getMetadataFromBugzillaInner( bugQuery, verbose ):

    if ( bugQuery == None ):
        raise ValueError( "getMetadataFromBugzilla: parameter bugQuery must be non-None" )

    if ( verbose ):
        print ( 'at getMetadataFromBugzilla( ' + bugQuery + ' )\n' )

    URL = globalConfiguration.getBugzillaRestURL( bugQuery )

    if ( verbose ):
        print ('using ' + URL + ' for metadata fetching\n')

    response = requests.get( URL )
    if ( verbose ):
        print ('response: ' + str(response) + '\n')
        # expected: <Response [200]>

    headers = response.headers
    if ( verbose ):
        print ('headers: ' + str(headers) + '\n')
        # expected: {'Date': 'Thu, 30 Jan 2025 01:46:52 GMT', 'Content-Type': 'application/json; charset=UTF-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Server': 'Apache', 'Access-control-allow-headers': 'origin, content-type, accept, x-requested-with', 'Access-control-allow-origin': '*', 'X-content-type-options': 'nosniff', 'X-frame-options': 'SAMEORIGIN', 'X-xss-protection': '1; mode=block', 'Set-Cookie': 'Bugzilla_login_request_cookie=99QcHv1K72; domain=bugstest.freebsd.org; path=/bugzilla/; HttpOnly', 'Etag': 'ydwYAJ2TdFqUc2bZ+peJ0A', 'X-Varnish': '17269736', 'Age': '0', 'Accept-Ranges': 'bytes', 'Via': '1.1 wfe1.nyi.FreeBSD.org', 'X-Cache': 'MISS', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'}

    bugsOuterDict = response.json()
    if ( verbose ):
        print ('getMetadataFromBugzillaInner: ' + str(bugsOuterDict) + '\n')
        # expected: { 'faults': [], 'bugs': [{'version': 'Latest', 'creation_time': '2015-02-11T14:57:50Z', 'is_open': True, 'op_sys': 'Any', 'url': '', 'keywords': ['patch'], 'assigned_to': 'freebsd-ports-bugs@FreeBSD.org', 'product': 'Ports & Packages', 'severity': 'Affects Only Me', 'classification': 'Unclassified', 'resolution': '', 'flags': [{'requestee': 'nobody@FreeBSD.org', 'creation_date': '2015-02-11T14:57:50Z', 'status': '?', 'id': 2436, 'name': 'maintainer-feedback', 'modification_date': '2015-02-11T14:57:50Z', 'setter': 'bugzilla@FreeBSD.org', 'type_id': 3}], 'id': 197538, 'last_change_time': '2015-10-27T13:05:37Z', 'is_cc_accessible': True, 'target_milestone': '---', 'deadline': None, 'is_creator_accessible': True, 'alias': [], 'cc': [], 'qa_contact': '', 'component': 'Individual Port(s)', 'priority': '---', 'platform': 'Any', 'status': 'Open', 'summary': 'databases/tuning-primer: MariaDB 10.x errors with joins and InnoDB status', 'whiteboard': '', 'creator_detail': {'real_name': 'Nobody User', 'email': 'nobody@FreeBSD.org', 'id': 1748, 'name': 'nobody@FreeBSD.org'}, 'is_confirmed': True, 'dupe_of': None, 'blocks': [], 'assigned_to_detail': {'name': 'freebsd-ports-bugs@FreeBSD.org', 'id': 13, 'real_name': '', 'email': 'freebsd-ports-bugs@FreeBSD.org'}, 'depends_on': [], 'creator': 'nobody@FreeBSD.org', 'groups': [], 'cc_detail': [], 'see_also': []}]}

    bugsInnerDict = ( bugsOuterDict[ globalConfiguration.REST_LEVEL1_KEY_BUGS ] )
    if ( verbose ):
        print ('bugsInnerDict: ' + str(bugsInnerDict) + '\n')
        # expected: {'is_creator_accessible': True, 'cc': [], 'last_change_time': '2015-10-27T13:05:37Z', 'status': 'Open', 'cc_detail': [], 'blocks': [], 'version': 'Latest', 'product': 'Ports & Packages', 'platform': 'Any', 'depends_on': [], 'op_sys': 'Any', 'alias': [], 'target_milestone': '---', 'creation_time': '2015-02-11T14:57:50Z', 'dupe_of': None, 'url': '', 'component': 'Individual Port(s)', 'resolution': '', 'is_cc_accessible': True, 'groups': [], 'creator_detail': {'id': 1748, 'email': 'nobody@FreeBSD.org', 'real_name': 'Nobody User', 'name': 'nobody@FreeBSD.org'}, 'priority': '---', 'flags': [{'requestee': 'nobody@FreeBSD.org', 'setter': 'bugzilla@FreeBSD.org', 'id': 2436, 'creation_date': '2015-02-11T14:57:50Z', 'type_id': 3, 'name': 'maintainer-feedback', 'modification_date': '2015-02-11T14:57:50Z', 'status': '?'}], 'assigned_to': 'freebsd-ports-bugs@FreeBSD.org', 'deadline': None, 'is_open': True, 'see_also': [], 'creator': 'nobody@FreeBSD.org', 'severity': 'Affects Only Me', 'keywords': ['patch'], 'qa_contact': '', 'summary': 'databases/tuning-primer: MariaDB 10.x errors with joins and InnoDB status', 'whiteboard': '', 'classification': 'Unclassified', 'is_confirmed': True, 'assigned_to_detail': {'id': 13, 'name': 'freebsd-ports-bugs@FreeBSD.org', 'email': 'freebsd-ports-bugs@FreeBSD.org', 'real_name': ''}, 'id': 197538}

    return bugsInnerDict


def getMetadataFromBugzilla( bugQuery, verbose ):

    try:
        return getMetadataFromBugzillaInner( bugQuery, verbose )
    except Exception as exception:
        raise Exception( 'at getMetadataFromBugzilla ' + str( exception ) + '\n' )

