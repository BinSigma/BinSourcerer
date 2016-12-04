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
# This Python script is the core script for BinSourcerer, a framework
# for assembly to source code matching
#
# Status: Debug
#
########################################################################

import BSUIManager
####import BSInputManager
import BSReportManager
import BSPluginManager
import BSUtilityManager
import BSConfigurationManager
import BSControlManager

#Needed because qtapp is launched from main
from PySide.QtCore import *
from PySide.QtGui import *
###

import sys #For command line args

#-----------------------------------------------------------------------
# BinSourcererCore
# This class is the main BinSourcerer Class. Communication between 
# more specialized Class are made through this core class
#-----------------------------------------------------------------------
class BinSourcererCore():

    def __init__(self, launchedFrom):
        #Config manager has to be first! Other depends on it.
        self._CfMngr = BSConfigurationManager.ConfigurationManager(self)
        
        self._UIMngr = BSUIManager.UIManager(self)
        ####self._InMngr = BSInputManager.InputManager(self)
        self._RpMngr = BSReportManager.ReportManager(self)
        self._PlMngr = BSPluginManager.PluginManager(self)
        self._UtMngr = BSUtilityManager.UtilityManager(self)
        self._CtMngr = BSControlManager.ControlManager(self)
        
        self._CfMngr.loadConfigFile()
        self._CfMngr.activateConfiguration()
   
        self._launched = launchedFrom
        
    #
    # This method is the framework main start point
    #
    def startBinSourcerer(self):

        #If a project was previously opened, it is re-opened
        ####lastProject = self._CfMngr.provideConfiguration(["LAST_PROJECT"])[0]
        ####try:
        ####    self._CfMngr.loadAndActivateProjectConfigFile(lastProject)
        ####except:
        ####    self._CfMngr.loadConfigFile()
        ####    self._CfMngr.activateConfiguration()
    
        #Lets start BinSourcerer!
        self.app = QApplication.instance()
        self._mainWindow = self._UIMngr.call("MainWindow", self._UIMngr, '')
        self._mainWindow.show()
        self.app.exec_()
        #After this point, after all actions, UIs will refer back to 
        #control manager, not to main. Control manager main objective
        #is to keep main as small and simple as possible.
        
#-----------------------------------------------------------------------
# __main__
# BinSourcerer begins here
#-----------------------------------------------------------------------
if __name__ == "__main__":
    
    #Used when called from within IDA Pro using the right script
    launched = None
    if len(sys.argv) > 1:
        launched = sys.argv[1]

    binSrcer = BinSourcererCore(launched)
    print("BinSourcererCore init status: Done")
    print("BinSourcerer is ready for magic...")
    binSrcer.startBinSourcerer()
	


   
