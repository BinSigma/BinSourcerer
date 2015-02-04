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

from PySide.QtCore import *
from PySide.QtGui import *

import os

CURR_PATH = os.path.join(os.path.dirname(__file__))
PAR_PATH = os.path.abspath(os.path.join(CURR_PATH, os.pardir))
###REPORT_MANAGER_OUTPUT_REPORT_PATH = PAR_PATH + '\\Offline\\'
#global REPORT_MANAGER_OUTPUT_REPORT_PATH
IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH = PAR_PATH + '\\Features\\'

#-----------------------------------------------------------------------
# Configuration agent
# The two next function are needed so the configuration manager will be
# able to provide configuration for this module.
# configurationNeed is called first. If no config for this 
# ui exists, user is prompted for ui configuration. If
# configuration exists, previous configs will be used. In all cases,
# configuration step is ended when configurationProvision
# is called with a configuration list as arg.
#-----------------------------------------------------------------------
#def configurationNeed():
#    return None #This ui does not need configuration
            
#def configurationProvision(uiConfig=[]):
#    pass #This ui does not need configuration


def configurationNeed():
    return ["REPORT_MANAGER_OUTPUT_REPORT_PATH","UI_REPORT_FILES_PATHS"]
            
def configurationProvision(utilityConfig=[]):
    global REPORT_MANAGER_OUTPUT_REPORT_PATH
    global UI_REPORT_FILES_PATHS
    REPORT_MANAGER_OUTPUT_REPORT_PATH = utilityConfig[0]
    UI_REPORT_FILES_PATHS = utilityConfig[1]
       
