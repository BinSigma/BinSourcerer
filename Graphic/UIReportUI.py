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

##UI_REPORT_FILES_PATHS = []
##REPORT_MANAGER_OUTPUT_REPORT_PATH = ""

#This is for display purpose only, the following dict is not to be managed 
#by the configuration manager.
configToDisplay = {"SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD":"Black List Threshold",
                    "UI_SEARCHERS_TUNING_SEPARATOR_CHAR":"Search Separation Character",
                    "SEARCH_FILTER_WORD_DICTIONARY_FILE":"Black List File",
                    "SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE":"Decimal Representation of Constants",
                    "SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT":"Minimum Function Count",
                    "SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT":"Minimum Constant Digit",
                    "SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT":"Minimum Constant Count",
                    "SEARCH_FILTER_MINIMUM_STRING_ENTROPY":"Minimum String Entropy",
                    "CONTROL_MANAGER_REQUEST_DELAY":"Search Request Delay",
                    "SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY":"Minimum Import Entropy",
                    "SEARCH_FILTER_MINIMUM_STRING_LENGTH":"Minimum String Length",
                    "SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT":"Minimum String Count",
                    "SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY":"Minimum Constant Entropy"}

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
    return ["UI_REPORT_FILES_PATHS", "REPORT_MANAGER_OUTPUT_REPORT_PATH"]
            
def configurationProvision(uiConfig=[]):
    global UI_REPORT_FILES_PATHS
    global REPORT_MANAGER_OUTPUT_REPORT_PATH
    UI_REPORT_FILES_PATHS = uiConfig[0]
    REPORT_MANAGER_OUTPUT_REPORT_PATH = uiConfig[1]

       
