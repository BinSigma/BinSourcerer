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

import time

CONTROL_MANAGER_REQUEST_DELAY = 2 # delay in between searches.

#-----------------------------------------------------------------------
# Configuration agent
# The two next function are needed so the configuration manager will be
# able to provide configuration for this module.
# configurationNeed is called first. If no config for this 
# input source exists, user is prompted for input configuration. If
# configuration exists, previous configs will be used. In all cases,
# configuration step is ended when configurationProvision
# is called with a configuration list as arg.
#-----------------------------------------------------------------------
def configurationNeed():
    return ["CONTROL_MANAGER_REQUEST_DELAY"]
            
def configurationProvision(utilityConfig=[]):
    global CONTROL_MANAGER_REQUEST_DELAY
    CONTROL_MANAGER_REQUEST_DELAY = utilityConfig[0]

#-----------------------------------------------------------------------
# ControlManager
# This class is intended to act as program execution control
# flow manager. The "glue" code in inside the Control Manager
#-----------------------------------------------------------------------
class ControlManager():

    _searchersAnalysersList = [] #List is used to ease process flow management

    def __init__(self, binSrcrCore):
        self._core = binSrcrCore
        
    #
    # startExtractorUI(extractorName="", searchersAnalysersList=[])
    # This method simply start the chosen extractor UI. This UI, when
    # over, will call the startTuningUI method.
    # searchersAnalysersList format is ["searcherName", "otherName", ...]
    # extractorName is a string containing the extractor name, nothing more.
    #
    def startExtractorUI(self, extractorName="", searchersAnalysersList=[]):
        #Keep for later when needed to launch searchers/analysers
        self._searchersAnalysersList = searchersAnalysersList
        
        #Launches the right extractor UI
        extractorUI = self._core._PlMngr.call(extractorName, self._core._PlMngr).getUI()
        self._extractorUI = self._core._UIMngr.call(extractorUI, self._core._UIMngr)
        self._extractorUI.show()
        
    #
    # startSearchersTuningUI(functionsList=[])
    # This method will possibly change in the future. This is why 
    # for now, it's only a bridge to startSearchersTuningUI
    #
    def startTuningUI(self, functionsList=[]):
        self.startSearchersTuningUI(functionsList)
        
    #
    # startSearchersTuningUI(functionsList=[])
    # This method simply calls the Searchers Tuning UI. From this UI
    # user can remove specific search terms or add some depending on
    # his needs. **** When user is done in the UI, UI will call 
    # coordinateSearchAndAnalyseActions method. ****
    # functionsList format should be as [("FunctionName", [("type", "searchTerm"), ...]), ...]
    #
    def startSearchersTuningUI(self, functionsList=[]):
        self._searchersTuningUI = self._core._UIMngr.call("SearchersTuningUI", self._core._UIMngr)
        self._searchersTuningUI.loadFunctions(functionsList)
        self._searchersTuningUI._names.setChecked(False) # This line and the next one are used to default
        self._searchersTuningUI.namesSelect()            # function name to not being selected
        self._searchersTuningUI.show()
    
    #
    # This method is in charge of showing the results to user. The report
    # UI is shown at start of method so user is not left in front 
    # of a black screen. This method will call the search actions
    # and analyse action. When search and analysis 
    # are over, this method call the report manager. Report is then built
    # and ReportUI is updated to show results to the user
    #
    # About parameters
    # analyseList is the complete original features list. This is needed by analysers.
    # searchList is the user filtered features list. This is used for
    # on-line and off-line code search jobs.
    # 
    # If needed, code could be written to forward the complete analyseList
    # to searchers from this method... 
	# It is not implemented yet.
    #
    def coordinateSearchAndAnalyseActions(self, analyseList, searchList):
        # Searchers and analyser list is in self._searchersAnalysersList
        # that has been saved inside startExtractorUI function.
        
        #Be nice and show a UI
        self._reportUI = self._core._UIMngr.call("ReportUI", self._core._UIMngr)
        self._reportUI.show()
        
        searchAndAnalyseResult = [] # List of search/analysis results used to build the final report
        
        #Search and analysis coordination
        functionIndex = 0
        totalFunctionCount = len(analyseList)
        
        #Progress bar code will go here so it's displayed to User
        progressBar = self._core._UIMngr.call("IndependentProgressBar", self._core._UIMngr)
        progressBar.showProgressBar("Searching", displayedText="Search in progress. Please wait...", maxValue=totalFunctionCount)
        #End of progress bar code zone
        
        while functionIndex < totalFunctionCount:
            # searchList and analyseList both have all the functions
            # searchList does not have all search terms for all functions
            # while analyseList does.
            currentFunctionResults = []
            currentFunctionResults.extend(self.searchAction(searchList[functionIndex], self._searchersAnalysersList))
            currentFunctionResults.extend(self.analyseAction(analyseList[functionIndex], self._searchersAnalysersList))
            if len(currentFunctionResults) > 0:
                searchAndAnalyseResult.append((analyseList[functionIndex][0], currentFunctionResults))
            functionIndex += 1
            
            #Progress bar code will go here
            progressBar.stepProgressBar()
            
            #check if user has cancelled current task
            if progressBar._cancelled:
                break
            #End of progress bar code zone
        
        progressBar.hideProgressBar()
        
        #Report write
        fileName = self._core._RpMngr.buildSearchReport(searchAndAnalyseResult)
        
        #Load the report so it can be showed inside the report viewer
        try:
            f = open(fileName, "r")
            content = ""
            for line in f:
                content += line
            f.close()
        except:
            Exception("Can't read the report file " + fileName)
        
        # setting report viewer to it show the report we just red
        self._reportUI._file.setText(fileName)
        self._reportUI._reportView.setText(content)
        self._reportUI.reloadReportList(fileName)
        
    
    #
    # This method is called when a search is made
    # searchList should be built as:
    # [(functionName, [("searchTerm", "type") ...]), ...]
    # searchersList should be built as:
    # ["searcher plugin identification", ...]
    # 
    # Returns
    # This method returns a list built like:
    # [HTML_RESULT_STRING, ...]
    #
    def searchAction(self, singleFunction, searchersList):
        
        pluginToBeUsed = []
        
        #First, we get list of all plugins to be used
        for plugin in self._core._PlMngr._plugins:
            pluginType = self._core._PlMngr.callForPlugin(plugin, "identifyPluginType")
            if "searcher" in pluginType:
                if self._core._PlMngr.callForPlugin(plugin, "identifyPlugin")[0] in searchersList:
                    #User asked to use this plugin
                    pluginToBeUsed.append(plugin)
        
        if len(pluginToBeUsed) < 1:
            return []
        
        currentFunctionResults = []
        
        #Apply filtering on search terms if none passes the filter, return
        filter = self._core._UtMngr.call("SearchFilter", self._core._UtMngr)
        filtered = filter.sf_filter(singleFunction[1])
        
        if len(filtered) == 0:
            return ""
            
        isLocalOnly = True    
        for plugin in pluginToBeUsed:
            pluginObject = self._core._PlMngr.call(self._core._PlMngr.callForPlugin(plugin, "identifyPlugin")[0], self._core._PlMngr)
            result = pluginObject.pluginSearch(filtered)
            
            if result:
                currentFunctionResults.append(result)
                
            if pluginObject.isLocal() != True:
                isLocalOnly = False #Some searchers are not local only

        #We only sleep if we have to manage on-line requests
        if not isLocalOnly:
            time.sleep(CONTROL_MANAGER_REQUEST_DELAY)
        
        return currentFunctionResults
        
    #
    # This method is called when an analysis is made
    # it will call all selected analyser modules to get single 
    # function analysis.
    #
    # Returns
    # This method returns a list built like:
    # [HTML_RESULT_STRING, ...]
    #
    def analyseAction(self, singleFunction, searchersList):
        
        pluginToBeUsed = []
        
        #First, we get list of all plugins to be used
        for plugin in self._core._PlMngr._plugins:
            pluginType = self._core._PlMngr.callForPlugin(plugin, "identifyPluginType")
            if "analyser" in pluginType:
                if self._core._PlMngr.callForPlugin(plugin, "identifyPlugin")[0] in searchersList:
                    #User asked to use this plugin
                    pluginToBeUsed.append(plugin)
        
        #Will go trough the whole list
        currentFunctionResults = []
               
        for plugin in pluginToBeUsed:
            pluginObject = self._core._PlMngr.call(self._core._PlMngr.callForPlugin(plugin, "identifyPlugin")[0], self._core._PlMngr)
            result = pluginObject.pluginAnalyse(singleFunction[1])
            if result:
                currentFunctionResults.append(result)
        
        return currentFunctionResults

        
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    ctMngr = ControlManager()


   