#-----------------------------------------------------------------------
# ConfigurationWindow
# This class is a simple interface so the user is able to change
# config file without getting out or restarting BinSourcerer
#-----------------------------------------------------------------------
class ConfigurationWindow(QDialog): 
    
    def __init__(self, uiMngr, parent=None):
        super(ConfigurationWindow, self).__init__(parent)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        ####self.setFixedSize(1000, 800)
        self.setWindowTitle("BinSourcerer - Configuration")
        self._manager = uiMngr
        
        #Tab creation and insertion
        self._tabWid = QTabWidget()
        self._tabSearchFilt = TabSearchFilter(self._manager)
        self._tabWid.addTab(self._tabSearchFilt, "Search")
        self._tabWebFetch = TabWebFetcher(self._manager)
        self._tabWid.addTab(self._tabWebFetch, "Network")
        
        #Bottom control button creation and insertion
        controlLayout = QGridLayout()
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.cancelAndHide)
        ok = QPushButton("Ok")
        ok.clicked.connect(self.okAndApply)
        undo = QPushButton("Reset")
        undo.clicked.connect(self.resetConfig)
        apply = QPushButton("Apply")
        apply.clicked.connect(self.writeConfigFile)
        controlLayout.addWidget(QWidget() , 0, 0, 1, 8)
        controlLayout.addWidget(apply, 0, 11, 1, 1)
        controlLayout.addWidget(undo, 0, 8, 1, 1)
        controlLayout.addWidget(cancel, 0, 10, 1, 1)
        controlLayout.addWidget(ok, 0, 9, 1, 1)
        
        #Creating layout
        layout = QVBoxLayout()
        layout.addWidget(self._tabWid)
        layout.addLayout(controlLayout)
        self.setLayout(layout)
        
        #Getting all managed var list
        #This list actually contains all configuration variables names that
        #are managed by custom tabs present in this window.
        managedVarList = []
        managedVarList.extend(self._tabWebFetch.configurationNeed())
        managedVarList.extend(self._tabSearchFilt.configurationNeed())
        
        #Getting the unmanaged variables list by inferring it from the managed list
        #The unmanaged variables will be shown in the "text" tab
        self._unmanagedVarList = []
        wholeConfig = self._manager._core._CfMngr._config
        for config in wholeConfig:
            if config not in managedVarList:
                self._unmanagedVarList.append(config)
                

    #
    # cancelAndHide
    # Do not save the config, reset display to original config and hide the window
    #
    def cancelAndHide(self):
        self.resetConfig()
        self.close()
    
    #
    # resetConfig
    # Reset display to original config. Warning, original config means 
    # "The config that is in the config file". Nothing more.
    #
    def resetConfig(self):
        self._tabWebFetch.configurationProvision(self._tabWebFetch._manager._core._CfMngr.provideConfiguration(self._tabWebFetch.configurationNeed()))
        self._tabSearchFilt.configurationProvision(self._tabSearchFilt._manager._core._CfMngr.provideConfiguration(self._tabSearchFilt.configurationNeed()))

  
    #
    # This is called when user use the "close" button.
    # Using the close button will cause the currently
    # displayed configuration to be saved and will close the window.
    #
    def okAndApply(self):
        self.writeConfigFile()
        self.close()
  
    #
    # writeConfigFile
    # Get all configuration and saves them into the config file.
    # At the end of this method, configuration is reloaded so it is taken into
    # account.
    #
    def writeConfigFile(self):
        #We start empty
        newConfig = ""
        
   
        #Now general settings
        if len(newConfig) == 0:
			newConfig += "UI_DEFAULT_EXTRACTOR_CHOICE = " + repr(str("Features File"))
        else:
			newConfig += "\n" + "UI_DEFAULT_EXTRACTOR_CHOICE = " + repr(str("Features File"))

        #Now web fetcher settings
        newConfig += "\n" + "WEB_FETCHER_HTTP_USE_PROXY = " + str(self._tabWebFetch._WEB_FETCHER_HTTP_USE_PROXY.isChecked())
        newConfig += "\n" + "WEB_FETCHER_HTTP_PROXY_LIST = "
        proxyList = []
        for item in range(0, self._tabWebFetch._WEB_FETCHER_HTTP_PROXY_LIST.count()):
            proxyList.append(str(self._tabWebFetch._WEB_FETCHER_HTTP_PROXY_LIST.item(item).text()))
        newConfig += str(proxyList)
        newConfig += "\n" + "WEB_FETCHER_HTTP_USER_AGENT = " + repr(str(self._tabWebFetch._WEB_FETCHER_HTTP_USER_AGENT.text()))
        newConfig += "\n" + "WEB_FETCHER_HTTP_ACCEPT = " + repr(str(self._tabWebFetch._WEB_FETCHER_HTTP_ACCEPT.text()))
        newConfig += "\n" + "WEB_FETCHER_HTTP_ACCEPT_LANGUAGE = " + repr(str(self._tabWebFetch._WEB_FETCHER_HTTP_ACCEPT_LANGUAGE.text()))
        newConfig += "\n" + "WEB_FETCHER_HTTP_CONNECTION = " + repr(str(self._tabWebFetch._WEB_FETCHER_HTTP_CONNECTION.text()))
  
        #Now search filter settings
        newConfig += "\n" + "UI_SEARCHERS_TUNING_SEPARATOR_CHAR = " + repr(str(self._tabSearchFilt._UI_SEARCHERS_TUNING_SEPARATOR_CHAR.text()))
        newConfig += "\n" + "CONTROL_MANAGER_REQUEST_DELAY = " + self._tabSearchFilt._CONTROL_MANAGER_REQUEST_DELAY.text()
        newConfig += "\n" + "SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE = " + str(self._tabSearchFilt._SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE.isChecked())
        newConfig += "\n" + "SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT = " + self._tabSearchFilt._SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT.text()
        newConfig += "\n" + "SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY = " + self._tabSearchFilt._SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY.text()
        newConfig += "\n" + "SEARCH_FILTER_MINIMUM_STRING_LENGTH = " + self._tabSearchFilt._SEARCH_FILTER_MINIMUM_STRING_LENGTH.text()
        newConfig += "\n" + "SEARCH_FILTER_MINIMUM_STRING_ENTROPY = " + self._tabSearchFilt._SEARCH_FILTER_MINIMUM_STRING_ENTROPY.text()
        newConfig += "\n" + "SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY = " + self._tabSearchFilt._SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY.text()
        newConfig += "\n" + "SEARCH_FILTER_FAST_SEARCH_ENABLE = " + str(self._tabSearchFilt._SEARCH_FILTER_FAST_SEARCH_ENABLE.isChecked())
        newConfig += "\n" + "SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT = " + self._tabSearchFilt._SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT.text()
        newConfig += "\n" + "SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT = " + self._tabSearchFilt._SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT.text()
        newConfig += "\n" + "SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT = " + self._tabSearchFilt._SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT.text()
        newConfig += "\n" + "SEARCH_FILTER_WORD_DICTIONARY_FILE = " + repr(str(self._tabSearchFilt._SEARCH_FILTER_WORD_DICTIONARY_FILE.text()))
        newConfig += "\n" + "SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD = " + self._tabSearchFilt._SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD.text()
       
    
        #Followed by ida pro settings
        newConfig += "\n" + "IDA_PRO_TEXT_EXTRACTOR_EXTRACTED_FILE = " + repr(str("extractedFeatures.xtrak"))
        newConfig += "\n" + "IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH = " + repr(str(IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH))
        
        #And then Report manager settings.
        newConfig += "\n" + "REPORT_MANAGER_OUTPUT_REPORT_PATH = " + repr(str(self._tabSearchFilt._REPORT_MANAGER_OUTPUT_REPORT_PATH.text()))
	newConfig += "\n" + "REPORT_MANAGER_REPORT_LIST = " + repr(str("Report.log"))
        newConfig += "\n" + "UI_REPORT_FILES_PATHS = "
        reportFilesPaths = []
        
        reportFilesPaths.append(str(self._tabSearchFilt._REPORT_MANAGER_OUTPUT_REPORT_PATH.text()))
        newConfig += str(reportFilesPaths)
        
        #Config is now ready to be saved and activated by the configuration manager.
        self._manager._core._CfMngr.setConfigFile(newConfig, fromConfigWindow=True, reload=False)
        

        
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication([])
    x = ConfigurationWindowNew(None)
    x.show
    app.exec_()

