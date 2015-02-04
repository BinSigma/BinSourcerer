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

#All those config are inside configuration file
#Initial config for var typing only! This will be overwritten by config manager
SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT = 4
SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY = 2
SEARCH_FILTER_MINIMUM_STRING_LENGTH = 6
SEARCH_FILTER_MINIMUM_STRING_ENTROPY = 2
SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE = True
SEARCH_FILTER_FAST_SEARCH_ENABLE = True
SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT = 3
SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT = 1
SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT = 1
SEARCH_FILTER_WORD_DICTIONARY_FILE = ""
SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD = 1/3
SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY = 0.5

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
def configurationNeed():
    return ["SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT", "SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY", "SEARCH_FILTER_MINIMUM_STRING_LENGTH", 
            "SEARCH_FILTER_MINIMUM_STRING_ENTROPY", "SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE", "SEARCH_FILTER_FAST_SEARCH_ENABLE", "SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT",
            "SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT", "SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT", "SEARCH_FILTER_WORD_DICTIONARY_FILE",
            "SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD", "SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY"]
            
def configurationProvision(utilityConfig=[]):
    global SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT
    global SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY
    global SEARCH_FILTER_MINIMUM_STRING_LENGTH
    global SEARCH_FILTER_MINIMUM_STRING_ENTROPY
    global SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE
    global SEARCH_FILTER_FAST_SEARCH_ENABLE
    global SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT
    global SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT
    global SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT
    global SEARCH_FILTER_WORD_DICTIONARY_FILE
    global SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD
    global SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY
    
    SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT = utilityConfig[0]
    SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY = utilityConfig[1]
    SEARCH_FILTER_MINIMUM_STRING_LENGTH = utilityConfig[2]
    SEARCH_FILTER_MINIMUM_STRING_ENTROPY = utilityConfig[3]
    SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE = utilityConfig[4]
    SEARCH_FILTER_FAST_SEARCH_ENABLE = utilityConfig[5]
    SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT = utilityConfig[6]
    SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT = utilityConfig[7]
    SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT = utilityConfig[8]
    SEARCH_FILTER_WORD_DICTIONARY_FILE = utilityConfig[9]
    SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD = utilityConfig[10]
    SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY = utilityConfig[11]

