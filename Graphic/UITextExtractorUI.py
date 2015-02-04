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
import ast

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
    return None #This ui does not need configuration
            
def configurationProvision(uiConfig=[]):
    pass #This ui does not need configuration

       
#-----------------------------------------------------------------------
# TextExtractorUI 
# This class is a helper for TextExtractor. It aims at displaying 
# data for the text extractor.
#-----------------------------------------------------------------------
class TextExtractorUI(QDialog): 
    
    _searchersAnalysersList = []
    _functionList = []
    
    def __init__(self, uiMngr, parent=None):
        self._manager = uiMngr
        super(TextExtractorUI, self).__init__(parent)
        self.setWindowTitle("BinSourcerer - Extracted Features File")
        self.setWindowFlags( Qt.WindowMinimizeButtonHint);
        self.setFixedSize(600, 400)
        
        #File selection zone
        fileInputBox = QGroupBox("Select File")
        self._fileSelect = QLineEdit()
        loadButton = QPushButton("Open")
        loadButton.clicked.connect(self.loadFile)
        filterLabel = QLabel("Filter")
	pathLabel = QLabel("File Path")
        self._filterText = QLineEdit()
        self._filterText.textChanged.connect(self.keypressed)
        clearFilterButton = QPushButton("Clear")
        clearFilterButton.clicked.connect(self.clearFilter)
        topGridLayout = QGridLayout()
	topGridLayout.addWidget(pathLabel, 0, 0, 1, 1)
	topGridLayout.addWidget(loadButton, 0, 7, 1, 1)
        topGridLayout.addWidget(self._fileSelect, 0, 1, 1, 6)
        topGridLayout.addWidget(filterLabel, 1, 0, 1, 1)
        topGridLayout.addWidget(self._filterText, 1, 1, 1, 6)
        topGridLayout.addWidget(clearFilterButton, 1, 7, 1, 1)
        fileInputBox.setLayout(topGridLayout)
        
        #Selected file function zone
        functionsBox = QGroupBox("Select Functions")
        middleHBoxLayout = QHBoxLayout()
        self._functionsView = QTableWidget(0, 2)
        self._functionsView.setColumnWidth(0, 170)
        self._functionsView.setColumnWidth(1, 380)
        self._functionsView.setHorizontalHeaderLabels(["Address", "Function Name"])
        middleHBoxLayout.addWidget(self._functionsView)
        functionsBox.setLayout(middleHBoxLayout)

        #User want all functions
        self._allFuncCheckBox = QCheckBox("Select All Functions")
        self._allFuncCheckBox.clicked.connect(self.selectAll)
        extractButton = QPushButton("Start")
        extractButton.clicked.connect(self.getData)
        
        
        topLayout = QHBoxLayout()
        midLayout = QHBoxLayout()
        bottomLayout = QGridLayout()

        topLayout.addWidget(fileInputBox)
        midLayout.addWidget(functionsBox)
        bottomLayout.addWidget(self._allFuncCheckBox, 0, 0, 1, 6)
        bottomLayout.addWidget(extractButton, 0, 7, 1, 1)
        
        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addLayout(midLayout)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)
        ####
    

    #
    # This is triggered when user types into the filter textBox
    # so filter can be applied.
    #
    def keypressed(self):
        self.applyFilter(self._filterText.text())
    
    #
    # Function list is reloaded given the filter
    #
    def applyFilter(self, filter):
        #Remove all lines for filter can be applied
        while (self._functionsView.rowCount() > 0):
            self._functionsView.removeRow(0)
            
        for function in self._functionList:
            if str(filter).upper() not in str(function[1]).upper() and filter != "":
                continue # Current function does not matches the filter
            
            #Will now add row that matches the filter
            row = self._functionsView.rowCount()
            eaString = function[0]
            if eaString[-1] == "L":
                eaString = eaString[0:-1]
            eaItem = QTableWidgetItem(eaString)
            eaItem.setFlags(eaItem.flags() ^ Qt.ItemIsEditable)
            nameItem = QTableWidgetItem(function[1])
            nameItem.setFlags(nameItem.flags() ^ Qt.ItemIsEditable)
            self._functionsView.setRowCount(row + 1)
            self._functionsView.setItem(row,0,eaItem)
            self._functionsView.setItem(row,1,nameItem)
            self._functionsView.setSelectionBehavior(QAbstractItemView.SelectRows)
    
        #If select all is activated, we have to keep everything selected...
        self.selectAll()
    
    def clearFilter(self):
        self._filterText.setText("")
        self.applyFilter("")
    
    #
    # UI method intended to show some interaction when user clicks
    # the "Select All Functions" button.
    #
    def selectAll(self):
        selectOrNot = False
        if self._allFuncCheckBox.isChecked():
            selectOrNot = True
            
        for index in range(0, self._functionsView.rowCount()):
            item = self._functionsView.item(index, 0)
            item.setSelected(selectOrNot)
            item = self._functionsView.item(index, 1)
            item.setSelected(selectOrNot)
        

    
    #
    # This method is used to call the plugin extract method on the
    # extractor. That method will return features for selected functions
    # only.
    #
    def getData(self):
        eaList = self.getSelectedEas()
        
        #Get all features for selected function on specified fileName
        self._extractor = self._manager._core._PlMngr.call("TextExtractor", self._manager._core._PlMngr)
        result = self._extractor.pluginExtract(self._featureList, eaList)
        self.close()
        #Next Step! - Call to self._manager._core._CtMngr.startTuningUI(result)
        #is MANDATORY for every Extractor when work is done!!!
        self._manager._core._CtMngr.startTuningUI(result)
 
    #
    # This simply gets the selected lines in the displayed window
    #
    def getSelectedEas(self):
        eaList = []
        #First, build EAs list for wanted methods
        for index in range(0, self._functionsView.rowCount()):
            item = self._functionsView.item(index, 0)
            
            if self._allFuncCheckBox.isChecked():
                eaList.append(int(item.text(), 16))
            else:
                #If method is selected add to the list
                if item.isSelected():
                    eaList.append(int(item.text(), 16))
        return eaList
 
    #
    # This method is charged with this UI grid population task
    # it finds all functions found in previously built text file
    #
    def loadFile(self):
        #Make sure function list is empty!!
        self._functionList = []
        #User chose file to work on
        fname = QFileDialog.getOpenFileName(None, "Open file", "","Features files (*.xtrak)")
        
        if fname[0] != "":
        
            #Next line is needed in case the user opens more than one file...
            self._functionsView.setRowCount(0)
            
            self._fileName = fname[0]
            self._fileSelect.setText(fname[0])
            
            fileContent = []
            f = open(self._fileName, "r")
            for line in f:
                fileContent.append(ast.literal_eval(line))
            f.close()
            self._featureList = fileContent
            
            # Add a row for all functions in the list
            for function in self._featureList:
                row = self._functionsView.rowCount()
                eaString = str(hex(function[0][1]))
                if eaString[-1] == "L":
                    eaString = eaString[0:-1]
                eaItem = QTableWidgetItem(eaString)
                eaItem.setFlags(eaItem.flags() ^ Qt.ItemIsEditable)
                nameItem = QTableWidgetItem(function[0][0])
                nameItem.setFlags(nameItem.flags() ^ Qt.ItemIsEditable)
                self._functionsView.setRowCount(row + 1)
                self._functionsView.setItem(row,0,eaItem)
                self._functionsView.setItem(row,1,nameItem)
                self._functionsView.setSelectionBehavior(QAbstractItemView.SelectRows)
                #This list will be used to build filtered display
                self._functionList.append((eaString, function[0][0]))
    
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    x = TextExtractorUI(None)


   
