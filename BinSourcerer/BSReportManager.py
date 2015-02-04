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

REPORT_MANAGER_OUTPUT_REPORT_PATH = ""
REPORT_MANAGER_REPORT_LIST = "Report.log"
#Current report search configuration
UI_SEARCHERS_TUNING_SEPARATOR_CHAR = '***'
CONTROL_MANAGER_REQUEST_DELAY = 4
SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE = False
SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT = 7
SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY = 2.1
SEARCH_FILTER_MINIMUM_STRING_LENGTH = 6
SEARCH_FILTER_MINIMUM_STRING_ENTROPY = 2
SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY = 0.3
SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT = 4
SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT = 1
SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT = 1
SEARCH_FILTER_WORD_DICTIONARY_FILE = ' '
SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD = 33

#-----------------------------------------------------------------------
# Configuration agent
# The two next functions are needed so that the configuration manager can
# provide configuration for this module.
# configurationNeed is called first. If no config for this 
# module exists, user is prompted for module configuration. If
# configuration exists, previous configs will be used. In all cases,
# configuration step is ended when configurationProvision
# is called with a configuration list as arg.
#-----------------------------------------------------------------------
def configurationNeed():
    return ["REPORT_MANAGER_OUTPUT_REPORT_PATH",
			"REPORT_MANAGER_REPORT_LIST",
			"UI_SEARCHERS_TUNING_SEPARATOR_CHAR",
			"CONTROL_MANAGER_REQUEST_DELAY",
			"SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE",
            "SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT",
			"SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY",
			"SEARCH_FILTER_MINIMUM_STRING_LENGTH",
            "SEARCH_FILTER_MINIMUM_STRING_ENTROPY",
			"SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY",
			"SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT",
            "SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT",
			"SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT",
			"SEARCH_FILTER_WORD_DICTIONARY_FILE",
            "SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD"]
            
def configurationProvision(moduleConfig=[]):
    global REPORT_MANAGER_OUTPUT_REPORT_PATH
    global REPORT_MANAGER_REPORT_LIST
    
    global UI_SEARCHERS_TUNING_SEPARATOR_CHAR
    global CONTROL_MANAGER_REQUEST_DELAY
    global SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE
    global SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT
    global SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY
    global SEARCH_FILTER_MINIMUM_STRING_LENGTH
    global SEARCH_FILTER_MINIMUM_STRING_ENTROPY
    global SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY
    global SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT
    global SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT
    global SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT
    global SEARCH_FILTER_WORD_DICTIONARY_FILE
    global SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD
    
    REPORT_MANAGER_OUTPUT_REPORT_PATH = moduleConfig[0]
    REPORT_MANAGER_REPORT_LIST = moduleConfig[1]
    
    UI_SEARCHERS_TUNING_SEPARATOR_CHAR = moduleConfig[2]
    CONTROL_MANAGER_REQUEST_DELAY = moduleConfig[3]
    SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE = moduleConfig[4]
    SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT = moduleConfig[5]
    SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY = moduleConfig[6]
    SEARCH_FILTER_MINIMUM_STRING_LENGTH = moduleConfig[7]
    SEARCH_FILTER_MINIMUM_STRING_ENTROPY = moduleConfig[8]
    SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY = moduleConfig[9]
    SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT = moduleConfig[10]
    SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT = moduleConfig[11]
    SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT = moduleConfig[12]
    SEARCH_FILTER_WORD_DICTIONARY_FILE = moduleConfig[13]
    SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD = moduleConfig[14]


