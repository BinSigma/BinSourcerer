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

import urllib #used for the quote function (encoding search query)
from operator import itemgetter #for ordering tuple list

#-----------------------------------------------------------------------
# Configuration agent
# The two next function are needed so the configuration manager will be
# able to provide configuration for this module.
# configurationNeed is called first. If no config for this 
# utility exists, user is prompted for utility configuration. If
# configuration exists, previous configs will be used. In all cases,
# configuration step is ended when configurationProvision
# is called with a configuration list as arg.
#-----------------------------------------------------------------------

#This configuration comes from the configuration file.
SEARCH_PREP_AUTO_PRIORITIZE = False


def configurationNeed():
    ####return ["SEARCH_PREP_AUTO_PRIORITIZE"]
	return None
            
def configurationProvision(utilityConfig=[]):
	pass
    ####global SEARCH_PREP_AUTO_PRIORITIZE
    ####SEARCH_PREP_AUTO_PRIORITIZE = utilityConfig[0]


#-----------------------------------------------------------------------
# SearchPrep
# This class is a simple utility that aim to be a versatile entropy
# calculator
#-----------------------------------------------------------------------
class SearchPrep():

    def __init__(self, utMngr):
        self._manager = utMngr

    #inputSearchTerms is tuple list containing search terms
    #return a single string to be used in search queries
    #in case search query is too long, this prep function
    #will select object to go in search based on priority
    #level, the higher, the better
    def sp_prepareSearch(self, inputSearchTerms, maxLength=1000, stringPriority=3, constantPriority=2, functionPriority=1, encodeOutput=True, quoteAroundStrings=True, quoteAroundConst=False, prefixHexConst=False):
        inputSearchTerms = sorted(inputSearchTerms, key=itemgetter(2), reverse=True)
        
        if SEARCH_PREP_AUTO_PRIORITIZE:
            #We will work that entropy out!
            return self.sp_prepareSearch_Auto(inputSearchTerms, maxLength, encodeOutput, quoteAroundStrings, quoteAroundConst, prefixHexConst)
        else:
            #Nothing fancy, just build the search (in fact this is more complicated...)
            return self.sp_prepareSearch_NotAuto(inputSearchTerms, maxLength, stringPriority, constantPriority, functionPriority, encodeOutput, quoteAroundStrings, quoteAroundConst, prefixHexConst)
        
 
    
    def sp_prepareSearch_NotAuto(self, inputSearchTerms, maxLength=1000, stringPriority=3, constantPriority=2, functionPriority=1, encodeOutput=True, quoteAroundStrings=True, quoteAroundConst=False, prefixHexConst=False):
        iterationCounter = 0;
        searchString = ""
        functionCounter = 0
        functionList = []
        stringCounter = 0
        stringList = []
        constantCounter = 0
        constantList = []
        
        #Knowing how much of each type is required if we need
        #to use prioritisation scheme 
        for searchTerm in inputSearchTerms:
            if searchTerm[0] == 'n' or searchTerm[0] == 'i':
                if not searchTerm[1] in functionList: #If already in list, do not use
                    functionCounter += 1
                    functionList.append(searchTerm[1])
                continue
            if searchTerm[0] == 'c':
                if not searchTerm[1] in functionList: #If already in list, do not use
                    constantCounter += 1
                    constantList.append(searchTerm[1])
                continue
            if searchTerm[0] == 's':
                if not searchTerm[1] in functionList: #If already in list, do not use
                    stringCounter += 1
                    stringList.append(searchTerm[1])
        
        #sort on length to help the selection process
        stringList.sort(key=len, reverse=False)
        constantList.sort(key=len, reverse=False)
        functionList.sort(key=len, reverse=False)
        
        while iterationCounter < 100:
            #Building query with all that is left
            for i in range(0, stringCounter):
                if quoteAroundStrings and len(stringList[i]) < 35 and " " in stringList[i]: #Only use quotes if there are
                                                                                            #more than 1 word in a string
                    searchString += " \"" + stringList[i] + "\""
                else:
                    searchString += " " + stringList[i]
                
            for i in range(0, constantCounter):
                if quoteAroundConst:
                    if prefixHexConst:
                        searchString += " \"" + "0x" + constantList[i] + "\""
                    else:
                        searchString += " \"" + constantList[i] + "\""
                else:
                    if prefixHexConst:
                        searchString += " " + "0x" + constantList[i]
                    else:
                        searchString += " " + constantList[i]
                
            for i in range(0, functionCounter):
                searchString += " " + functionList[i]
            
            #Encode before length check
            if encodeOutput:
                searchString = urllib.quote_plus(searchString)
            
            #If length matches, we have a query! Ready to go!
            if len(searchString) <= maxLength:
                return searchString
            
            #But if we don't... Time for some compromise
            priorityList = [(stringPriority, stringCounter), (constantPriority, constantCounter), (functionPriority, functionCounter)]
            lowestValue = 100
            lowestIndex = -1
            
            #Find the current less important type
            for i in range(0, len(priorityList)):
                if priorityList[i][0] < lowestValue and priorityList[i][1] > 0:
                    lowestValue = priorityList[i][0]
                    lowestIndex = i
            
            if lowestIndex == 2: #Function are the current less important items
                functionCounter -= 1
            elif lowestIndex == 1: #Constants are the current less important items
                constantCounter -= 1
            else: #Strings are the current less important items
                stringCounter -= 1

            searchString = ""
            iterationCounter += 1
        
        return None #If we're here, it was not possible to 
                  #build a search that match the length and rules given by the user
                  #Class user will have to choose the best way to handle this situation
                  #inside calling code. 
    
    def sp_prepareSearch_Auto(self, inputSearchTerms, maxLength=1000, encodeOutput=True, quoteAroundStrings=True, quoteAroundConst=False, prefixHexConst=False):
        #print inputSearchTerms
        lastGoodSearchQuery = ""
        currentSearchQuerry = ""
        searchString = ""
        
        for item in inputSearchTerms:
            if len(currentSearchQuerry) < maxLength:
                lastGoodSearchQuery = currentSearchQuerry
                
                if quoteAroundConst and item[0] == 'c':
                    if prefixHexConst:
                        searchString += " \"" + "0x" + item[1] + "\""
                    else:
                        searchString += " \"" + "0x" + item[1] + "\""
                elif quoteAroundStrings and item[0] == 's' and len(item[1]) < 35 and " " in item[1]: #Only use quotes if there are
                                                                                                                     #more than 1 word in a string
                    searchString += " \"" + item[1] + "\""
                else:
                    if item[0] == 'c' and prefixHexConst:
                        searchString += " " + "0x" + item[1]
                    else:
                        searchString += " " + item[1]
                    
                if encodeOutput:
                    currentSearchQuerry = urllib.quote_plus(searchString)
                else:
                    currentSearchQuerry = searchString
            else:
                print "Too long"
                break

        if len(currentSearchQuerry) < maxLength:
            lastGoodSearchQuery = currentSearchQuerry
        
        if len(lastGoodSearchQuery) == 0:
            return None
        return lastGoodSearchQuery
    
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    entroCalc = EntropyCalculator()


   
