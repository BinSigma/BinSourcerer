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

import os
import imp

UI_MANAGER_GRAPHIC_PATH = os.path.dirname(os.path.realpath(__file__)) + "/Graphic/"

#-----------------------------------------------------------------------
# Configuration agent
# The two next function are needed so the configuration manager will be
# able to provide configuration for this module.
# configurationNeed is called first. If no config for this 
# module exists, user is prompted for module configuration. If
# configuration exists, previous configs will be used. In all cases,
# configuration step is ended when configurationProvision
# is called with a configuration list as arg.
#-----------------------------------------------------------------------
def configurationNeed():
    return None
            
def configurationProvision(moduleConfig=[]):
    pass

#-----------------------------------------------------------------------
# UIManager
# This class is intended to act as a bridge for communication between
# the core and the UI.
#-----------------------------------------------------------------------
class UIManager():

    _ui = []

    def __init__(self, binSrcrCore):
        self._core = binSrcrCore
        self._ui = []
        #Loading module configuration
        configurationProvision(self._core._CfMngr.provideConfiguration(configurationNeed()))
        
        for filename in os.listdir(UI_MANAGER_GRAPHIC_PATH):
            #Only .py files will be loaded
            if filename[-3:] != ".py":
                continue
                
            #Loading all utilityModules in utility path, -3 for ".py" file extension
            findResult = imp.find_module(filename[:-3], [UI_MANAGER_GRAPHIC_PATH])
            try:
                mod = imp.load_module(filename[:-3], findResult[0], findResult[1], findResult[2])
                
                if self.uiIsValid(mod):
                    self._ui.append(mod)
                    #Loading single utility configuration from configuration manager
                    mod.configurationProvision(self._core._CfMngr.provideConfiguration(mod.configurationNeed()))
            finally:
                findResult[0].close()
    
    #
    # This method is used to prevent divergent ui to be loaded
    # by the framework. Returns True if ui is valid, False if not.
    # TODO: This method could be changed so it also checks that needed functions
    #       actually returns the right type of informations...
    #
    def uiIsValid(self, plug=None):
        if plug == None:
            return False
        
        if (hasattr(plug, "configurationNeed") and hasattr(plug, "configurationProvision")):
                return True
        return False
    
    #
    # This method acts as a wrapper for calls to dynamically loaded modules
    # use is like: utMngrInstance.call(string functionName, arg1, ...)
    # note that arg use is optional. If many callable objects have
    # the same name, only the first one will be called.
    # Note: You can use this function to get constructed object
    # of class present in managed modules
    #
    def call(self, name, *args):
        for module in self._ui:
            if hasattr(module, name):
                attrib = getattr(module, name)
                return attrib(*args)
        return None

#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    uiMngr = UIManager()


   