#-----------------------------------------------------------------------
# ReportManager
# This class is intended to act as an interface for report building
# when analysis is over and report is required from the framework
#-----------------------------------------------------------------------
class ReportManager():

    def __init__(self, binSrcrCore):
        self._core = binSrcrCore
        
        #Loading module configuration
        configurationProvision(self._core._CfMngr.provideConfiguration(configurationNeed()))

    #
    # This method is charged with the task of saving a single 
    # search report on disk. The path where the report will be saved
    # is determined by REPORT_MANAGER_OUTPUT_REPORT_PATH configuration
    # specific name for a report is, in fact, md5 sum for report content
    #
    def buildSearchReport(self, results):
        ra = self._core._UtMngr.call("RessourcesAccessor", self._core._UtMngr) #Needed to write report to disk
        htmlString = "<html><head><title>BinSourcerer - Matching Report</title>\n"
        
        #Those meta tags are used by the report viewer so meta info about the report are available
        htmlString += "<meta name=\"UI_SEARCHERS_TUNING_SEPARATOR_CHAR\" content=\"%s\">\n" %(str(UI_SEARCHERS_TUNING_SEPARATOR_CHAR))
        htmlString += "<meta name=\"CONTROL_MANAGER_REQUEST_DELAY\" content=\"%s\">\n" %(str(CONTROL_MANAGER_REQUEST_DELAY))
        htmlString += "<meta name=\"SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE\" content=\"%s\">\n" %(str(SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE))
        htmlString += "<meta name=\"SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT\" content=\"%s\">\n" %(str(SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT))
        htmlString += "<meta name=\"SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY\" content=\"%s\">\n" %(str(SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY))
        htmlString += "<meta name=\"SEARCH_FILTER_MINIMUM_STRING_LENGTH\" content=\"%s\">\n" %(str(SEARCH_FILTER_MINIMUM_STRING_LENGTH))
        htmlString += "<meta name=\"SEARCH_FILTER_MINIMUM_STRING_ENTROPY\" content=\"%s\">\n" %(str(SEARCH_FILTER_MINIMUM_STRING_ENTROPY))
        htmlString += "<meta name=\"SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY\" content=\"%s\">\n" %(str(SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY))
        htmlString += "<meta name=\"SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT\" content=\"%s\">\n" %(str(SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT))
        htmlString += "<meta name=\"SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT\" content=\"%s\">\n" %(str(SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT))
        htmlString += "<meta name=\"SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT\" content=\"%s\">\n" %(str(SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT))
        htmlString += "<meta name=\"SEARCH_FILTER_WORD_DICTIONARY_FILE\" content=\"%s\">\n" %(str(SEARCH_FILTER_WORD_DICTIONARY_FILE))
        htmlString += "<meta name=\"SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD\" content=\"%s\">\n" %(str(SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD))
        
        #Report Body
        htmlString += "</head><body>"
        #Report start
        htmlString += "<h1>BinSourcerer Report</h1><hr />"
        #Core report section (report content)
        for function in results:
            htmlString += "<h2><font color=\"red\">" + function[0] + "</font></h2>"
            for result in function[1]:
                htmlString += result
            htmlString += "<hr />"
        htmlString += "</body></html>"
        
        newReport = ra.ra_saveToRessource(htmlString, REPORT_MANAGER_OUTPUT_REPORT_PATH)
        self.addReportToList(newReport)
        return newReport
    
    #
    # This function returns the current report list content
    #
    def getReportList(self):
        reportList = []
        reportPath = REPORT_MANAGER_OUTPUT_REPORT_PATH + REPORT_MANAGER_REPORT_LIST
        if os.path.isfile(reportPath):
            file = open(reportPath, "r+")
            for reportFile in file:
                reportList.append(reportFile[:-1])
            file.close()
        return reportList
    
    #
    # This function save a new report list overwriting the old one
    #
    def saveReportList(self, newList):
        reportPath = REPORT_MANAGER_OUTPUT_REPORT_PATH + REPORT_MANAGER_REPORT_LIST
        file = open(reportPath, "w")
        for report in newList:
            file.write(report + "\n")
        file.close()
    
    #
    # This function adds the report path to the report list file
    # this file simply contain a list of all report so they can
    # be loaded by the UI
    #
    def addReportToList(self, newReport):
        reportPath = REPORT_MANAGER_OUTPUT_REPORT_PATH + REPORT_MANAGER_REPORT_LIST
        try:
            file = open(reportPath, "r")
            content = file.readlines()
            file.close()
        except:
            content = []
        if not newReport + "\n" in content:
            file = open(reportPath, "a+")
            file.write(newReport + "\n")
            file.close()
    
    #
    # This function will delete a single report from the list
    # it will also delete the report html file. When all done, 
    # new list is saved back to disk
    #
    def deleteReport(self, reportToDelete):
        try:
            os.remove(reportToDelete)
        except:
            Exception("Error while removing report file")
            
        reportList = self.getReportList()
        
        if reportToDelete in reportList:
            reportList.remove(reportToDelete)
        
        self.saveReportList(reportList)
        
        
     
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    rpMngr = ReportManager()


   
