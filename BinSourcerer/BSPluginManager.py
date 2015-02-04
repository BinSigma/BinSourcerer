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
# Description:
# This Python script is part of BinSourcerer, a framework
# for assembly to source code matching
#
# Status: Debug
#
########################################################################


'''
*************************************************************************
*************************************************************************
IMPORTANT: This comment is used so users of the framework knows how to
use it. Any changes to the plug-in architecture HAVE to be reflected inside
this comment.
*************************************************************************
*************************************************************************

About the plug-in architecture
In BinSourcerer framework, plug-ins are dynamically loaded. This file is responsible
for plug-in management. In order to handle each plug-in as it's supposed to be handled,
plug-ins have to conform themselves to some basic rules.

The Methods that HAVE to be implemented in every plug-ins:

def configurationNeed():
 This function is used for the configuration manager so it knows what configuration
 should be sent to the plug-in.
            
def configurationProvision(utilityConfig=[]):
 This function is used for the configuration manager to provide plug-in configuration based
 on the informations given by the configurationNeed function.

def identifyPluginType():
 This function is used so the framework can know which plug-in type it's dealing with. Function
 call on a plug-in and framework behaviour against that plug-in directly depends on the value
 returned by this function. The returned value, even if plug-in returns only 1 value, should be
 inserted into a list. Therefore, plug-ins can have multiple "types".
 #TODO: Those comments HAVE to be kept up to date!!!

 Current plug-in types are:
  "searcher"
    This type of plug-in is called using the pluginSearch method.
    This method should return HTML formatted string so it can be sent
    directly to the Report Manager. These plug-ins will be shown as 
    check-box in a list so user can decide if she wishes to use the plug-in
    for search purposes.
  "analyser"
    This type of plug-in is called using the pluginAnalyse method.
    The method should result in analysis results being returned as an HTML
    string so it can be sent to Report Manager. 
    This type of plug-in will be shown to users using check-boxes, just like searchers.
    When a user clicks on the button, pluginAnalyse method is called.
    IMPORTANT NOTE: Main difference between searchers and analysers is that,
    searchers will only get selected features (after features tuning) while
    analysers gets the full original features list.
  "extractor"
    This type of plug-in is called using the pluginExtract method.
    This type of plug-in should be used in order to extract features
    from a data source. For example, an IdaPro feature extractor 
    would use the IdaPro Input source to extract features from
    an Ida pro data source. The decision to put extractor in plug-in
    rather than in Input source was motivated by the possibilities
    that a single input source could be used in many ways by different 
    extractor plug-ins. Given this, it's up to the user to build
    specialized extractor that will fit his need while still using
    generic data sources. This type of plug-in will be shown to users
    using a radio button form so users can select only one extractor for each task.
    IMPORTANT FOR EXTRACTORS:
    Extractors are a special kind of plug-in. They usually have to 
    be configured from a UI in order to be useful. Given this,
    extractors MUST IMPLEMENT method getUI(). This method returns 
    a string containing related extractor UI class name. This 
    class module should be inside Graphic directory so it is 
    managed by the UI Manager. Extractor specific flow control
    should be done INSIDE THE UI PART. When the work is done,
    UI should call startTuningUI inside the Control manager. At
    that point, extractor job is over, control will be passed
    to the search and analyse logic.
    
def identifyPlugin():
 This function is used so the framework can identify a plug-in using its name.
 Note that this functions returns 2 versions of the same name inside a list
 ["PluginName", "Plugin Display Name"]
 First item in the list should be an exact match for the plug-in main class name.
 Second item is a name used by UI components in order to be able to identify
 plug-ins.
 For example, if a call to this method on a plug-in returns:
 ["FirstSearch", "First Searcher"]
 Plug-in class name is FirstSearch and this plug-in will be identified by a
 "First Searcher" check-box in the UI.
 
'''

import imp
import sys
import os

PLUGIN_MANAGER_PLUGIN_PATH = os.path.dirname(os.path.realpath(__file__)) + "/Plugin/"

