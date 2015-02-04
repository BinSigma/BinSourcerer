BinSourcerer
============

Assembly to Source Code Matching Framework for IDA Pro.

Updates
--------
v1.31: Dynamic Path

v1.30: Fixed Config

v1.20: GitHub Support

v1.10: BlackDuck Support

v1.00: HRC14


BinSourcerer (a.k.a RE-Source Online) is an assembly to source code matching framework for binary auditing and malware analysis. Please refer to the following papers for more information:

*** "RESource: A Framework for Online Matching of Assembly with Open Source Code"

http://dx.doi.org/10.1007/978-3-642-37119-6_14

*** "On the Reverse Engineering of the Citadel Botnet"

http://dx.doi.org/10.1007/978-3-319-05302-8_25

A quick guide can be found in:

https://github.com/BinSigma/BinSourcerer/wiki/Quick-Guide

BinSourcerer is an assembly to source code matching framework written in Python. The main purpose of BinSourcerer is to recreate the functionalities that RE-Google provided before the Google Code Search API was discontinued. This plugin can be used for code search (GitHub, Ohloh, etc.) and function tagging. It generates a disassembly feature file that can be used in various binary analyzes. Moreover, the framework functionalities are easily expandable.
