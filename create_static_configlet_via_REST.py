#!/usr/bin/env python
#
# Copyright (c) 2019, Arista Networks
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   Neither the name of Arista Networks nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN

__author__ = 'Petr Ankudinov'

# Demo configlet builder to create a static configlet via REST API

from time import time as time
from datetime import datetime as datetime
from cvplibrary import RestClient
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def time_stamp():
    """
    time_stamp function can be used for debugging or to display timestamp for specific event to a user
    :return: returns current system time as a string in Y-M-D H-M-S format
    """
    time_not_formatted = time()
    time_formatted = datetime.fromtimestamp(time_not_formatted).strftime('%Y-%m-%d:%H:%M:%S.%f')
    return time_formatted

    
# simple procedure to send REST API GET/POST request

def query(postfix, http_type='GET', data=None):
    response = False
    query_string = 'https://localhost/cvpservice/' + postfix
    client = RestClient(query_string, http_type)
    if http_type == 'POST':
       client.setRawData(json.dumps(data))
    if client.connect():
       response = json.loads(client.getResponse())
    return response


if __name__ == '__main__':
    
    configlet_name = 'TEST_CFGLET'
    
    config = '\n'.join([
        '! Configlet content should be defined here',
        'interface loopback123',
        '  description TEST_LOOPBACK',
        ])
    
    print ('\n'.join([
        '! Print is not required',
        '! But can display some log'
        ]))
      
    # get configlet list
    existing_configlets = query('configlet/getConfiglets.do?startIndex=0&endIndex=0')
    configlet_exists = False
    for configlet in existing_configlets['data']:
        if configlet['name'] == configlet_name:
            configlet_exists = True
    
    if configlet_exists:
        print ('! Failed to create configlet as a confilet with the same name already exists!')
    else:
        data = {'name': configlet_name, 'config': config}
        query('configlet/addConfiglet.do', http_type='POST', data=data)
        print ('! Configlet %s created at %s' % (configlet_name, time_stamp()))
    