#-----------------------------------------------------------------------
# Configuration agent
# The two next function are needed so the configuration manager
# can provide configuration for this module.
# configurationNeed is called first. If no config for this 
# module exists, the user is prompted for module configuration. If
# configuration exists, previous configs will be used. In all cases,
# configuration step is ended when configurationProvision
# is called with a configuration list as arg.
#-----------------------------------------------------------------------
def configurationNeed():
    return None #Current module does not need configuration
            
def configurationProvision(moduleConfig=[]):
    pass #Current module does not need configuration


#-----------------------------------------------------------------------
# PluginManager
# This class is intended to act as an interface to access
# user built plug-ins. Most of the framework is built as plug-ins
#-----------------------------------------------------------------------
class PluginManager():

    _plugins = []

    def __init__(self, binSrcrCore):
        self._core = binSrcrCore
        self._plugins = []
        #Loading module configuration
        configurationProvision(self._core._CfMngr.provideConfiguration(configurationNeed()))
        
        for filename in os.listdir(PLUGIN_MANAGER_PLUGIN_PATH):
            #Only .py files will be loaded
            if filename[-3:] != ".py":
                continue
                
            #Loading all utilityModules in utility path, -3 for ".py" file extension
            findResult = imp.find_module(filename[:-3], [PLUGIN_MANAGER_PLUGIN_PATH])
            try:
                mod = imp.load_module(filename[:-3], findResult[0], findResult[1], findResult[2])
                
                if self.pluginIsValid(mod):
                    self._plugins.append(mod)
                    #Loading single utility configuration from configuration manager
                    mod.configurationProvision(self._core._CfMngr.provideConfiguration(mod.configurationNeed()))
            finally:
                findResult[0].close()
    
    #
    # This method is used to prevent divergent plug-ins to be loaded
    # by the framework. Returns True if plug-in is valid, False if not.
    # TODO: This method could be changed so it also checks that needed functions
    #       actually returns the right type of informations...
    #
    def pluginIsValid(self, plug=None):
        isValid = True
        if plug == None:
            return False
        
        # Validate plug-in implements minimum required functions
        if (hasattr(plug, "configurationNeed") and hasattr(plug, "configurationProvision")
            and hasattr(plug, "identifyPlugin") and hasattr(plug, "identifyPluginType")):
            
            # Plug-in has to be of type "searcher", "analyser", "extractor"
            for type in plug.identifyPluginType():
                if type not in ["searcher", "analyser", "extractor"]:
                    isValid = False
                    break
            
            # Identify plug-in method should return an inside name and an UI name
            if len(plug.identifyPlugin()) != 2:
                isValid = False
            else:
                try:
                    # identifyPlugin returned info should only be of type str
                    if not isinstance(plug.identifyPlugin()[0], str) or not isinstance(plug.identifyPlugin()[1], str):
                        isValid = False
                except:
                    isValid = False
                    
            #Extractors have specific needs
            if plug.identifyPluginType() == "extractor":
                #They have to have a UI part
                if not hasattr(plug, "getUI"):
                    isValid = False
        else:
            isValid = False
            
        return isValid
    
    #
    # This method acts as a wrapper for calls to dynamically loaded modules
    # use is like: utMngrInstance.call(string functionName, arg1, ...)
    # note that arg use is optional. If many callable objects have
    # the same name, only the first one will be called.
    # Note: You can use this function to get constructed object
    # of class present in managed modules
    #
    def call(self, name, *args):
        for module in self._plugins:
            if hasattr(module, name):
                attrib = getattr(module, name)
                return attrib(*args)
        return None
    
    #
    # This method acts as a wrapper for calls to dynamically loaded modules
    # use it like: utMngrInstance.callForPlugin(Plugin, string functionName, arg1, ...)
    # note that arg use is optional. 
    # This is the same as call, but it will call directly for a specific plugin.
    # this help prevent name collision problems if those ever occurs.
    #
    def callForPlugin(self, module, name, *args):
        if hasattr(module, name):
            attrib = getattr(module, name)
            return attrib(*args)
        return None

#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    plMngr = PluginManager(None)


   