#-----------------------------------------------------------------------
# SearchFilter
# This class should be used as filtering utility for search terms before
# building any search query.
#-----------------------------------------------------------------------
class SearchFilter():

    _wordBlackList = []

    def __init__(self, utMngr):
        self._manager = utMngr
        
        #Initiating _wordsBlackList        
        wordListFile = open(SEARCH_FILTER_WORD_DICTIONARY_FILE, "r")
        for line in wordListFile:
            self._wordBlackList.append(line)
        wordListFile.close()

    #Return list of search query terms tuples that pass
    #filtering process. If Input list does not pass filtering process
    #this function returns an empty list
    #input should be as [('type', 'searchTerm'), ...]
    def sf_filter(self, input=[]):
        stringCounter = 0
        constantCounter = 0
        functionCounter = 0
        resultList = []
        
        #filter all input
        for searchTerm in input:
            #specific filter for "imports" function
            if searchTerm[0] == 'n' or searchTerm[0] == 'i':
                functionEntro, canUse = self.sf_canUseThisFunction(searchTerm[1])
                if canUse:
                    if searchTerm not in resultList:
                        if len(searchTerm) == 2:
                            searchTerm = list(searchTerm)
                            searchTerm.append(functionEntro)
                            searchTerm = tuple(searchTerm)
                        functionCounter += 1
                        resultList.append(searchTerm)
                continue
            #specific filter for "constants"
            if searchTerm[0] == 'c':
                constEntro, canUse = self.sf_canUseThisConstant(searchTerm[1])
                if canUse:
                    if searchTerm not in resultList:
                        if len(searchTerm) == 2:
                            searchTerm = list(searchTerm)
                            searchTerm.append(constEntro)
                            searchTerm = tuple(searchTerm)
                        constantCounter += 1
                        resultList.append(searchTerm)
                else:
                    #Constant may be a good decimal candidate
                    if SEARCH_FILTER_DECIMAL_TRANSLATION_ENABLE:
                        decimal = str(int(searchTerm[1], 16)) #This is for code readability.
                        hexadecimal = searchTerm[1]
                        if self.sf_isGoodDecimalCandidate(hexadecimal, decimal):
                            if (searchTerm[0], decimal, constEntro) not in resultList:
                                resultList.append((searchTerm[0], decimal, constEntro))
                                constantCounter += 1
                                #print "Using decimal " + decimal
                        
                continue
            #specific filter for "strings"
            if searchTerm[0] == 's':
                stringEntro, canUse = self.sf_canUseThisString(searchTerm[1])
                if canUse:
                    if searchTerm not in resultList:
                        if len(searchTerm) == 2:
                            searchTerm = list(searchTerm)
                            searchTerm.append(stringEntro)
                            searchTerm = tuple(searchTerm)
                        resultList.append(searchTerm)
                        stringCounter += 1
        
        if SEARCH_FILTER_FAST_SEARCH_ENABLE:
            #
            # Fast Search has 3 rules to prevent false positive and useless searches
            #   1- Search has to have at least 1 good constant OR
            #   2- Search has to have at least 1 good string OR
            #   3- Search has to have at least 3 functions
            #
            if (stringCounter >= SEARCH_FILTER_FAST_SEARCH_MINIMUM_STRING_COUNT or
                constantCounter >= SEARCH_FILTER_FAST_SEARCH_MINIMUM_CONST_COUNT or
                functionCounter >= SEARCH_FILTER_FAST_SEARCH_MINIMUM_FUNCTION_COUNT):
                return resultList
            resultList = [] #Empty list search does not match fast search 3 rules   
        return resultList #Empty if nothing passed filters
        
    
    #Return True if this function can be used in search
    def sf_canUseThisFunction(self, inputFunction):
	SEARCH_PREP_AUTO_PRIORITIZE = False
        if inputFunction in self._wordBlackList:
            return 0, False

        if SEARCH_PREP_AUTO_PRIORITIZE:
            # get function entropy information
            entropyCalculator = self._manager.call("EntropyCalculator", self._manager)
            functionEntro = entropyCalculator.ec_calculateFunctionalPseudoEntropy([inputFunction])
        
        # make decisions based on configuration
        if SEARCH_PREP_AUTO_PRIORITIZE and functionEntro >= SEARCH_FILTER_MINIMUM_IMPORT_ENTROPY:
            return functionEntro, True
        elif SEARCH_PREP_AUTO_PRIORITIZE:
            return functionEntro, False
        else:
            # in this case we return 1 as entropy number because it will not be taken into account
            # since SEARCH_PREP_AUTO_PRIORITIZE is false.
            return 1, True

            
    #Return True if this string can be used in search
    def sf_canUseThisString(self, inputString):
        entro = 0.0
        if len(inputString) >= SEARCH_FILTER_MINIMUM_STRING_LENGTH:
            #Calculating string entropy
            entropyCalculator = self._manager.call("EntropyCalculator", self._manager)
            entro = entropyCalculator.ec_calculateEntropy(inputString, isHexa=False)
            if entro >= SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY:
                #Now check for dictionary forbidden words
                brokenInput = inputString.split()
                forbiddenWordCounter = 0
                
                for word in brokenInput:
                    if word in self._wordBlackList:
                        forbiddenWordCounter += 1
                if (forbiddenWordCounter/len(brokenInput))*100 <= SEARCH_FILTER_PRESENT_IN_DICTIONARY_THRESHOLD:
                    #Forbidden word ratio is low enough to use the string!
                    #All conditions are met, we can use the string!
                    return entro, True
        
        return entro, False
        
    #Return True if this constant can be used in search
    def sf_canUseThisConstant(self, inputConstant):
        if len(inputConstant) >= SEARCH_FILTER_MINIMUM_CONSTANT_DIGIT:
            #Calculating constant entropy
            entropyCalculator = self._manager.call("EntropyCalculator", self._manager)
            entro = entropyCalculator.ec_calculateEntropy(inputConstant, isHexa=True)
            if entro >= SEARCH_FILTER_MINIMUM_CONSTANT_ENTROPY:
                return entro, True
        return 0, False
        
    def sf_isGoodDecimalCandidate(self, inputConstantHex, inputConstantDec):
        #Calculating constant entropy
        entropyCalculator = self._manager.call("EntropyCalculator", self._manager)
        #If hex entropy is high
        if entropyCalculator.ec_calculateEntropy(inputConstantHex, isHexa=True) > 1.5:
            #And dec entropy is low
            if entropyCalculator.ec_calculateEntropy(inputConstantDec, isHexa=False, isDecimal=True) <= 1:
                #Programmer probably wrote this constant using the decimal value.
                return True
        return False
 
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    searchFilt = SearchFilter()


   
