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

import md5
import os

REPORT_MANAGER_OUTPUT_REPORT_PATH = ""

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
    return ["REPORT_MANAGER_OUTPUT_REPORT_PATH"]
            
def configurationProvision(utilityConfig=[]):
    global REPORT_MANAGER_OUTPUT_REPORT_PATH
    REPORT_MANAGER_OUTPUT_REPORT_PATH = utilityConfig[0]


#-----------------------------------------------------------------------
# WebFetcher
# This class is a simple utility that aim to be a common web gate for
# all requests to the WWW
#-----------------------------------------------------------------------
class RessourcesAccessor():

    def __init__(self, utMngr):
        self._manager = utMngr

    #
    # This function will save data to a given path using data md5sum
    # as file name. The file name is returned to the user.
    #
    def ra_saveToRessource(self, data, path=REPORT_MANAGER_OUTPUT_REPORT_PATH):
        #This is required when running inside IDA pro
        #IDA Python does not seems to evaluate path=REPORT_MANAGER_OUTPUT_REPORT_PATH
        #in method signature since REPORT_MANAGER_OUTPUT_REPORT_PATH is originaly = ""
        if REPORT_MANAGER_OUTPUT_REPORT_PATH != "" and path == "":
            path = REPORT_MANAGER_OUTPUT_REPORT_PATH
            
        if not data:
            return ""
            
        if not os.path.isdir(path):
            #Creating directory for support files
            os.mkdir(path)
    
        pageMd5Sum = md5.new(data).hexdigest()
        pageMd5Sum = path + pageMd5Sum + ".html"
        f = open(pageMd5Sum, "w")
        f.write(data)
        f.close()
        return pageMd5Sum
    

#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    rscrAcc = RessourcesAccessor()


   
