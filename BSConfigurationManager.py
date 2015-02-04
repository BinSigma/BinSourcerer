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

import ast
import os

import BSUIManager
import BSReportManager
import BSPluginManager
import BSUtilityManager
import BSControlManager


#Path to config file. Most configuration should be inside binSrcr.config
CONFIG_MANAGER_CONFIG_FILE = os.path.dirname(os.path.realpath(__file__)) + "\\binSrcr.config"


#-----------------------------------------------------------------------
# ConfigurationManager
# This class is intended to be used by the user to manage
# BinSourcerer configuration.
#-----------------------------------------------------------------------
class ConfigurationManager():
    
    _config = {} #All configurations will be inside this dictionary after CM has been loaded 
    _currentProject = ""
    
    def __init__(self, binSrcrCore):
        if CONFIG_MANAGER_CONFIG_FILE == "":
            raise Exception("CONFIG_MANAGER_CONFIG_FILE has to be configured inside BSConfigurationManager.py")
            
        self._core = binSrcrCore
        
        #Reading configuration file into _config
        self.loadConfigFile()
    
    #
    # This method is in charge of loading configuration file
    # content into the self._config dictionary
    #
    def loadConfigFile(self):
        self._config = {}
        try:
            configFile = open(CONFIG_MANAGER_CONFIG_FILE, "r")
            #print "ok"
            for line in configFile: #1 line = 1 config
                brokenLine = line.partition("=")
                if line == brokenLine[0]: #If line is the same after being partitioned, 
                    continue              #there is no configuration on that line, we can pass...
                #print brokenLine[0].lstrip().rstrip()
                self._config[brokenLine[0].lstrip().rstrip()] = ast.literal_eval(brokenLine[2].lstrip().rstrip())
                
            configFile.close()
        except:
            raise Exception("Unable to load configuration from CONFIG_MANAGER_CONFIG_FILE")
        
    #
    # This main objective of this method is to load config from project
    # configuration file and to activate the new running configuration
    # by merging the project configuration with the running configuration
    #
    def loadAndActivateProjectConfigFile(self, projectConfigFile):
        
        if projectConfigFile is None or projectConfigFile == "":
            self.loadConfigFile()
            self.activateConfiguration()
            self.changeCurrentProject(projectConfigFile)
            return
        
        try:
            #Lets get project specific configuration file
            configFile = open(projectConfigFile, "r")
            
            #Set configuration running configuration to project configuration
            for line in configFile: #1 line = 1 config
                brokenLine = line.partition("=")
                self._config[brokenLine[0].lstrip().rstrip()] = ast.literal_eval(brokenLine[2].lstrip().rstrip())
             
            configFile.close()
            
            #Reload running configuration
            self.activateConfiguration()
            
            self.changeCurrentProject(projectConfigFile)
        except:
            raise Exception("Unable to load configuration from project file. Default framework file as been loaded.")
    
    #
    # This Method is key to configuration provision for 
    # user built utilities and plug-ins.
    # It is also used for binSrcr built-in modules configuration. Its input is the list of strings
    # for required config params. The output (Return value) is a list
    # containing all params in the same order as input.
    #
    def provideConfiguration(self, configNeeds=[]):
        if configNeeds == None: #Calling code does not need any configuration
            return None
        
        configList = []
        for singleConfig in configNeeds:
            if singleConfig in self._config:
                configList.append(self._config[singleConfig])
            else: # This can happen when new modules is loaded and user forgot to copy the configuration
                raise Exception(singleConfig + " was requested but could not be found inside configuration file. Please add required configuration to configuration file.")
        return configList

    #
    # This method is used in order to give out the whole
    # config file content if ever asked (ie: UI configurator)
    #
    def getConfigFile(self):
        configList = []
        try:
            configFile = open(CONFIG_MANAGER_CONFIG_FILE, "r")
            for line in configFile:
                configList.append(line)
            configFile.close()
        except:
            raise Exception("Unable to load configuration from CONFIG_MANAGER_CONFIG_FILE")
        
        #We also have to deal with project specific configuration
        if self._currentProject != "":
            projectConfig = []
            
            try:
                configFile = open(CONFIG_MANAGER_CONFIG_FILE, "r")
                for line in configFile:
                    projectConfig.append(line)
                configFile.close()
                
                for pconfig in projectConfig:
                    brokenLine = pconfig.partition("=")
                    pconfigParam = brokenLine[0].lstrip().rstrip()
                    
                    for config in configList:
                        brokenLine = config.partition("=")
                        configParam = brokenLine[0].lstrip().rstrip()
                        
                        #If project is loaded we replace Framework specific
                        #config for project config
                        if configParam == pconfigParam:
                            configList.remove(config)
                            configList.append(pconfig)
            
            except:
                raise Exception("Unable to load configuration from CONFIG_MANAGER_CONFIG_FILE")
        
        config = ""
        for line in configList:
            config += line
        
        return config
     
    #
    # This method is used to overwrite the current config file
    # it also triggers a framework wide reconfiguration
    #
    # Because this can be triggered from many places in the framework,
    # there is a special case when it is triggered from the configuration
    # window. In this case, data coming to the function could contain
    # framework configurations mixed with specific project configuration.
    # This has to be managed in order to avoid chaos (inconsistent config files)...
    #
    def setConfigFile(self, data, reload=True, fromConfigWindow=False):
        
        if fromConfigWindow and self._currentProject != "":
            #we get current framework disk configuration
            frameworkConfig = {}
            configFile = open(CONFIG_MANAGER_CONFIG_FILE, "r")
            for line in configFile:
                brokenLine = line.partition("=")
                frameworkConfig[brokenLine[0].lstrip().rstrip()] = brokenLine[2].lstrip().rstrip()
            configFile.close()
            
            #we get current project disk configuration
            projectConfig = {}
            configFile = open(self._currentProject, "r")
            for line in configFile:
                brokenLine = line.partition("=")
                projectConfig[brokenLine[0].lstrip().rstrip()] = brokenLine[2].lstrip().rstrip()
            configFile.close()
            
            #now we get current running configuration or configuration to be saved
            configToBeSaved = data.split("\n")
            newConfig = {}
            for line in configToBeSaved:
                brokenLine = line.partition("=")
                newConfig[brokenLine[0].lstrip().rstrip()] = brokenLine[2].lstrip().rstrip()
            
            #we parse that new config in order to find out what goes where
            for key in newConfig.keys():
                if key in projectConfig.keys():
                    #In this case the config is for the project
                    projectConfig[key] = newConfig[key]
                else:
                    #In this one, for the whole framework
                    frameworkConfig[key] = newConfig[key]

            #now it's time to rebuild a framework configuration file
            config = ""
            for key in frameworkConfig.keys():
                config += key + " = " + (str(frameworkConfig[key])) + "\n"
            config = config[:-1]
            
            self.setConfigFile(config)
            
            #now it's time to rebuild a project configuration file
            config = ""
            for key in projectConfig.keys():
                config += key + " = " + (str(projectConfig[key])) + "\n"
            config = config[:-1]
            
            #write project configuration and reload
            projectConfigFile = open(self._currentProject, "w")
            projectConfigFile.write(config)
            projectConfigFile.close()
            self.loadAndActivateProjectConfigFile(self._currentProject)
        
        else:
            try:
                configFile = open(CONFIG_MANAGER_CONFIG_FILE, "w")
                configFile.write(data)
                configFile.close()
            except:
                raise Exception("Unable to load configuration from CONFIG_MANAGER_CONFIG_FILE")
        
        if reload:
            try:
                #Reloading configuration for all the framework
                self.loadConfigFile()
                self.activateConfiguration()
                    
            except:
                raise Exception("Error while reloading framework configuration")
        
    #
    # This method is used to overwrite the running config
    # for a single variable
    #
    def setRunningConfigForVariable(self, var, value):
        try:
            if var in self._config:
                self._config[var] = value
                self.activateConfiguration()
        except:
            raise Exception("Error while reloading " + var + " configuration")
    
    #
    # A call to this method will cause a complete framework reconfiguration
    # important changes to managers and managed module architecture have to
    # be reflected in this method.
    #
    def activateConfiguration(self):
        # Reload all managers configuration
        BSUIManager.configurationProvision(self.provideConfiguration(BSUIManager.configurationNeed()))
        BSReportManager.configurationProvision(self.provideConfiguration(BSReportManager.configurationNeed()))
        BSPluginManager.configurationProvision(self.provideConfiguration(BSPluginManager.configurationNeed()))
        BSUtilityManager.configurationProvision(self.provideConfiguration(BSUtilityManager.configurationNeed()))
        BSControlManager.configurationProvision(self.provideConfiguration(BSControlManager.configurationNeed()))
        
        # Reload all managed modules configuration
        for mod in self._core._UIMngr._ui:
            mod.configurationProvision(self.provideConfiguration(mod.configurationNeed()))
        ####for mod in self._core._InMngr._inputSources:
        ####    mod.configurationProvision(self.provideConfiguration(mod.configurationNeed()))
        for mod in self._core._PlMngr._plugins:
            mod.configurationProvision(self.provideConfiguration(mod.configurationNeed()))
        for mod in self._core._UtMngr._utilities:
            mod.configurationProvision(self.provideConfiguration(mod.configurationNeed()))
        
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    cfMngr = ConfigurationManager()


   
