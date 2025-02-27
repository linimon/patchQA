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
# getAttachmentsFromBugzilla: get attachments from a Bugzilla instance via REST.
#

import base64
import json
import logging
import logging.config
import requests
import sys

# 20250205: using py-patch_ng as upstream instead of our own code
import patch_ng
from patch_ng import Patch
from patch_ng import PatchSet
from patch_ng import fromfile, fromstring

logging.config.fileConfig( 'patchQA.logging.conf' )
logger = logging.getLogger( 'patch_ng' )

import localConfiguration
import globalConfiguration

def getAttachmentsFromBugzillaInner( bug_id, verbose ):

    if ( bug_id == None or not str( bug_id ).isnumeric() ):
        raise ValueError( "getAttachmentsFromBugzilla: parameter bug_id must be numeric" )

    if ( verbose ):
        print ( 'at getAttachmentsFromBugzilla( ' + bug_id + ' )\n' )

    URL = globalConfiguration.getBugzillaURL() + '/rest/bug/' + bug_id
    if ( verbose ):
        print ('using ' + URL + ' for patch fetching\n')

    response = requests.get( URL )
    if ( verbose ):
        print ('response: ' + str(response) + '\n')
        # expected: <Response [200]>

    headers = response.headers
    if ( verbose ):
        print ('headers: ' + str(headers) + '\n')
        # expected: {'Date': 'Thu, 30 Jan 2025 01:46:52 GMT', 'Content-Type': 'application/json; charset=UTF-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Server': 'Apache', 'Access-control-allow-headers': 'origin, content-type, accept, x-requested-with', 'Access-control-allow-origin': '*', 'X-content-type-options': 'nosniff', 'X-frame-options': 'SAMEORIGIN', 'X-xss-protection': '1; mode=block', 'Set-Cookie': 'Bugzilla_login_request_cookie=99QcHv1K72; domain=bugstest.freebsd.org; path=/bugzilla/; HttpOnly', 'Etag': 'ydwYAJ2TdFqUc2bZ+peJ0A', 'X-Varnish': '17269736', 'Age': '0', 'Accept-Ranges': 'bytes', 'Via': '1.1 wfe1.nyi.FreeBSD.org', 'X-Cache': 'MISS', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'}

    restOuterDict = response.json()
    if ( verbose ):
        print ('restOuterDict: ' + str(restOuterDict) + '\n')
        # expected: { 'faults': [], 'bugs': [{'version': 'Latest', 'creation_time': '2015-02-11T14:57:50Z', 'is_open': True, 'op_sys': 'Any', 'url': '', 'keywords': ['patch'], 'assigned_to': 'freebsd-ports-bugs@FreeBSD.org', 'product': 'Ports & Packages', 'severity': 'Affects Only Me', 'classification': 'Unclassified', 'resolution': '', 'flags': [{'requestee': 'nobody@FreeBSD.org', 'creation_date': '2015-02-11T14:57:50Z', 'status': '?', 'id': 2436, 'name': 'maintainer-feedback', 'modification_date': '2015-02-11T14:57:50Z', 'setter': 'bugzilla@FreeBSD.org', 'type_id': 3}], 'id': 197538, 'last_change_time': '2015-10-27T13:05:37Z', 'is_cc_accessible': True, 'target_milestone': '---', 'deadline': None, 'is_creator_accessible': True, 'alias': [], 'cc': [], 'qa_contact': '', 'component': 'Individual Port(s)', 'priority': '---', 'platform': 'Any', 'status': 'Open', 'summary': 'databases/tuning-primer: MariaDB 10.x errors with joins and InnoDB status', 'whiteboard': '', 'creator_detail': {'real_name': 'Nobody User', 'email': 'nobody@FreeBSD.org', 'id': 1748, 'name': 'nobody@FreeBSD.org'}, 'is_confirmed': True, 'dupe_of': None, 'blocks': [], 'assigned_to_detail': {'name': 'freebsd-ports-bugs@FreeBSD.org', 'id': 13, 'real_name': '', 'email': 'freebsd-ports-bugs@FreeBSD.org'}, 'depends_on': [], 'creator': 'nobody@FreeBSD.org', 'groups': [], 'cc_detail': [], 'see_also': []}]}

    restInnerDict = ( restOuterDict[ globalConfiguration.REST_LEVEL1_KEY_BUGS ][ 0 ] )
    if ( verbose ):
        print ('restInnerDict: ' + str(restInnerDict) + '\n')
        # expected: {'is_creator_accessible': True, 'cc': [], 'last_change_time': '2015-10-27T13:05:37Z', 'status': 'Open', 'cc_detail': [], 'blocks': [], 'version': 'Latest', 'product': 'Ports & Packages', 'platform': 'Any', 'depends_on': [], 'op_sys': 'Any', 'alias': [], 'target_milestone': '---', 'creation_time': '2015-02-11T14:57:50Z', 'dupe_of': None, 'url': '', 'component': 'Individual Port(s)', 'resolution': '', 'is_cc_accessible': True, 'groups': [], 'creator_detail': {'id': 1748, 'email': 'nobody@FreeBSD.org', 'real_name': 'Nobody User', 'name': 'nobody@FreeBSD.org'}, 'priority': '---', 'flags': [{'requestee': 'nobody@FreeBSD.org', 'setter': 'bugzilla@FreeBSD.org', 'id': 2436, 'creation_date': '2015-02-11T14:57:50Z', 'type_id': 3, 'name': 'maintainer-feedback', 'modification_date': '2015-02-11T14:57:50Z', 'status': '?'}], 'assigned_to': 'freebsd-ports-bugs@FreeBSD.org', 'deadline': None, 'is_open': True, 'see_also': [], 'creator': 'nobody@FreeBSD.org', 'severity': 'Affects Only Me', 'keywords': ['patch'], 'qa_contact': '', 'summary': 'databases/tuning-primer: MariaDB 10.x errors with joins and InnoDB status', 'whiteboard': '', 'classification': 'Unclassified', 'is_confirmed': True, 'assigned_to_detail': {'id': 13, 'name': 'freebsd-ports-bugs@FreeBSD.org', 'email': 'freebsd-ports-bugs@FreeBSD.org', 'real_name': ''}, 'id': 197538}

    product = restInnerDict[ globalConfiguration.REST_LEVEL2_KEY_PRODUCT ]
    if verbose:
        print ('product: ' + str(product) )

    component = restInnerDict[ globalConfiguration.REST_LEVEL2_KEY_COMPONENT ]
    if verbose:
        print ('component: ' + str(component) )

    summary = restInnerDict[ globalConfiguration.REST_LEVEL2_KEY_SUMMARY ]
    if verbose:
        print ('summary from bug: ' + str(summary) )

    attachmentURL = URL + '/attachment'
    #attachmentJSON = requests.get(attachmentURL)
    response = requests.get( attachmentURL )

    # print ('json attachment dict: ' + str(attachmentJSON.json()) )
    # expected: {'bugs': {'197538': [{'creation_time': '2015-02-11T14:57:50Z', 'is_obsolete': 0, 'id': 152868, 'bug_id': 197538, 'flags': [], 'is_patch': 1, 'summary': 'Files diff', 'is_private': 0, 'data': 'SW5kZXg6IE1ha2VmaWxlCj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KLS0tIE1ha2VmaWxlCShyZXZpc2lvbiAzNzg4MzkpCisrKyBNYWtlZmlsZQkod29ya2luZyBjb3B5KQpAQCAtMSwxNyArMSwxNiBAQAotIyBDcmVhdGVkIGJ5OiBKb2UgSG9ybiA8am9laG9ybkBnbWFpbC5jb20+CisjIENyZWF0ZWQgYnk6IE1hdHRpYSBCYXNvbmUgPG1hdHRpYS5iYXNvbmVAZ21haWwuY29tPgogIyAkRnJlZUJTRCQKIAogUE9SVE5BTUU9CXR1bmluZy1wcmltZXIKIFBPUlRWRVJTSU9OPQkxLjYucjEKIENBVEVHT1JJRVM9CWRhdGFiYXNlcwotTUFTVEVSX1NJVEVTPQlodHRwOi8vbGF1bmNocGFkLm5ldC9teXNxbC0ke1BPUlROQU1FfS90cnVuay8xLjYtcjEvK2Rvd25sb2FkLworTUFTVEVSX1NJVEVTPQlodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vbWF0dGlhYmFzb25lLyR7UE9SVE5BTUV9L21hc3Rlci8KIERJU1ROQU1FPQkke1BPUlROQU1FfS5zaAogRVhUUkFDVF9TVUZYPQogRVhUUkFDVF9PTkxZPQotRElTVF9TVUJESVI9CSR7UE9SVE5BTUV9LyR7RElTVFZFUlNJT059CiAKLU1BSU5UQUlORVI9CWpvZWhvcm5AZ21haWwuY29tCi1DT01NRU5UPQlNeVNRTCBwZXJmb3JtYW5jZSB0dW5pbmcgcHJpbWVyIHNjcmlwdAorTUFJTlRBSU5FUj0JbWF0dGlhLmJhc29uZUBnbWFpbC5jb20KK0NPTU1FTlQ9CU15U1FMIHBlcmZvcm1hbmNlIHR1bmluZyBwcmltZXIgc2NyaXB0IHdpdGggTWFyaWFEQiBzdXBwb3J0CiAKIExJQ0VOU0U9CUdQTHYyCiAKQEAgLTIxLDcgKzIwLDcgQEAKIFBMSVNUX0ZJTEVTPQliaW4vJHtQT1JUTkFNRX0KIAogZG8taW5zdGFsbDoKLQkke0lOU1RBTExfU0NSSVBUfSAke0RJU1RESVJ9LyR7RElTVF9TVUJESVJ9LyR7UE9SVE5BTUV9LnNoIFwKKwkke0lOU1RBTExfU0NSSVBUfSAke0RJU1RESVJ9LyR7UE9SVE5BTUV9LnNoIFwKIAkJJHtTVEFHRURJUn0ke1BSRUZJWH0vYmluLyR7UE9SVE5BTUV9CiAKIC5pbmNsdWRlIDxic2QucG9ydC5taz4KSW5kZXg6IGRpc3RpbmZvCj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KLS0tIGRpc3RpbmZvCShyZXZpc2lvbiAzNzg4MzkpCisrKyBkaXN0aW5mbwkod29ya2luZyBjb3B5KQpAQCAtMSwyICsxLDIgQEAKLVNIQTI1NiAodHVuaW5nLXByaW1lci8xLjYucjEvdHVuaW5nLXByaW1lci5zaCkgPSA3OTA2Mzg4ZGU1NjE2ZTAyMjNkZWRlMTBkYjM2OGIyMTlhZDM3ZWQ2YmFiNzJlMmVlZDFlYmYxOTI5ZTM4NDIwCi1TSVpFICh0dW5pbmctcHJpbWVyLzEuNi5yMS90dW5pbmctcHJpbWVyLnNoKSA9IDUxODkyCitTSEEyNTYgKHR1bmluZy1wcmltZXIuc2gpID0gNjM4YjFhMTYxMTExZGIwMDRhNzlkZjhhMzRkYWI0MmRiMTEzY2U2ZTZmYzQ5Y2MxOGM0OTYwZDliMDI1YWFjZAorU0laRSAodHVuaW5nLXByaW1lci5zaCkgPSA1MjEzMQpJbmRleDogcGtnLWRlc2NyCj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KLS0tIHBrZy1kZXNjcgkocmV2aXNpb24gMzc4ODM5KQorKysgcGtnLWRlc2NyCSh3b3JraW5nIGNvcHkpCkBAIC0yLDYgKzIsNyBAQAogYW5kICJTSE9XIFZBUklBQkxFUyBMSUtFLi4uIiB0aGVuIGF0dGVtcHRzIHRvIHByb2R1Y2UKIHNhbmUgcmVjb21tZW5kYXRpb25zIGZvciB0dW5pbmcgc2VydmVyIHZhcmlhYmxlcy4KIAotSXQgaXMgY29tcGF0aWJsZSB3aXRoIGFsbCB2ZXJzaW9ucyBvZiBNeVNRTCAzLjIzIC0gNS4xLgorSXQgaXMgY29tcGF0aWJsZSB3aXRoIGFsbCB2ZXJzaW9ucyBvZiBNeVNRTCAzLjIzIC0gNS41IGFuZAorTWFyaWFEQiA1LjUvMTAueAogCi1XV1c6CWh0dHBzOi8vbGF1bmNocGFkLm5ldC9teXNxbC10dW5pbmctcHJpbWVyCitXV1c6IGh0dHBzOi8vZ2l0aHViLmNvbS9tYXR0aWFiYXNvbmUvdHVuaW5nLXByaW1lciAK', 'creator': 'nobody@FreeBSD.org', 'content_type': 'text/plain', 'size': 2013, 'last_change_time': '2015-02-11T14:57:50Z', 'file_name': 'tuning-primer-1.6.r1.diff'}]}, 'attachments': {}}

    attachmentsDict = response.json()
    # print ('attachmentsDict[bugs]: ' +str(attachmentsDict['bugs']) )
    # expected: {'creation_time': '2015-02-11T14:57:50Z', 'is_obsolete': 0, 'id': 152868, 'bug_id': 197538, 'flags': [], 'is_patch': 1, 'summary': 'Files diff', 'is_private': 0, 'data': 'SW5kZXg6IE1ha2VmaWxlCj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KLS0tIE1ha2VmaWxlCShyZXZpc2lvbiAzNzg4MzkpCisrKyBNYWtlZmlsZQkod29ya2luZyBjb3B5KQpAQCAtMSwxNyArMSwxNiBAQAotIyBDcmVhdGVkIGJ5OiBKb2UgSG9ybiA8am9laG9ybkBnbWFpbC5jb20+CisjIENyZWF0ZWQgYnk6IE1hdHRpYSBCYXNvbmUgPG1hdHRpYS5iYXNvbmVAZ21haWwuY29tPgogIyAkRnJlZUJTRCQKIAogUE9SVE5BTUU9CXR1bmluZy1wcmltZXIKIFBPUlRWRVJTSU9OPQkxLjYucjEKIENBVEVHT1JJRVM9CWRhdGFiYXNlcwotTUFTVEVSX1NJVEVTPQlodHRwOi8vbGF1bmNocGFkLm5ldC9teXNxbC0ke1BPUlROQU1FfS90cnVuay8xLjYtcjEvK2Rvd25sb2FkLworTUFTVEVSX1NJVEVTPQlodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vbWF0dGlhYmFzb25lLyR7UE9SVE5BTUV9L21hc3Rlci8KIERJU1ROQU1FPQkke1BPUlROQU1FfS5zaAogRVhUUkFDVF9TVUZYPQogRVhUUkFDVF9PTkxZPQotRElTVF9TVUJESVI9CSR7UE9SVE5BTUV9LyR7RElTVFZFUlNJT059CiAKLU1BSU5UQUlORVI9CWpvZWhvcm5AZ21haWwuY29tCi1DT01NRU5UPQlNeVNRTCBwZXJmb3JtYW5jZSB0dW5pbmcgcHJpbWVyIHNjcmlwdAorTUFJTlRBSU5FUj0JbWF0dGlhLmJhc29uZUBnbWFpbC5jb20KK0NPTU1FTlQ9CU15U1FMIHBlcmZvcm1hbmNlIHR1bmluZyBwcmltZXIgc2NyaXB0IHdpdGggTWFyaWFEQiBzdXBwb3J0CiAKIExJQ0VOU0U9CUdQTHYyCiAKQEAgLTIxLDcgKzIwLDcgQEAKIFBMSVNUX0ZJTEVTPQliaW4vJHtQT1JUTkFNRX0KIAogZG8taW5zdGFsbDoKLQkke0lOU1RBTExfU0NSSVBUfSAke0RJU1RESVJ9LyR7RElTVF9TVUJESVJ9LyR7UE9SVE5BTUV9LnNoIFwKKwkke0lOU1RBTExfU0NSSVBUfSAke0RJU1RESVJ9LyR7UE9SVE5BTUV9LnNoIFwKIAkJJHtTVEFHRURJUn0ke1BSRUZJWH0vYmluLyR7UE9SVE5BTUV9CiAKIC5pbmNsdWRlIDxic2QucG9ydC5taz4KSW5kZXg6IGRpc3RpbmZvCj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KLS0tIGRpc3RpbmZvCShyZXZpc2lvbiAzNzg4MzkpCisrKyBkaXN0aW5mbwkod29ya2luZyBjb3B5KQpAQCAtMSwyICsxLDIgQEAKLVNIQTI1NiAodHVuaW5nLXByaW1lci8xLjYucjEvdHVuaW5nLXByaW1lci5zaCkgPSA3OTA2Mzg4ZGU1NjE2ZTAyMjNkZWRlMTBkYjM2OGIyMTlhZDM3ZWQ2YmFiNzJlMmVlZDFlYmYxOTI5ZTM4NDIwCi1TSVpFICh0dW5pbmctcHJpbWVyLzEuNi5yMS90dW5pbmctcHJpbWVyLnNoKSA9IDUxODkyCitTSEEyNTYgKHR1bmluZy1wcmltZXIuc2gpID0gNjM4YjFhMTYxMTExZGIwMDRhNzlkZjhhMzRkYWI0MmRiMTEzY2U2ZTZmYzQ5Y2MxOGM0OTYwZDliMDI1YWFjZAorU0laRSAodHVuaW5nLXByaW1lci5zaCkgPSA1MjEzMQpJbmRleDogcGtnLWRlc2NyCj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KLS0tIHBrZy1kZXNjcgkocmV2aXNpb24gMzc4ODM5KQorKysgcGtnLWRlc2NyCSh3b3JraW5nIGNvcHkpCkBAIC0yLDYgKzIsNyBAQAogYW5kICJTSE9XIFZBUklBQkxFUyBMSUtFLi4uIiB0aGVuIGF0dGVtcHRzIHRvIHByb2R1Y2UKIHNhbmUgcmVjb21tZW5kYXRpb25zIGZvciB0dW5pbmcgc2VydmVyIHZhcmlhYmxlcy4KIAotSXQgaXMgY29tcGF0aWJsZSB3aXRoIGFsbCB2ZXJzaW9ucyBvZiBNeVNRTCAzLjIzIC0gNS4xLgorSXQgaXMgY29tcGF0aWJsZSB3aXRoIGFsbCB2ZXJzaW9ucyBvZiBNeVNRTCAzLjIzIC0gNS41IGFuZAorTWFyaWFEQiA1LjUvMTAueAogCi1XV1c6CWh0dHBzOi8vbGF1bmNocGFkLm5ldC9teXNxbC10dW5pbmctcHJpbWVyCitXV1c6IGh0dHBzOi8vZ2l0aHViLmNvbS9tYXR0aWFiYXNvbmUvdHVuaW5nLXByaW1lciAK', 'creator': 'nobody@FreeBSD.org', 'content_type': 'text/plain', 'size': 2013, 'last_change_time': '2015-02-11T14:57:50Z', 'file_name': 'tuning-primer-1.6.r1.diff'}

    returnableList = []
    attachmentList = attachmentsDict[ globalConfiguration.REST_LEVEL1_KEY_BUGS] [bug_id ]
    if ( verbose ):
        print( 'attachmentList = ' + str( attachmentList ) )
    nAttachments = len( attachmentList )
    if ( nAttachments == 0 ):
        if ( verbose ):
            print( 'no attachments found.' )
        return None
    else:
        if ( verbose ):
            if ( nAttachments == 1 ):
                print( 'found one attachment.' )
            else:
                print( 'found ' + str( nAttachments ) + ' attachments.' )

    attachmentDictIterator = iter( attachmentList )

    while True:
        try:
            attachmentDict = next( attachmentDictIterator )

            if ( attachmentDict == None ):
                pass
            #print( 'attachmentDict: attachmentDict = ' + str( attachmentDict ) )

            #b'Index: Makefile\n===================================================================\n--- Makefile\t(revision 378839)\n+++ Makefile\t(working copy)\n@@ -1,17 +1,16 @@\n-# Created by: Joe Horn <joehorn@gmail.com>\n+# Created by: Mattia Basone <mattia.basone@gmail.com>\n # $FreeBSD$\n \n PORTNAME=\ttuning-primer\n PORTVERSION=\t1.6.r1\n CATEGORIES=\tdatabases\n-MASTER_SITES=\thttp://launchpad.net/mysql-${PORTNAME}/trunk/1.6-r1/+download/\n+MASTER_SITES=\thttps://raw.githubusercontent.com/mattiabasone/${PORTNAME}/master/\n DISTNAME=\t${PORTNAME}.sh\n EXTRACT_SUFX=\n EXTRACT_ONLY=\n-DIST_SUBDIR=\t${PORTNAME}/${DISTVERSION}\n \n-MAINTAINER=\tjoehorn@gmail.com\n-COMMENT=\tMySQL performance tuning primer script\n+MAINTAINER=\tmattia.basone@gmail.com\n+COMMENT=\tMySQL performance tuning primer script with MariaDB support\n \n LICENSE=\tGPLv2\n \n@@ -21,7 +20,7 @@\n PLIST_FILES=\tbin/${PORTNAME}\n \n do-install:\n-\t${INSTALL_SCRIPT} ${DISTDIR}/${DIST_SUBDIR}/${PORTNAME}.sh \\\n+\t${INSTALL_SCRIPT} ${DISTDIR}/${PORTNAME}.sh \\\n \t\t${STAGEDIR}${PREFIX}/bin/${PORTNAME}\n \n .include <bsd.port.mk>\nIndex: distinfo\n===================================================================\n--- distinfo\t(revision 378839)\n+++ distinfo\t(working copy)\n@@ -1,2 +1,2 @@\n-SHA256 (tuning-primer/1.6.r1/tuning-primer.sh) = 7906388de5616e0223dede10db368b219ad37ed6bab72e2eed1ebf1929e38420\n-SIZE (tuning-primer/1.6.r1/tuning-primer.sh) = 51892\n+SHA256 (tuning-primer.sh) = 638b1a161111db004a79df8a34dab42db113ce6e6fc49cc18c4960d9b025aacd\n+SIZE (tuning-primer.sh) = 52131\nIndex: pkg-descr\n===================================================================\n--- pkg-descr\t(revision 378839)\n+++ pkg-descr\t(working copy)\n@@ -2,6 +2,7 @@\n and "SHOW VARIABLES LIKE..." then attempts to produce\n sane recommendations for tuning server variables.\n \n-It is compatible with all versions of MySQL 3.23 - 5.1.\n+It is compatible with all versions of MySQL 3.23 - 5.5 and\n+MariaDB 5.5/10.x\n \n-WWW:\thttps://launchpad.net/mysql-tuning-primer\n+WWW: https://github.com/mattiabasone/tuning-primer \n'

            # evaluate disqualifying metadata from each patch

            try:
                is_obsolete = attachmentDict[ 'is_obsolete' ]
                if ( is_obsolete == 0 ):
                    if ( verbose ):
                        print( 'attachment is not obsolete.' )
                else:
                    if ( verbose ):
                        print( 'attachment is obsolete, skipping.' )
                    continue
            except:
                print( 'attachment is not valid (has no is_obsolete), skipping.' )
                continue

            try:
                is_patch = attachmentDict[ 'is_patch' ]
                if ( is_patch == 1 ):
                    if ( verbose ):
                        print( 'attachment is patch.' )
                else:
                    if ( verbose ):
                        print( 'attachment is not patch, skipping.' )
                    continue
            except:
                print( 'attachment is not valid (has no is_patch), skipping.' )
                continue

            # now evaluate the payload
            decodedPatch = base64.b64decode( attachmentDict[ globalConfiguration.REST_LEVEL3_KEY_DATA ] )
            decodedPatchString = str( decodedPatch, encoding='utf-8' )
            if ( verbose ):
                print ('decodedPatchString:\n' + decodedPatchString + '\n\n')
            #(actual patch appears)

            # TODO rewrite nasty upstream interface
            # Parse text string and return PatchSet() object (or False if parsing fails)
            patchSet = fromstring( decodedPatch )
            if ( patchSet == False ):
                if ( verbose ):
                    print( 'patchSet returned false.' )
                continue
            else:
                if ( verbose ):
                    print( 'patchSet = ' + str( patchSet ) + '\n' )

            returnableList.append ( patchSet )

        except StopIteration:
            #print( 'patch iteration done.' )
            break

        except Exception as exception:
            print( 'at getAttachmentsFromBugzillaInner: ' + str( exception ) + '\n' )
            return None

    return returnableList


def getAttachmentsFromBugzilla( bug_id, verbose ):

    try:
        return getAttachmentsFromBugzillaInner( bug_id, verbose )
    except Exception as exception:
        raise Exception( 'at getAttachmentsFromBugzilla: ' + str( exception ) + '\n' )