#-----------------------------------------------------------------------
# ReportUI
# This class objective is to show the end report to the user
#-----------------------------------------------------------------------
class ReportUI(QDialog):

    _currentLoadedFile = []
    
    def __init__(self, uiMngr, parent=None):
        super(ReportUI, self).__init__(parent)
        self.setWindowTitle("BinSourcerer - Report Viewer")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint);
        self._manager = uiMngr

        self.setGeometry(50, 50, 800, 600)
        
        # Text zone containing report path
        fileBox = QGroupBox("Report")
        topHBoxLayout = QHBoxLayout()
        self._file = QLineEdit("Loading...")
        topHBoxLayout.addWidget(self._file)
        fileBox.setLayout(topHBoxLayout)
        
        # Text zone showing report content
        reportOutputBox = QGroupBox("")
        middleHBoxLayout = QHBoxLayout()
        self._reportView = QTextBrowser()
        self._reportView.setOpenLinks(False)
        self._reportView.anchorClicked.connect(self.link)
        self._reportView.viewport().installEventFilter(self)
        #connect(self._reportView,SIGNAL(anchorClicked(QUrl)),this,SLOT(onAnchorClicked(QUrl)));

        # Report Viewer
        middleHBoxLayout.addWidget(self._reportView)
        reportOutputBox.setLayout(middleHBoxLayout)
        
        # Close button
        closeButton = QPushButton("Close")
        closeButton.clicked.connect(self.close)
        
        # Full list of reports
        self._reportList = QListWidget()
        self._reportList.itemClicked.connect(self.changeItemSelection)
        
        #Delete report button
        deleteButton = QPushButton("Delete Report")
        deleteButton.clicked.connect(self.deleteReport)
        
        #Link preview
        self._linkPreview = QLabel()
        self._linkPreview.setStyleSheet("font: 8pt;");
        
        #Info grid
        self._configView = QTableWidget(0, 2)
        self._configView.setColumnWidth(0, 120)
        self._configView.setColumnWidth(1, 130)
        self._configView.setHorizontalHeaderLabels(["Configuration", "Value"])
        self._configView.verticalHeader().setVisible(False)
        
        #Get everything together and display it!
        contentLayout = QGridLayout()
        contentLayout.addWidget(fileBox, 0, 0, 1, 6)
        contentLayout.addWidget(reportOutputBox, 1, 0, 20, 6)
        contentLayout.addWidget(self._reportList, 0, 7, 15, 2)
        contentLayout.addWidget(self._configView, 15, 7, 6, 2)
        contentLayout.addWidget(self._linkPreview, 21, 0, 2, 6)
        contentLayout.addWidget(deleteButton, 21, 7, 1, 1)
        contentLayout.addWidget(closeButton, 21, 8, 1, 1)
        
        self.setLayout(contentLayout)
        self.reloadReportList()
    
    # 
    # This is intended to filter mouse event in order to display
    # links url when in mouse over situations. After some search
    # on the internet, there did not seems to have any fast track
    # solution to this need so I build this method. Feel free to change
    # if you have any better solution.
    #
    # Downside to this "quick hack" is that if we ever have more than
    # one link on a line in reports, chances are that this will be broken...
    #
    def eventFilter(self,target,event):     
        if(event.type()==QEvent.MouseMove):
        
            #Lets get the link information
            tc = self._reportView.cursorForPosition(event.pos())
            tc.select(QTextCursor.WordUnderCursor)
            content = tc.selection().toHtml()
            
            #Now we parse in order to find the URL
            newLink = ""
            if "<a href=\"" in content:
                brokenString = content.split("<a href=\"")
                brokenString = brokenString[1].split("\"")
                linkPath = brokenString[0]
                
                goodLine = ""
                for line in self._currentLoadedFile:
                    if linkPath in line:
                        goodLine = line
                        break
                
                
                while len(linkPath) > 100:
                    newLink += linkPath[0:100] + "\n"
                    linkPath = linkPath[100:]
                    
                if len(linkPath) <= 100:
                    #After this line newLink contains the full URL
                    #with \n in order to be displayed in a proper way
                    newLink += linkPath
                
            #If the user is sitting on a link    
            if self._reportView.viewport().cursor().shape() == Qt.PointingHandCursor:
                self._linkPreview.setText("Link: " + newLink)
            else:
                self._linkPreview.setText("")
        
        return False
        '''
        print "eventFilter "+str(event.type())
        if(event.type()==QEvent.MouseButtonPress):
            print "Mouse was presssed "+str(event.type())
            self.mousePressEvent(event) 
            return True
        return False 
        '''
    
    #
    # This is activated when the user clicks on a new report so it can be loaded
    #
    def changeItemSelection(self, widgetItem):
    
        if widgetItem is not None:
        
            #Empty config details view if we dont do this
            #the list will grow with each item selection
            while (self._configView.rowCount() > 0):
                self._configView.removeRow(0)
        
            #Open file and display content
            fileName = REPORT_MANAGER_OUTPUT_REPORT_PATH + widgetItem.text()
            self._file.setText(fileName)
            file = open(fileName, "r")
            fileContent = ""
            
            reportConfig = {}
            
            #Get file meta tags
            for line in file:
                if "<meta name=" in line:
                    splitedLine = line.split("\"")
                    reportConfig[splitedLine[1]] = splitedLine[3]
                fileContent += line
                self._currentLoadedFile.append(line)
            file.close()
            self._reportView.setText(fileContent)
            
            #If current report have meta tags populate config view zone
            if reportConfig != {}:
                for config in reportConfig:
                    row = self._configView.rowCount()
                    configItem = QTableWidgetItem(configToDisplay[config])
                    configItem.setToolTip(configToDisplay[config])
                    configItem.setFlags(configItem.flags() ^ Qt.ItemIsEditable)
                    valueItem = QTableWidgetItem(reportConfig[config])
                    valueItem.setToolTip(reportConfig[config])
                    valueItem.setFlags(valueItem.flags() ^ Qt.ItemIsEditable)
                    self._configView.setRowCount(row + 1)
                    self._configView.setItem(row,0,configItem)
                    self._configView.setItem(row,1,valueItem)
                    self._configView.setSelectionBehavior(QAbstractItemView.SelectRows)
           
    #
    # This is activated when the user clicks on a link
    #
    def link(self, clickedLink):
        result = QDesktopServices.openUrl(clickedLink)
        if not result:
            for path in UI_REPORT_FILES_PATHS:
                linkText = str(clickedLink.toString())
                if not path.upper() in linkText.upper():
                    linkText = "file:///" + path + linkText
                else:
                    linkText = "file:///" + linkText
                result = QDesktopServices.openUrl(QUrl(linkText))

                if result:
                    break
    #
    # This is activated when the report list needs to be reloaded
    # normally, at initial ReportUi load or when report is added or
    # removed from the report list.
    # fileName parameter let the user select the "UI Selected" report 
    #
    def reloadReportList(self, fileName=None):
        while (self._reportList.count() > 0):
            self._reportList.takeItem(0)
    
        reports = self._manager._core._RpMngr.getReportList()
        
        for rep in reports:
            item = QListWidgetItem(rep.split("\\")[-1])
            self._reportList.addItem(item)
            if rep == fileName:
                item.setSelected(True)
                self.changeItemSelection(item)
        
        if fileName == None:
            self._reportList.setCurrentRow(0)
            self.changeItemSelection(self._reportList.currentItem())
        
        
    #
    # This is activated when the user clicks on the "delete report" button
    # you have to be careful, even if the report will be removed from the
    # list and the report file removed from the disk. Downloaded single results
    # linked inside the report file will NOT be deleted. Given this, if the
    # report folder is not cleaned from time to time, it can (and will) grow
    # to a quite impressive size...
    #
    def deleteReport(self):
        if self._reportList.currentItem() is not None:
        
            reply = QMessageBox.question(self, "Delete", "Are you sure you want to delete this report?\nYou will not be able to recover it later.", QMessageBox.Yes | QMessageBox.No)
        
            if reply == QMessageBox.Yes:
                selectedItemText = REPORT_MANAGER_OUTPUT_REPORT_PATH + str(self._reportList.currentItem().text())
                if selectedItemText:
                    self._manager._core._RpMngr.deleteReport(selectedItemText)
                    self.reloadReportList()
        
        
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    app = QApplication([])   
    x = ReportUI(None)
    x.show()
    app.exec_()

   
