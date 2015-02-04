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

import math
import time

TOTAL_FILE_COUNT = 0

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
    return None #This utility does not need configuration
            
def configurationProvision(utilityConfig=[]):
    pass #This utility does not need configuration


#-----------------------------------------------------------------------
# EntropyCalculator
# This class is a simple utility that aim to be a versatile entropy
# calculator
#-----------------------------------------------------------------------
class EntropyCalculator():

    def __init__(self, utMngr):
        self._manager = utMngr

    # This comes from C. Shannon work.
    def ec_calculateEntropy(self, input, isHexa=True, isDecimal=False):
        entropy = 0
        rangeCalculation = []
        if input:
            input = input.upper()
            if isHexa:
                rangeCalculation = range(0x30, 0x3A)
                rangeCalculation.extend(range(0x41, 0x47))
            elif isDecimal:
                rangeCalculation = range(48, 58)
            else:
                rangeCalculation = range(32,256)
                
            for x in rangeCalculation:
                p_x = float(input.count(chr(x)))/len(input)
                if p_x > 0:
                    entropy += - p_x*math.log(p_x, 2)
        return entropy
    
    # This as been build from the previous (ec_calculateEntropy) in a try
    # to get an "entropy" calculation about function call from a offline
    # code base. This as primarily been built using trial an error...
    # This function could surely be improved given enough time.
    def ec_calculateFunctionalPseudoEntropy(self, input):
        global TOTAL_FILE_COUNT
        pseudoEntropy = 0
        rangeCalculation = []
        if input:

            searcher = self._manager._core._PlMngr.call("CodeSearcher", (self._manager._core._PlMngr))
            if TOTAL_FILE_COUNT == 0:
                #Initialising file count... This one will be long
                TOTAL_FILE_COUNT = len(set(searcher.codeSearch(" "))) #Attempt to get all the files
            
            if TOTAL_FILE_COUNT <= 0:
                return pseudoEntropy
            
            for x in input:
                fileWithFunctionCount = len(set(searcher.codeSearch(x)))
                
                p_x = float(fileWithFunctionCount) / TOTAL_FILE_COUNT
                if p_x > 0.0:
                    p_x = float(1) / p_x
                    pseudoEntropy += p_x*math.log(p_x, 2) / (TOTAL_FILE_COUNT)
                else:
                    pseudoEntropy = 8
                   
        return pseudoEntropy
    

#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    entroCalc = EntropyCalculator(None)
    value = raw_input()
    print entroCalc.ec_calculateEntropy(value)
    time.sleep(30)


   