#
# All configurations linked to web access should go inside this tab
#
class TabWebFetcher(QWidget):
    #-----------------------------------------------------------------------
    # Configuration agent
    # The two next function are needed so the configuration manager will be
    # able to provide configuration for this module (This class in the current case).
    # configurationNeed is called first. If
    # configuration exists, previous configs will be used. In all cases,
    # configuration step is ended when configurationProvision
    # is called with a configuration list as arg.
    #-----------------------------------------------------------------------
    def configurationNeed(self):
        return ["WEB_FETCHER_HTTP_USE_PROXY", "WEB_FETCHER_HTTP_PROXY_LIST", "WEB_FETCHER_HTTP_USER_AGENT",
                "WEB_FETCHER_HTTP_ACCEPT", "WEB_FETCHER_HTTP_ACCEPT_LANGUAGE", "WEB_FETCHER_HTTP_CONNECTION"]
            
    def configurationProvision(self, uiConfig=[]):
        
        self._WEB_FETCHER_HTTP_USE_PROXY.setChecked(uiConfig[0])
        self._WEB_FETCHER_HTTP_USER_AGENT.setText(uiConfig[2])
        self._WEB_FETCHER_HTTP_ACCEPT.setText(uiConfig[3])
        self._WEB_FETCHER_HTTP_ACCEPT_LANGUAGE.setText(uiConfig[4])
        self._WEB_FETCHER_HTTP_CONNECTION.setText(uiConfig[5])
        
        while (self._WEB_FETCHER_HTTP_PROXY_LIST.count() > 0):
            self._WEB_FETCHER_HTTP_PROXY_LIST.takeItem(0)
        
        for proxy in uiConfig[1]:
            #Add proxy to proxy list
            item = QListWidgetItem(proxy)
            self._WEB_FETCHER_HTTP_PROXY_LIST.addItem(item)

    
    def __init__(self, uiMngr, parent=None):
        super(TabWebFetcher, self).__init__(parent)
        
        #
        # Build control items
        #
        self._WEB_FETCHER_HTTP_USE_PROXY = QCheckBox("Use Proxy")
        
        userAgentLabel = QLabel("User-Agent")
        self._WEB_FETCHER_HTTP_USER_AGENT = QLineEdit()
        
        httpAcceptLabel = QLabel("HTTP-Accept")
        self._WEB_FETCHER_HTTP_ACCEPT = QLineEdit()
        
        httpAcceptLanguageLabel = QLabel("HTTP-Accept Language")
        self._WEB_FETCHER_HTTP_ACCEPT_LANGUAGE = QLineEdit()
        
        httpConnectionLabel = QLabel("HTTP-Connection")
        self._WEB_FETCHER_HTTP_CONNECTION = QLineEdit()
        
        httpProxyListLabel = QLabel("Proxy List")
        self._WEB_FETCHER_HTTP_PROXY_LIST = QListWidget()
        removeProxyButton = QPushButton("Remove")
        removeProxyButton.clicked.connect(self.removeProxy)
        
        httpNewProxyLabel = QLabel("New Proxy")
        self._NewProxy = QLineEdit()
        addProxyButton = QPushButton("Add")
        addProxyButton.clicked.connect(self.addProxy)
        
        #
        # UI element positioning
        #
        layout = QGridLayout()
        layout.addWidget(userAgentLabel, 0, 0, 1, 1, Qt.AlignTop)
        layout.addWidget(self._WEB_FETCHER_HTTP_USER_AGENT, 0, 1, 1, 6, Qt.AlignTop)
        layout.addWidget(httpAcceptLabel, 1, 0, 1, 1, Qt.AlignTop)
        layout.addWidget(self._WEB_FETCHER_HTTP_ACCEPT, 1, 1, 1, 6, Qt.AlignTop)
        layout.addWidget(httpAcceptLanguageLabel, 2, 0, 1, 1, Qt.AlignTop)
        layout.addWidget(self._WEB_FETCHER_HTTP_ACCEPT_LANGUAGE, 2, 1, 1, 6, Qt.AlignTop)
        layout.addWidget(httpConnectionLabel, 3, 0, 1, 1, Qt.AlignTop)
        layout.addWidget(self._WEB_FETCHER_HTTP_CONNECTION, 3, 1, 1, 6, Qt.AlignTop)
        
        layout.addWidget(httpProxyListLabel, 4, 0, 1, 1, Qt.AlignTop)
        layout.addWidget(self._WEB_FETCHER_HTTP_PROXY_LIST, 4, 1, 1, 6, Qt.AlignTop)
        layout.addWidget(removeProxyButton, 5, 6, 1, 1, Qt.AlignTop)
        layout.addWidget(httpNewProxyLabel, 6, 0, 1, 1, Qt.AlignTop)
        layout.addWidget(self._NewProxy, 6, 1, 1, 6, Qt.AlignTop)
        layout.addWidget(addProxyButton, 7, 6, 1, 1, Qt.AlignTop)
        layout.addWidget(self._WEB_FETCHER_HTTP_USE_PROXY, 8, 0, 1, 1, Qt.AlignTop)
        
        spacer = QWidget()
        layout.addWidget(spacer, 9, 0, 11, 1)
        
        self.setLayout(layout)
        
        #Populate UI with configuration
        self._manager = uiMngr
        self.configurationProvision(self._manager._core._CfMngr.provideConfiguration(self.configurationNeed()))

    
    #Activated when user clicks the remove proxy button
    def removeProxy(self):
        selectedItems = self._WEB_FETCHER_HTTP_PROXY_LIST.selectedItems()
        for item in selectedItems:
            self._WEB_FETCHER_HTTP_PROXY_LIST.takeItem(self._WEB_FETCHER_HTTP_PROXY_LIST.indexFromItem(item).row())
    
    #Activated when user clicks the add proxy button
    def addProxy(self):
        newProxy = str(self._NewProxy.text())
        self._WEB_FETCHER_HTTP_PROXY_LIST.addItem(QListWidgetItem(newProxy))
        self._NewProxy.setText("")

