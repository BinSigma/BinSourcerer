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

import sys, time
from PySide.QtCore import *
from PySide.QtGui import *

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
# UINAME
# This class implements X capabilities
#-----------------------------------------------------------------------
class IndependentProgressBar(QWidget):
    
    #root = None
    _cancelled = False

    def __init__(self, uiMngr, parent=None,):
        super(IndependentProgressBar, self).__init__(parent)
        self._manager = uiMngr
        self.setFixedSize(500, 100)
        self.progressbar = QProgressBar()
        self.progressbar.setMinimum(1)

    #
    # This method build and show a single stand alone progress bar
    # that will be under the calling code control. Correct usage by
    # user is assumed. Single steps are calculated from user input.
    # all user should have to do in order to use the bar is to pass
    # maxValue when progressBar is shown and then call stepProgressBar
    # each time a "milestone" is reach within calling code.
    #
    def showProgressBar(self, name="Progress", displayedText="In progress, please wait...", maxValue=0.0):
        if maxValue == 0:
            return
        
        # Getting the progress bar ready
        self.progressbar.setMaximum(maxValue)
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progressbar)
        
        # Add button and label informations
        label = QLabel(displayedText)
        button = QPushButton("Cancel")
        button.clicked.connect(self.cancelAction)
        interact_layout = QHBoxLayout()
        interact_layout.addWidget(label)
        button_layout = QGridLayout()
        label = QLabel("")
        button_layout.addWidget(label, 0,0)
        button_layout.addWidget(button, 0,1)
        button_layout.addWidget(label, 0,2)
        
        # Put it all together and display the progress bar
        main_layout = QVBoxLayout()
        main_layout.addLayout(interact_layout)
        main_layout.addLayout(progress_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self.setWindowTitle(name)
        self._active = True
        self.show()
        
    
    #
    # Calling this method will advance progress bar 1 step ahead
    #
    def stepProgressBar(self):
        self.progressbar.setValue(self.progressbar.value() + 1)
        self._manager._core.app.processEvents()
    
    #
    # When user is done using the progress bar, he calls this method.
    #
    def hideProgressBar(self):
        self.close()
        
    #
    # This will change the _canceled value. At all iteration,
    # user should check this value to make sure it's not true.
    # if it is, user has cancelled the current task and it should be stopped
    #
    def cancelAction(self):
        self._cancelled = True

#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":

    app = QApplication([])
    mainWindow = IndependentProgressBar("MainWindow", None)
    mainWindow.showProgressBar(maxValue=500, text="Progress bar sample text.")
    mainWindow.stepProgressBar()
    #mainWindow.show()
    app.exec_()

   
