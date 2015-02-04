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

import time
import random
import string
import os
import sys
import md5
import urllib
from bs4 import BeautifulSoup

REPORT_MANAGER_OUTPUT_REPORT_PATH = ""

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
    return ["REPORT_MANAGER_OUTPUT_REPORT_PATH"]
            
def configurationProvision(utilityConfig=[]):
    global REPORT_MANAGER_OUTPUT_REPORT_PATH
    REPORT_MANAGER_OUTPUT_REPORT_PATH = utilityConfig[0]

#----------------------------------------------------------------------
# Plugin type
# Since many plugins with diferent capabilities can be integrated
# to the framework, we need a general method to understand the
# use of each plugin in a unified way. The value returned by this method
# will allow the framework to call the right operations on the plugin.
#----------------------------------------------------------------------
def identifyPluginType():
    return ["searcher"] 
    
#-----------------------------------------------------------------------
# Plugin name
# This is used so the framework can give a name to a specific plugin
# The name will be used to visualy identify each plugins.
#-----------------------------------------------------------------------
def identifyPlugin():
    return ["OhlohCCPPSearcher", "BlackDuck (C/C++)"] #First item in list have to have the same name as main class name. Second item in list is visual name
       
#-----------------------------------------------------------------------
# OhlohSearcher
# This class implements Ohloh online search capabilities
#-----------------------------------------------------------------------
class OhlohCCPPSearcher():

    def __init__(self, plMngr):
        self._manager = plMngr
        
        self.__repONL = """
        <h3>%s</h3>
        %s <br />
        <b>Elements : </b> <font color="SaddleBrown" face="Courier New,Courier, monospace">
        %s</font> <br />
        <b>Projects : </b> <font color="Green" face="Courier New,Courier, monospace">
        %s</font><br />""" 
        self.__repLNK = """
        <b>Source : </b> %s <br />"""
    
    #
    # This method is used to manage request timing. Local search engines
    # do not need wait time in between request. This method will be called
    # by the control manager when managing search or analysis requests.
    #
    def isLocal(self):
        return False
    

    #
    # Main search plugin function, returns HTML string
    # that can be used by the report manager.
    #
    def pluginSearch(self, searchList):
        #First, we only keep good search terms
        #searchList = self.filterSearchItems(searchList)
        #Now, select terms in order not to overflow the search query buffer
        searchQuery = self.selectSearchItems(searchList)
        if searchQuery == None:
            return "" #Search not worth the time...
        #Out on the Internet to get results
        results, sourcefiles, projects, pageMd5Sum = self.doSearch(searchQuery)
        #Parsing results and report HTML string generation
        searchQuery = urllib.unquote_plus(searchQuery)
        resultHTML = self.GenerateOhlohHtml(results, projects, pageMd5Sum, searchQuery)
        return resultHTML
        
    #
    # This is used to filter search items. After this is called
    # only "good" search terms should be present inside the search
    # list items.
    #
    def filterSearchItems(self, searchList):
        filter = self._manager._core._UtMngr.call("SearchFilter", self._manager._core._UtMngr)
        return filter.sf_filter(searchList)
    
    #
    # Search items selection in order to prepare limit search.
    # WARNING, this returns a query string to be used inside a 
    # search!!!
    #
    def selectSearchItems(self, searchList):
        prepper = self._manager._core._UtMngr.call("SearchPrep", self._manager._core._UtMngr)
        return prepper.sp_prepareSearch(searchList, maxLength=1000, quoteAroundStrings=True) #Ohloh has 1000 chars limits
    
    #
    # Search is sent to Ohloh, this function
    # returns on disk results file + parsed results
    #
    def doSearch(self, searchQuery):
        ohlohQuery = "http://code.openhub.net/search?s=" + searchQuery
        ohlohQueryPostfix="&browser=Default&pp=0&fl=C%2B%2B&fl=C&mp=1&ml=1&me=1&md=1&ff=1&filterChecked=true"
        
        webFetcher = self._manager._core._UtMngr.call("WebFetcher", self._manager._core._UtMngr)
        requestCounter = 0
        htmlResults = webFetcher.wf_fetchPage(ohlohQuery + ohlohQueryPostfix)
        
        #This has to be here because Ohloh has many "misses"
        while htmlResults == "" and requestCounter <= 3:
            requestCounter += 1
            time.sleep(requestCounter * 5) #Give Ohloh some time has proven to be very effective against Ohloh misses
            htmlResults = webFetcher.wf_fetchPage(ohlohQuery + ohlohQueryPostfix)
        
        comment, src, prj, ress, pageMd5Sum = self.parseOhlohPage(htmlResults)
        return ress, src, prj, pageMd5Sum

    #
    # This will parse the results files so they can later be used to generate
    # HTML for the report
    #
    def parseOhlohPage(self, HtmlPage):
        ##
        ##
        ##Writing result page to disk
        webFetcher = self._manager._core._UtMngr.call("WebFetcher", self._manager._core._UtMngr)
        #Full local implementations of specific files:
        if not os.path.isdir(REPORT_MANAGER_OUTPUT_REPORT_PATH):
            #Creating directory for support files
            os.mkdir(REPORT_MANAGER_OUTPUT_REPORT_PATH)
        
        # Following files are required in order to get the right display
        # for Ohloh pages. Download only if we don't already have them...
        if not os.path.isfile(REPORT_MANAGER_OUTPUT_REPORT_PATH + "csOhlohDesign.css"):
            supportHtml = webFetcher.wf_fetchPage("http://code.openhub.net/style/csOhlohDesign.css")
            f = open(REPORT_MANAGER_OUTPUT_REPORT_PATH + "csOhlohDesign.css", "w")
            f.write(supportHtml)
            f.close()
        if not os.path.isfile(REPORT_MANAGER_OUTPUT_REPORT_PATH + "select2.css"):
            supportHtml = webFetcher.wf_fetchPage("http://code.openhub.net/style/select2.css")
            f = open(REPORT_MANAGER_OUTPUT_REPORT_PATH + "select2.css", "w")
            f.write(supportHtml)
            f.close()
        if not os.path.isfile(REPORT_MANAGER_OUTPUT_REPORT_PATH + "sharing.js"):
            supportHtml = webFetcher.wf_fetchPage("http://code.openhub.net/js/sharing.js")
            f = open(REPORT_MANAGER_OUTPUT_REPORT_PATH + "sharing.js", "w")
            f.write(supportHtml)
            f.close()
        if not os.path.isfile(REPORT_MANAGER_OUTPUT_REPORT_PATH + "sharedHeader.js"):
            supportHtml = webFetcher.wf_fetchPage("http://code.openhub.net/js/sharedHeader.js")
            f = open(REPORT_MANAGER_OUTPUT_REPORT_PATH + "sharedHeader.js", "w")
            f.write(supportHtml)
            f.close()
        if not os.path.isfile(REPORT_MANAGER_OUTPUT_REPORT_PATH + "searchPageResults.js"):
            supportHtml = webFetcher.wf_fetchPage("http://code.openhub.net/js/searchPageResults.js")
            f = open(REPORT_MANAGER_OUTPUT_REPORT_PATH + "searchPageResults.js", "w")
            f.write(supportHtml)
            f.close()
        if not os.path.isfile(REPORT_MANAGER_OUTPUT_REPORT_PATH + "jquery.min.js"):
            supportHtml = webFetcher.wf_fetchPage("http://code.openhub.net/style/googleapis/1.7.1/jquery.min.js")
            f = open(REPORT_MANAGER_OUTPUT_REPORT_PATH + "jquery.min.js", "w")
            f.write(supportHtml)
            f.close()
        if not os.path.isfile(REPORT_MANAGER_OUTPUT_REPORT_PATH + "jquery.jstree.js"):
            supportHtml = webFetcher.wf_fetchPage("http://code.openhub.net/js/jstree/jquery.jstree.js")
            f = open(REPORT_MANAGER_OUTPUT_REPORT_PATH + "jquery.jstree.js", "w")
            f.write(supportHtml)
            f.close()
        if not os.path.isfile(REPORT_MANAGER_OUTPUT_REPORT_PATH + "ohlohDesign.js"):
            supportHtml = webFetcher.wf_fetchPage("http://code.openhub.net/js/ohlohDesign.js")
            f = open(REPORT_MANAGER_OUTPUT_REPORT_PATH + "ohlohDesign.js", "w")
            f.write(supportHtml)
            f.close()
        if not os.path.isfile(REPORT_MANAGER_OUTPUT_REPORT_PATH + "select2.js"):
            supportHtml = webFetcher.wf_fetchPage("http://code.openhub.net/js/select2.js")
            f = open(REPORT_MANAGER_OUTPUT_REPORT_PATH + "select2.js", "w")
            f.write(supportHtml)
            f.close()
        
        #Fixing img and links paths
        tempHtmlPage = string.replace(HtmlPage, "href='/", "href='http://code.openhub.net/")
        tempHtmlPage = string.replace(tempHtmlPage, "href=\"/", "href=\"http://code.openhub.net/")
        tempHtmlPage = string.replace(tempHtmlPage, "src='/", "src='http://code.openhub.net/")
        tempHtmlPage = string.replace(tempHtmlPage, "src=\"/", "src=\"http://code.openhub.net/")
        tempHtmlPage = string.replace(tempHtmlPage, "action='/", "action='http://code.openhub.net/")
        tempHtmlPage = string.replace(tempHtmlPage, "action=\"/", "action=\"http://code.openhub.net/")
        
        #Fixing javascript paths
        tempHtmlPage = string.replace(tempHtmlPage, "return getActionURL()", "")
        tempHtmlPage = string.replace(tempHtmlPage, "orginalHref.substring(0, orginalHref.indexOf(window.location.search));", "\"http://code.openhub.net\"")

        tempHtmlPage = string.replace(tempHtmlPage, "http://code.openhub.net/style/csOhlohDesign.css", "csOhlohDesign.css")
        tempHtmlPage = string.replace(tempHtmlPage, "http://code.openhub.net/style/select2.css", "select2.css")
        tempHtmlPage = string.replace(tempHtmlPage, "http://code.openhub.net/js/sharing.js", "sharing.js")
        tempHtmlPage = string.replace(tempHtmlPage, "http://code.openhub.net/js/sharedHeader.js", "sharedHeader.js")
        tempHtmlPage = string.replace(tempHtmlPage, "http://code.openhub.net/js/searchPageResults.js", "searchPageResults.js")
        tempHtmlPage = string.replace(tempHtmlPage, "http://code.openhub.net/style/googleapis/1.7.1/jquery.min.js", "jquery.min.js")
        tempHtmlPage = string.replace(tempHtmlPage, "http://code.openhub.net/js/jstree/jquery.jstree.js", "rjquery.jstree.js")
        tempHtmlPage = string.replace(tempHtmlPage, "http://code.openhub.net/js/ohlohDesign.js", "ohlohDesign.js")
        tempHtmlPage = string.replace(tempHtmlPage, "http://code.openhub.net/js/select2.js", "select2.js")
        
        pageMd5Sum = md5.new(HtmlPage).hexdigest()
        pageMd5Sum = REPORT_MANAGER_OUTPUT_REPORT_PATH + "" + pageMd5Sum + ".html"
        f = open(pageMd5Sum, "w")
        f.write(tempHtmlPage)
        f.close()

        ##End writing result page to disk
        ##
        ##
        
        soup=BeautifulSoup(HtmlPage)
        #Ohloh Search Engine
        LDIC = {} #Dictionary
        LL =[] #List of Links
        DICLIST = [] #List of Result,Link tuples
        src = ""
        prj = ""
        ohlohUrl = 'http://code.openhub.net'
        try:
            #Extract the Filename and Source URL
            fileNameList = []
            sourceUrlList = []
            for itm in soup('div', {'class': 'fileNameLabel'}):
                fln = itm.a.text.encode('ascii','ignore')
                fileNameList.append(fln)
                flu = ohlohUrl+str(itm.a['href'])
                sourceUrlList.append(flu)
                #Build the dictionary
                LDIC.update( { flu : fln } )
                DICLIST = LDIC.items()
            
            if (fileNameList):
                src = ', '.join(self.remove_duplicates(fileNameList))
            #Extract the Project Name
            projectNameList = [blt.a.text.encode('ascii','ignore') for blt in soup.findAll('div', {'class': 'projectNameLabel'})]
            if (projectNameList):
                prj = ', '.join(self.remove_duplicates(projectNameList))
        except:
            print " --Non-standard page style (Html formatting _err_)"
            
        comment = ""
        ress=DICLIST
        i = 0
        lrs=len(DICLIST)

        while i < lrs:
            title = ' _ '.join(DICLIST[i])
            comment += title + "\n"
            i += 1    
        
        return comment, src, prj, ress, pageMd5Sum
    
    def remove_duplicates(self, inpLst):
        return list(set(inpLst))
    
    #
    # Final report HTML string preparation
    #
    def GenerateOhlohHtml(self, ohlohResults, projects, resultPath, query):
        if len(ohlohResults) == 0:
            return ""
        
        htmlString = ""
        ohlohLink = ""
        if resultPath is not "":
            splitted = resultPath.split("\\") if (os.name == "nt" and sys.platform == "win32") else resultPath.split("/")
            ohlohLink += "<a href=\"" + splitted[len(splitted)-1] + "\">See Ohloh results</a>"
        #

        htmlString += (self.__repONL % ("Ohloh", ohlohLink, query, projects) )

        if ohlohResults:
            for j in range(len(ohlohResults)):
                htmlString += (self.__repLNK % self.getLink(ohlohResults[j][1],ohlohResults[j][0]))
        return htmlString
    #
    # Helper method for GenerateOhlohHtml
    #
    def getLink(self, label, url):
        return '<a href="%s">%s</a>' % (url, label)
    
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    searcher = OhlohSearcher(None)


   
