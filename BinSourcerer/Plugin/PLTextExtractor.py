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

UI_DEFAULT_EXTRACTOR_CHOICE = ""

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
    return ["UI_DEFAULT_EXTRACTOR_CHOICE"]
            
def configurationProvision(utilityConfig=[]):
    global UI_DEFAULT_EXTRACTOR_CHOICE
    UI_DEFAULT_EXTRACTOR_CHOICE = utilityConfig=[0]

#----------------------------------------------------------------------
# Plugin type
# Since many plugins with diferent capabilities can be integrated
# to the framework, we need a general method to understand the
# use of each plugin in a unified way. The value returned by this method
# will allow the framework to call the right operations on the plugin.
# for more information about plugin types, see related comment inside
# BSPluginManager.py
#----------------------------------------------------------------------
def identifyPluginType():
    return ["extractor"] 
    
#-----------------------------------------------------------------------
# Plugin name
# This is used so the framework can give a name to a specific plugin
# The name will be used to visualy identify each plugins.
#-----------------------------------------------------------------------
def identifyPlugin():
    return ["TextExtractor", "Features File"] #First item in list have to have the same name as main class name. Second item in list is visual name
     

#-----------------------------------------------------------------------
# Check when showed in the UI
# This method is used to tell UI if this choice should be checked
# when showed in the UI. Visual identification(identifyPlugin()[1]) is used as choice.
#-----------------------------------------------------------------------
def defaultCheckChoice():
    selfIdentity = identifyPlugin()
    
    if selfIdentity[1] == UI_DEFAULT_EXTRACTOR_CHOICE:
        return True
    return False

     
#-----------------------------------------------------------------------
# TextExtractor 
# This class implements ...
#-----------------------------------------------------------------------
class TextExtractor():

    def __init__(self, plMngr):
        self._manager = plMngr
    
    def getUI(self):
        return "TextExtractorUI"
    #
    # This method is in charge for features extraction
    # since text extractor is a special case where 
    # features are already extracted from an external source
    # this logic is quite simple. In fact, this classe is only
    # present in order to fully comply with framework construct.
    #
    def pluginExtract(self, functionList, selectedEas):
        result = []
        
        for function in functionList:
            if function[0][1] in selectedEas:
                result.append((function[0][0], function[1]))
                
        return result
            

        
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    x = TextExtractor(None)
