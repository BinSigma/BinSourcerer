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

SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE = False
SEARCH_FILTER_FAST_SEARCH_ENABLE = False
UI_DEFAULT_EXTRACTOR_CHOICE = "Features File"

FAST_MODE = None
DECIMAL_TRANSLATION = None

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
def configurationNeed():
    return ["SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE", "SEARCH_FILTER_FAST_SEARCH_ENABLE"]
            
def configurationProvision(uiConfig=[]):
    global SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE
    global SEARCH_FILTER_FAST_SEARCH_ENABLE
    global UI_DEFAULT_EXTRACTOR_CHOICE
    
    SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE = uiConfig[0]
    SEARCH_FILTER_FAST_SEARCH_ENABLE = uiConfig[1]
    
    #Loading default "fast configuration"
    if FAST_MODE is not None and DECIMAL_TRANSLATION is not None:
        if SEARCH_FILTER_FAST_SEARCH_ENABLE:
            FAST_MODE.setChecked(True)
        else:
            FAST_MODE.setChecked(False)
        if SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE:
            DECIMAL_TRANSLATION.setChecked(True)
        else:
            DECIMAL_TRANSLATION.setChecked(False)

       
#-----------------------------------------------------------------------
# MainWindow
# This class is pyside UI for BinSourcerer main UI window
# This window is used so the user can choose dataSource and
# searchers or analysers to be used for his BinSourcerer session
#-----------------------------------------------------------------------
class MainWindow(QMainWindow ): 
    _configUI = None
    _newProjConfigUI = None
    _reportUI = None
    
    def __init__(self, uiMngr, lastProject, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.setWindowTitle("BinSourcerer")
        self.setWindowFlags( Qt.WindowMinimizeButtonHint);
        self._manager = uiMngr

        global FAST_MODE
        global DECIMAL_TRANSLATION
        
        extractorsList = []
        searchersList = []
        analysersList = []
        
        # Load plugin informations in order to build UI
        for plugin in self._manager._core._PlMngr._plugins:
            if "extractor" in plugin.identifyPluginType():
                extractorsList.append(plugin.identifyPlugin()[1]) #[1] corresponds to the plugin UI Name
            elif "searcher" in plugin.identifyPluginType():
                searchersList.append(plugin.identifyPlugin()[1]) #[1] corresponds to the plugin UI Name
            elif "analyser" in plugin.identifyPluginType():
                analysersList.append(plugin.identifyPlugin()[1]) #[1] corresponds to the plugin UI Name

        # Data extractor zone
        self.radioBoxExtractor = QGroupBox("Data Extractor")
        radioBoxVBoxLayout = QVBoxLayout()
        radioBoxVBoxLayout.setAlignment(Qt.AlignTop)
        for extractor in extractorsList:
            rdiobtn = QRadioButton(extractor)
            radioBoxVBoxLayout.addWidget(rdiobtn)
            if extractor == UI_DEFAULT_EXTRACTOR_CHOICE:
                rdiobtn.setChecked(True)
        self.radioBoxExtractor.setLayout(radioBoxVBoxLayout)
        
        # Searchers Zone
        self.radioBoxSearchers = None
        if len(searchersList) > 0:
            self.radioBoxSearchers = QGroupBox("Code Repositories")
            ckBoxVBoxLayout = QVBoxLayout()
            ckBoxVBoxLayout.setAlignment(Qt.AlignTop)
            for searcher in searchersList:
                rdiobtn = QCheckBox(searcher)
                ckBoxVBoxLayout.addWidget(rdiobtn)
            self.radioBoxSearchers.setLayout(ckBoxVBoxLayout)
        
        # Analysers Zone
        self.radioBoxAnalysers = None
        if len(analysersList) > 0:
            self.radioBoxAnalysers = QGroupBox("Analyzer")
            ckBoxVBoxLayout = QVBoxLayout()
            ckBoxVBoxLayout.setAlignment(Qt.AlignTop)
            for searcher in analysersList:
                rdiobtn = QCheckBox(searcher)
                ckBoxVBoxLayout.addWidget(rdiobtn)
            self.radioBoxAnalysers.setLayout(ckBoxVBoxLayout)
        
        # Top zone layout
        choiceSelectLayout = QHBoxLayout()
        choiceSelectLayout.addWidget(self.radioBoxExtractor)
        
        #Only display searcher/analysers GroupBox if they are not empty
        if self.radioBoxSearchers is not None:
            choiceSelectLayout.addWidget(self.radioBoxSearchers)
        if self.radioBoxAnalysers is not None:
            choiceSelectLayout.addWidget(self.radioBoxAnalysers)
            
        # Quick config layout 
        qConfigSelectLayout = QVBoxLayout()
        self._fastMode = QCheckBox("Fast Mode")
        self._fastMode.clicked.connect(self.activateFastMode)
        self._hexToDeci = QCheckBox("Search for Decimal Representation of Constants")
        self._hexToDeci.clicked.connect(self.activateHexToDeci)
        
        if SEARCH_FILTER_FAST_SEARCH_ENABLE:
            self._fastMode.setChecked(True)
        
        if SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE:
            self._hexToDeci.setChecked(True)
            
        FAST_MODE = self._fastMode
        DECIMAL_TRANSLATION = self._hexToDeci
        
        qConfigSelectLayout.addWidget(self._fastMode)
        qConfigSelectLayout.addWidget(self._hexToDeci)
        
        # Bottom zone layout
        optionsLayout = QHBoxLayout()
        configButton = QPushButton("Configure")
        configButton.clicked.connect(self.config)
        startButton = QPushButton("Start")
        startButton.clicked.connect(self.start)
        exitButton = QPushButton("Exit")
        exitButton.clicked.connect(self.exitBinSourcerer)
        optionsLayout.addWidget(startButton)
        optionsLayout.addWidget(configButton)
        optionsLayout.addWidget(exitButton)
        
       
        # Global layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(choiceSelectLayout)
        mainLayout.addLayout(qConfigSelectLayout)
        mainLayout.addLayout(optionsLayout)
        
        windowWidget = QWidget()
        windowWidget.setLayout(mainLayout)
        self.setCentralWidget(windowWidget)
 
    # Simply clode the main window
    def exitBinSourcerer(self):
        self.close()
    
    # Communicate with configuration manager to change config
    def activateFastMode(self):
        if self._fastMode.isChecked():
            self._manager._core._CfMngr.setRunningConfigForVariable("SEARCH_FILTER_FAST_SEARCH_ENABLE", True)
        else:
            self._manager._core._CfMngr.setRunningConfigForVariable("SEARCH_FILTER_FAST_SEARCH_ENABLE", False)
        
    # Communicate with configuration manager to change config
    def activateHexToDeci(self):
        if self._hexToDeci.isChecked():
            self._manager._core._CfMngr.setRunningConfigForVariable("SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE", True)
        else:
            self._manager._core._CfMngr.setRunningConfigForVariable("SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE", False)
    
    # Enter configuration window
    def config(self):
        self._configUI = self._manager.call("ConfigurationWindow", self._manager)
        self._configUI.show()
        
    # Enter report browser
    def report(self):
        self._reportUI = self._manager.call("ReportUI", self._manager)
        self._reportUI.show()
    
    # Launch search/analysis
    def start(self):
        extractor = ""
        searchersAnalysersUINameList = []
        pluginList = self._manager._core._PlMngr._plugins
        
        # Lets get the choosen extractor
        for item in self.radioBoxExtractor.children():
            if item.__class__.__name__ == "QRadioButton":
                if item.isChecked():
                    extractor = item.text()
                    
        # and then get the Searchers/Analysers list
        for item in self.radioBoxSearchers.children():
            if item.__class__.__name__ == "QCheckBox":
                if item.isChecked():
                    searchersAnalysersUINameList.append(item.text())
        for item in self.radioBoxAnalysers.children():
            if item.__class__.__name__ == "QCheckBox":
                if item.isChecked():
                    searchersAnalysersUINameList.append(item.text())
        
        searchersAnalysersList = []
        for plugin in pluginList:
            if plugin.identifyPlugin()[1] in searchersAnalysersUINameList: 
                searchersAnalysersList.append(plugin.identifyPlugin()[0]) #[0] is the Internal Plugin name, it's used to call the plugin
            elif plugin.identifyPlugin()[1] == extractor:
                extractor = plugin.identifyPlugin()[0]
        #Launches the right extractor UI
        self._manager._core._CtMngr.startExtractorUI(extractor, searchersAnalysersList)

#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":
    x = MainWindow(None)


   
