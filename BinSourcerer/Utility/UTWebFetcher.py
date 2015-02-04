#!/usr/bin/env python
# -*-coding: utf8 -*-

########################################################################
# Copyright 2014 Concordia University
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
########################################################################
# This Python script is part of BinSourcerer, a framework
# for assembly to source code matching
#
# Status: Debug
#
########################################################################

import urllib
import urllib2
import random
#import requests

WEB_FETCHER_HTTP_USE_PROXY = True
WEB_FETCHER_HTTP_PROXY_LIST = ["127.0.0.1:8080"]
WEB_FETCHER_HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0"
WEB_FETCHER_HTTP_ACCEPT = "*/*"
WEB_FETCHER_HTTP_ACCEPT_LANGUAGE = "fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3"
WEB_FETCHER_HTTP_CONNECTION = "keep-alive"

#-----------------------------------------------------------------------
# Configuration agent
# The two next function are needed so the configuration manager will be
# able to provide configuration for this module.
# configurationNeed is called first. If no config for this 
# utility exists, user is prompted for utility configuration. If
# configuration exists, previous configs will be used. In all cases,
# configuration step is ended when configurationProvision
# is called with a configuration list as arg.
#-----------------------------------------------------------------------
def configurationNeed():
    return ["WEB_FETCHER_HTTP_USE_PROXY", "WEB_FETCHER_HTTP_PROXY_LIST", "WEB_FETCHER_HTTP_USER_AGENT",
            "WEB_FETCHER_HTTP_ACCEPT", "WEB_FETCHER_HTTP_ACCEPT_LANGUAGE", "WEB_FETCHER_HTTP_CONNECTION"]
            
def configurationProvision(utilityConfig=[]):
    global WEB_FETCHER_HTTP_USE_PROXY
    global WEB_FETCHER_HTTP_PROXY_LIST
    global WEB_FETCHER_HTTP_USER_AGENT
    global WEB_FETCHER_HTTP_ACCEPT
    global WEB_FETCHER_HTTP_ACCEPT_LANGUAGE
    global WEB_FETCHER_HTTP_CONNECTION
    
    WEB_FETCHER_HTTP_USE_PROXY = utilityConfig[0]
    WEB_FETCHER_HTTP_PROXY_LIST = utilityConfig[1]
    WEB_FETCHER_HTTP_USER_AGENT = utilityConfig[2]
    WEB_FETCHER_HTTP_ACCEPT = utilityConfig[3]
    WEB_FETCHER_HTTP_ACCEPT_LANGUAGE = utilityConfig[4]
    WEB_FETCHER_HTTP_CONNECTION = utilityConfig[5]


#-----------------------------------------------------------------------
# WebFetcher
# This class is a simple utility that aim to be a common web gate for
# all requests to the WWW
#-----------------------------------------------------------------------
class WebFetcher():

    def __init__(self, utMngr):
        self._manager = utMngr

    def wf_fetchPage(self, url):
        if not url:
            return ""
    
        opener = None
        
        if WEB_FETCHER_HTTP_USE_PROXY:
            #urlib2 will use proxies
            #First, Pick a proxy at random!
            proxy = random.randint(0, len(WEB_FETCHER_HTTP_PROXY_LIST)-1)
            #Then configure that proxy
            proxy = urllib2.ProxyHandler({"http": WEB_FETCHER_HTTP_PROXY_LIST[proxy], "https": WEB_FETCHER_HTTP_PROXY_LIST[proxy]})
            opener = urllib2.build_opener(proxy)
            #Ready to use, query will go trough the proxy!
        else:
            opener = urllib2.build_opener()
            
        opener.addheaders = [("User-agent", WEB_FETCHER_HTTP_USER_AGENT),
                                ("Accept", WEB_FETCHER_HTTP_ACCEPT),
                                ("Accept-Language", WEB_FETCHER_HTTP_ACCEPT_LANGUAGE),
                                ("Connection",WEB_FETCHER_HTTP_CONNECTION)]


        
        req = urllib2.Request(url)
        
        try:
            response = urllib2.urlopen(req)

            
        except IOError, e:
            if hasattr(e, "reason"):
                print(" --Could not connect to the server!")
                print(" --Reason: ", e.reason)
                return ""
            elif hasattr(e, "code"):
                print(" --The server couldn't fulfill the request.")
                print(" --Error code: ", e.code)
                return ""
        else: #No error detected
            return response.read()
            #return ""
'''
TODO remove when ok.            
def test():
    print(WEB_FETCHER_HTTP_CONNECTION)
'''
            
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    webFetch = WebFetcher()


   