#
# All configuration related to filtering search terms should go in this tab.
#        
class TabSearchFilter(QWidget):

    #-----------------------------------------------------------------------
    # Configuration agent
    # The two next function are needed so the configuration manager will be
    # able to provide configuration for this module (This class in the current case).
    # configurationNeed is called first. If
    # configuration exists, previous configs will be used. In all cases,
    # configuration step is ended when configurationProvision
    # is called with a configuration list as arg.
    #-----------------------------------------------------------------------
    def configurationNeed(self):
        return ["SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT", "SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY", "SEARCH_FILTER_MINIMUM_STRING_LENGTH",
                "SEARCH_FILTER_MINIMUM_STRING_ENTROPY", "SEARCH_FILTER_FAST_SEARCH_ENABLE", "SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT",
                "SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT", "SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT", "SEARCH_FILTER_WORD_DICTIONARY_FILE",
                "SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD", "SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY", "SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE",
                "UI_SEARCHERS_TUNING_SEPARATOR_CHAR", "CONTROL_MANAGER_REQUEST_DELAY", "REPORT_MANAGER_OUTPUT_REPORT_PATH" , "UI_REPORT_FILES_PATHS"]
            
    def configurationProvision(self, uiConfig=[]):
        self._SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT.setText(str(uiConfig[0]))
        self._SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY.setText(str(uiConfig[1]))
        self._SEARCH_FILTER_MINIMUM_STRING_LENGTH.setText(str(uiConfig[2]))
        self._SEARCH_FILTER_MINIMUM_STRING_ENTROPY.setText(str(uiConfig[3]))
        self._SEARCH_FILTER_FAST_SEARCH_ENABLE.setChecked(uiConfig[4])
        self._SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT.setText(str(uiConfig[5]))
        self._SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT.setText(str(uiConfig[6]))
        self._SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT.setText(str(uiConfig[7]))
        self._SEARCH_FILTER_WORD_DICTIONARY_FILE.setText(str(uiConfig[8]))
        self._SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD.setText(str(uiConfig[9]))
        self._SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY.setText(str(uiConfig[10]))
        self._SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE.setChecked(uiConfig[11])
        self._UI_SEARCHERS_TUNING_SEPARATOR_CHAR.setText(str(uiConfig[12]))
        self._CONTROL_MANAGER_REQUEST_DELAY.setText(str(uiConfig[13]))
	self._REPORT_MANAGER_OUTPUT_REPORT_PATH.setText(str(uiConfig[14]))
	self._UI_REPORT_FILES_PATHS.setText(str(uiConfig[15]))

    
    def __init__(self, uiMngr, parent=None):
        super(TabSearchFilter, self).__init__(parent)
        
        #
        # Build control items
        #
        tuningSeparatorChar = QLabel("Separator Character")
        self._UI_SEARCHERS_TUNING_SEPARATOR_CHAR = QLineEdit()
	reportOutputPath = QLabel("Results Folder")
        self._REPORT_MANAGER_OUTPUT_REPORT_PATH = QLineEdit()
        reportOutputButton = QPushButton("Open")
        reportOutputButton.clicked.connect(self.selectReportOutput)
		
        
        requestDelay = QLabel("Request Delay")
        self._CONTROL_MANAGER_REQUEST_DELAY = QLineEdit()
        
        self._SEARCH_FILTER_FAST_SEARCH_ENABLE = QCheckBox("Use Fast Mode by Default")
        
        self._SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE = QCheckBox("Search for Decimal Representation of Constants by Default")
        
        fastMinimumFunction = QLabel("Minimum Function Count")
        self._SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT = QLineEdit()
        
        fastMinimumConstant = QLabel("Minimum Constant Count")
        self._SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT = QLineEdit()
        
        fastMinimumString = QLabel("Minimum String Count")
        self._SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT = QLineEdit()
        
        minimumConstantDigit = QLabel("Minimum Constant Digit")
        self._SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT = QLineEdit()
        
        minimumConstantEntropy = QLabel("Minimum Constant Entropy")
        self._SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY = QLineEdit()
        
        minimumStringLength = QLabel("Minimum String Length")
        self._SEARCH_FILTER_MINIMUM_STRING_LENGTH = QLineEdit()
        
        minimumStringEntropy = QLabel("Minimum String Entropy")
        self._SEARCH_FILTER_MINIMUM_STRING_ENTROPY = QLineEdit()
        
        minimumImportEntropy = QLabel("Minimum Import Entropy")
        self._SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY = QLineEdit()
        
        inDictionaryThreshold = QLabel("Black List Threshold")
        self._SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD = QLineEdit()
        
        dictionnary = QLabel("Black List File")
        self._SEARCH_FILTER_WORD_DICTIONARY_FILE = QLineEdit()
        selectButton = QPushButton("Select File")
        selectButton.clicked.connect(self.selectFile)

        self._REPORT_MANAGER_OUTPUT_REPORT_PATH = QLineEdit() ###
        self._UI_REPORT_FILES_PATHS = QLineEdit() ### 

        
        #
        #Positioning UI elements
        #
        generalBox = QGroupBox("General")
        gLayout = QGridLayout()
        gLayout.addWidget(requestDelay, 0, 0, 1, 1)
        gLayout.addWidget(self._CONTROL_MANAGER_REQUEST_DELAY, 0, 1, 1, 6)
        gLayout.addWidget(tuningSeparatorChar, 1, 0, 1, 1)
        gLayout.addWidget(self._UI_SEARCHERS_TUNING_SEPARATOR_CHAR, 1, 1, 1, 6)
        gLayout.addWidget(reportOutputPath, 2, 0, 1, 1)
        gLayout.addWidget(self._REPORT_MANAGER_OUTPUT_REPORT_PATH, 2, 1, 1, 5)
        gLayout.addWidget(reportOutputButton, 2, 6)
        generalBox.setLayout(gLayout)
         
        filterBox = QGroupBox("Filters")
        gLayout = QGridLayout()
        gLayout.addWidget(self._SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE, 0, 0, 1, 7)
        gLayout.addWidget(minimumConstantDigit, 1, 0, 1, 1)
        gLayout.addWidget(self._SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT, 1, 1, 1, 6)
        gLayout.addWidget(minimumConstantEntropy, 2, 0, 1, 1)
        gLayout.addWidget(self._SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY, 2, 1, 1, 6)
        gLayout.addWidget(minimumStringLength, 3, 0, 1, 1)
        gLayout.addWidget(self._SEARCH_FILTER_MINIMUM_STRING_LENGTH, 3, 1, 1, 6)
        gLayout.addWidget(minimumStringEntropy, 4, 0, 1, 1)
        gLayout.addWidget(self._SEARCH_FILTER_MINIMUM_STRING_ENTROPY, 4, 1, 1, 6)
        gLayout.addWidget(minimumImportEntropy, 5, 0, 1, 1)
        gLayout.addWidget(self._SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY, 5, 1, 1, 6)
        filterBox.setLayout(gLayout)
        
        #Positioning UI elements 
        fastBox = QGroupBox("Fast Mode")
        gLayout = QGridLayout()
        gLayout.addWidget(self._SEARCH_FILTER_FAST_SEARCH_ENABLE, 0, 0, 1, 7)
        gLayout.addWidget(fastMinimumFunction, 1, 0, 1, 1)
        gLayout.addWidget(self._SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT, 1, 1, 1, 6)
        gLayout.addWidget(fastMinimumConstant, 2, 0, 1, 1)
        gLayout.addWidget(self._SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT, 2, 1, 1, 6)
        gLayout.addWidget(fastMinimumString, 3, 0, 1, 1)
        gLayout.addWidget(self._SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT, 3, 1, 1, 6)
        fastBox.setLayout(gLayout)
        
        #Positioning UI elements 
        dictBox = QGroupBox("Black List")
        gLayout = QGridLayout()
        gLayout.addWidget(inDictionaryThreshold, 0, 0, 1, 1)
        gLayout.addWidget(self._SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD, 0, 1, 1, 6)
        gLayout.addWidget(dictionnary, 1, 0, 1, 1)
        gLayout.addWidget(self._SEARCH_FILTER_WORD_DICTIONARY_FILE, 1, 1, 1, 5)
        gLayout.addWidget(selectButton, 1, 6, 1, 1)
        dictBox.setLayout(gLayout)
        
        #Displaying UI
        layout = QVBoxLayout()
        layout.addWidget(generalBox)
        layout.addWidget(filterBox)
        layout.addWidget(fastBox)
        layout.addWidget(dictBox)
        self.setLayout(layout)
        
        #Populate UI with configuration
        self._manager = uiMngr
        self.configurationProvision(self._manager._core._CfMngr.provideConfiguration(self.configurationNeed()))
    
    #Activated when user click the select dictionary file button
    def selectFile(self):
        fname = QFileDialog.getOpenFileName(None, "Open file", "","Text files (*.txt)")
        fname = fname[0].replace("/", "\\")
        if len(fname) > 0:
            self._SEARCH_FILTER_WORD_DICTIONARY_FILE.setText(fname)
        
    #Activated with the select report output button
    def selectReportOutput(self):
        fname = QFileDialog.getExistingDirectory()
        if len(fname) > 0:
            self._REPORT_MANAGER_OUTPUT_REPORT_PATH.setText(fname + "\\")
