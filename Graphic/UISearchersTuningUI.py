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


UI_SEARCHERS_TUNING_SEPARATOR_CHAR = "-" # This char is used to separate search terms in the UI

#Those two params are not available inside the configuration file.
USELECTED_CELL_BACK_COLOR = QColor(250, 250, 250, 255)
USELECTED_CELL_FRONT_COLOR = QColor(170, 170, 170, 170)

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
    return ["UI_SEARCHERS_TUNING_SEPARATOR_CHAR"]
            
def configurationProvision(uiConfig=[]):
    global UI_SEARCHERS_TUNING_SEPARATOR_CHAR
    UI_SEARCHERS_TUNING_SEPARATOR_CHAR = uiConfig[0]

       
#-----------------------------------------------------------------------
# SearchersTuningUI 
# This class is used to let user fine tune his search queries
#-----------------------------------------------------------------------
class SearchersTuningUI(QDialog): 
    
    _searchersAnalysersList = []
    _originalFunctionsList = []
    _userNameList = []
    _userConstantList = []
    _userStringList = []
    _userImportList = []
    
    def __init__(self, uiMngr, parent=None):
        self._manager = uiMngr
        super(SearchersTuningUI, self).__init__(parent)
        self.setWindowTitle("Select Features")
        self.setWindowFlags( Qt.WindowMinimizeButtonHint);
        
        self.setGeometry(100, 100, 1000, 600)
        
        #
        # Set the "top zone"
        #
        bulkBox = QGroupBox("Add/Remove")
        topHBoxLayout = QGridLayout()
        self._names = QCheckBox("Name")
        self._names.setChecked(True)
        self._names.clicked.connect(self.namesSelect)
        self._constants = QCheckBox("Constants")
        self._constants.setChecked(True)
        self._constants.clicked.connect(self.constantsSelect)
        self._strings = QCheckBox("Strings")
        self._strings.setChecked(True)
        self._strings.clicked.connect(self.stringsSelect)
        self._imports = QCheckBox("Imported Functions")
        self._imports.setChecked(True)
        self._imports.clicked.connect(self.importsSelect)
        reset = QPushButton("Reset")
        reset.clicked.connect(self.reset)
        topHBoxLayout.addWidget(self._names, 0, 0, 1, 1)
        topHBoxLayout.addWidget(self._constants, 0, 1, 1, 1)
        topHBoxLayout.addWidget(self._strings, 0, 2, 1, 1)
        topHBoxLayout.addWidget(self._imports, 0, 3, 1, 3)
        topHBoxLayout.addWidget(reset, 0, 7, 1, 1)
        bulkBox.setLayout(topHBoxLayout)
        
        #
        # Features modification zone
        #
        functionsBox = QGroupBox("Features Selection")
        midHBoxLayout = QHBoxLayout()
        self._functionsView = QTableWidget(0, 5)
        self._functionsView.setColumnWidth(0, 170)
        self._functionsView.setColumnWidth(1, 170)
        self._functionsView.setColumnWidth(2, 170)
        self._functionsView.setColumnWidth(3, 170)
        self._functionsView.setColumnWidth(4, 170)
        self._functionsView.setHorizontalHeaderLabels(["Function", "Name", "Constants", "Strings", "Imported Functions"])
        self._functionsView.cellClicked.connect(self.addOrRemoveContent)
        
        midHBoxLayout.addWidget(self._functionsView)
        functionsBox.setLayout(midHBoxLayout)

        # When features are ok, user pushes this button to launch the search
        searchButton = QPushButton("Search")
        searchButton.clicked.connect(self.search)
        
        topLayout = QHBoxLayout()
        midLayout = QHBoxLayout()
        bottomLayout = QGridLayout()

        topLayout.addWidget(bulkBox)
        midLayout.addWidget(functionsBox)
        bottomLayout.addWidget(QWidget(), 0, 0, 1, 6)
        bottomLayout.addWidget(searchButton, 0, 7, 1, 1)
        
        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addLayout(midLayout)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)
        ####
    
    
    #
    # This is activated when the user clicks inside a cell
    #
    def addOrRemoveContent(self, row, column):
        #print("Row %d and Column %d was clicked" % (row, column))
        item = self._functionsView.item(row, column)
        if item.text() != "":
            if item.background().color() == USELECTED_CELL_BACK_COLOR:
                backBrush = QBrush(Qt.white)
                frontBrush = QBrush(Qt.black) 
            else:
                backBrush = QBrush(USELECTED_CELL_BACK_COLOR)
                frontBrush = QBrush(USELECTED_CELL_FRONT_COLOR)

            item.setBackground(backBrush)
            item.setForeground(frontBrush)
        self._functionsView.clearSelection()
        
    
    #
    # This is activated when the user clicks on the "Name" checkbox
    #
    def namesSelect(self):
        for y in range(0, self._functionsView.rowCount()):
            item = self._functionsView.item(y, 1)
            if self._names.isChecked():
                backBrush = QBrush(Qt.white)
                frontBrush = QBrush(Qt.black) 
            else:
                backBrush = QBrush(USELECTED_CELL_BACK_COLOR)
                frontBrush = QBrush(USELECTED_CELL_FRONT_COLOR) 
            item.setBackground(backBrush)
            item.setForeground(frontBrush)
    
    #
    # This is activated when the user clicks on the "Constants" checkbox
    #
    def constantsSelect(self):
        for y in range(0, self._functionsView.rowCount()):
            item = self._functionsView.item(y, 2)
            if self._constants.isChecked():
                backBrush = QBrush(Qt.white)
                frontBrush = QBrush(Qt.black) 
            else:
                backBrush = QBrush(USELECTED_CELL_BACK_COLOR)
                frontBrush = QBrush(USELECTED_CELL_FRONT_COLOR) 
            item.setBackground(backBrush)
            item.setForeground(frontBrush)
    
    #
    # This is activated when the user clicks on the "Strings" checkbox
    #
    def stringsSelect(self):
        for y in range(0, self._functionsView.rowCount()):
            item = self._functionsView.item(y, 3)
            if self._strings.isChecked():
                backBrush = QBrush(Qt.white)
                frontBrush = QBrush(Qt.black) 
            else:
                backBrush = QBrush(USELECTED_CELL_BACK_COLOR)
                frontBrush = QBrush(USELECTED_CELL_FRONT_COLOR) 
            item.setBackground(backBrush)
            item.setForeground(frontBrush)
    #
    # This is activated when the user clicks on the "Imports" checkbox
    #
    def importsSelect(self):
        for y in range(0, self._functionsView.rowCount()):
            item = self._functionsView.item(y, 4)
            if self._imports.isChecked():
                backBrush = QBrush(Qt.white)
                frontBrush = QBrush(Qt.black) 
            else:
                backBrush = QBrush(USELECTED_CELL_BACK_COLOR)
                frontBrush = QBrush(USELECTED_CELL_FRONT_COLOR) 
            item.setBackground(backBrush)
            item.setForeground(frontBrush)
    
    #
    # Set UI and selected informations back to default
    #
    def reset(self):
        while (self._functionsView.rowCount() > 0):
            self._functionsView.removeRow(0);
        self.loadFunctions(self._originalFunctionsList)
        self._names.setChecked(False)
        self._constants.setChecked(True)
        self._strings.setChecked(True)
        self._imports.setChecked(True)
        self.namesSelect()
    

    #
    # This method is used to load UI grid with functions 
    # features. This is called from Control Manager
    #
    def loadFunctions(self, functionsList):
        self._originalFunctionsList = functionsList
        for function in functionsList:
            #In order to facilitate features edition
            #all features are grouped inside the same cell
            #using a single string for each function type
            nText = ""
            cText = ""
            sText = ""
            iText = ""
            for searchTerm in function[1]:
                if searchTerm[0] == "i":
                    if iText == "":
                        iText += searchTerm[1]
                    else:
                        iText += UI_SEARCHERS_TUNING_SEPARATOR_CHAR + searchTerm[1]
                    continue
                elif searchTerm[0] == "s":
                    if sText == "":
                        sText += searchTerm[1]
                    else:
                        sText += UI_SEARCHERS_TUNING_SEPARATOR_CHAR + searchTerm[1]
                    continue
                elif searchTerm[0] == "c":
                    if cText == "":
                        cText += searchTerm[1]
                    else:
                        cText += UI_SEARCHERS_TUNING_SEPARATOR_CHAR + searchTerm[1]
                    continue
                elif searchTerm[0] == "n":
                    try:
                        nText += searchTerm[1]
                        continue
                    except:
                        print searchTerm
                        
            
            #Building new cells with the newly created strings
            funcNameItem = QTableWidgetItem(function[0])
            funcNameItem.setFlags(funcNameItem.flags() ^ Qt.ItemIsEditable)
            funcNItem = QTableWidgetItem(nText)
            #Set all names in red
            backBrush = QBrush(USELECTED_CELL_BACK_COLOR);
            frontBrush = QBrush(USELECTED_CELL_FRONT_COLOR)
            funcNItem.setBackground(backBrush)
            funcNItem.setForeground(frontBrush)
            
            funcCItem = QTableWidgetItem(cText)
            funcSItem = QTableWidgetItem(sText)
            funcIItem = QTableWidgetItem(iText)
            
            #Adding the new cells to the grid
            row = self._functionsView.rowCount()
            self._functionsView.setRowCount(row + 1)
            self._functionsView.setItem(row,0,funcNameItem)
            self._functionsView.setItem(row,1,funcNItem)
            self._functionsView.setItem(row,2,funcCItem)
            self._functionsView.setItem(row,3,funcSItem)
            self._functionsView.setItem(row,4,funcIItem)
            
            
            #Warn the user if his sep char is not suited for current function group
        self.checkSepChar(functionsList)

    #
    # This method is used to check if input function list
    # contains separator character. If so, it suggest the best
    # char to replace the current char.
    #
    def checkSepChar(self, functionsList):
        bestChar = ""
        charNumber = 0
        charSet = {}

        #Build comparison char dictionary 
        for y in range(32, 127):
            charSet[chr(y)] = 0
        
        #Calculate number of chars for each char
        bs = ""
        for function in functionsList:
            for searchTerm in function[1]:
                if searchTerm[0] == "i" or searchTerm[0] == "n" or searchTerm[0] == "s" or searchTerm[0] == "c":
                    bs += searchTerm[1]
        
        #Counting BigString chars
        totalChar = len(bs)
        baseIndex = 0
        sepCharLength = len(UI_SEARCHERS_TUNING_SEPARATOR_CHAR)
        while baseIndex < totalChar - sepCharLength:
            metaChar = bs[baseIndex:baseIndex+sepCharLength]
            if metaChar in charSet:
                charSet[metaChar] += 1
            else:
                charSet[metaChar] = 1
            baseIndex += 1
        
        #Check if current separator char is used 
        if UI_SEARCHERS_TUNING_SEPARATOR_CHAR in charSet and charSet[UI_SEARCHERS_TUNING_SEPARATOR_CHAR] != 0:
            message =  "UI_SEARCHERS_TUNING_SEPARATOR_CHAR is used by search terms\n"

            #if so, try to find the best separator char available
            for item in charSet:
                if bestChar == "":
                    bestChar = item
                    charNumber = charSet[item]
                elif charSet[item] < charNumber:
                    bestChar = item
                    charNumber = charSet[item]

            if charNumber == 0:
                #A perfect separator has been found (not in use at all in search terms)
                message += "But it's your lucky day!\nFor the current functions group, '" + bestChar + "' is a perfect separation character\n"
            else:
                #Not perfect separator char has been found, will show the
                #best available separator char to the user
                message += "No perfect chars where found for the current search\n"
                message += "The best char would be '" + bestChar + "\n"
                message += "Please note that chosing this char would impact on " + str(charNumber) + " search terms\n"
            
            message += "It is strongly advised that you change\n"
            message += "UI_SEARCHERS_TUNING_SEPARATOR_CHAR in configuration settings\n"
            message += "before proceeding with search or analysis.\n"
            
            #Show the waring to Mr. User
            mb = QMessageBox()
            mb.setWindowTitle('Warning!')
            mb.setText(message)
            mb.exec_()
            
    #
    # This method is called when the user clicks on the search button
    # When called, this method will parse the whole grid and rebuild
    # all features for all functions taking user changes into account.
    # if ever there is a risk for separator char to cause some problems,
    # this car can be set in the config file to a new char.
    # This function will call coordinateSearchAndAnalyseActions from
    # Control Manager with the original features list and the newly 
    # built features list. Both list are built like:
    #    [("FunctionName", [("type", "searchterm"), ...]), ...]
    def search(self):
        userFilteredFunctionsList = []
        for y in range(0, self._functionsView.rowCount()):
            #Get function name
            functionName = self._functionsView.item(y, 0).text()
            featuresList = []
            
            #This is needed in case we have some encoding problems
            maleableString = str(repr(self._functionsView.item(y, 3).text()))[2:] #remove front "u'" from the string
            maleableString = maleableString[:-1] #remove back "'" from the string
            
            #Get specific features n, c, s, i
            if self._functionsView.item(y, 1).background().color() != USELECTED_CELL_BACK_COLOR:
                nList = str(self._functionsView.item(y, 1).text()).split(UI_SEARCHERS_TUNING_SEPARATOR_CHAR)
            else:
                nList = []
            if self._functionsView.item(y, 2).background().color() != USELECTED_CELL_BACK_COLOR:
                cList = str(self._functionsView.item(y, 2).text()).split(UI_SEARCHERS_TUNING_SEPARATOR_CHAR)
            else:
                cList = []
            if self._functionsView.item(y, 3).background().color() != USELECTED_CELL_BACK_COLOR:
                sList = maleableString.split(UI_SEARCHERS_TUNING_SEPARATOR_CHAR)
            else:
                sList = []
            if self._functionsView.item(y, 4).background().color() != USELECTED_CELL_BACK_COLOR:
                iList = str(self._functionsView.item(y, 4).text()).split(UI_SEARCHERS_TUNING_SEPARATOR_CHAR)
            else:
                iList = []
            
            #Build features list for current function
            for item in nList:
                if len(item) > 0:
                    featuresList.append(('n', item))
            for item in cList:
                if len(item) > 0:
                    featuresList.append(('c', item))
            for item in sList:
                if len(item) > 0:
                    featuresList.append(('s', item))
            for item in iList:
                if len(item) > 0:
                    featuresList.append(('i', item))
            
            #Add function and related features list to the filtered list
            userFilteredFunctionsList.append((functionName, featuresList))
        
        #This step is over, lets go the the next step! Control is returned to the Control manager
        self.close() 
        self._manager._core._CtMngr.coordinateSearchAndAnalyseActions(self._originalFunctionsList, userFilteredFunctionsList)
          
            
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    x = SearchersTuningUI(None)


   
