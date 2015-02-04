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

DIRECTION_FORW = 0x03

import BSConfigurationManager
import idautils
import os

import idautils
import hashlib

#Offline Analyzer (OA), Windows function names and a brief description.
WinMalFuncInSight = {
    'accept':'The program may listen for incoming connections on a socket.',
    'AdjustTokenPrivileges':'The program may modify specific access privileges.',
    'AttachThreadInput':'The program may contain keylogging or spyware functionality.',
    'bind':'The program may listen for incoming connections.',
    'BitBlt':'The program may capture screenshots.',
    'CallNextHookEx':'The code calls the next hook in the chain set by SetWindowsHookEx.',
    'CertOpenSystemStore':'The program may access the certificates stored on the local system.',
    'CheckRemoteDebuggerPresent':'The code may contain an anti-debugging technique.',
    'CoCreateInstance':'The code creates a COM object.',
    'connect':'The program may connect to a remote command-and-control server.',
    'ConnectNamedPipe':'The code may create a server pipe for interprocess communication',
    'ControlService':'The code may start, stop, modify, or send a signal to a running service.',
    'CreateFile':'The program may create a new file or open an existing file.',
    'CreateFileMapping':'The code may read and modify PE files by creating handles to file mappings.',
    'CreateMutex':'Only one instance of the program runs on a system.',
    'CreateProcess':'The code may create and launch a new process.',
    'CreateRemoteThread':'The program may inject code into a different process.',
    'CreateService':'The program may create an autorun service or load kernel drivers.',
    'CreateToolhelp32Snapshot':'The code may create a snapshot of processes, heaps, threads, and modules.',
    'CryptAcquireContext':'The code may initialize the use of Windows encryption.',
    'DeviceIoControl':'The code may send control messages from user space to kernel space.',
    'DllCanUnloadNow':'The program implements a COM server. (Exported function)',
    'DllGetClassObject':'The program implements a COM server. (Exported function)',
    'DllInstall':'The program implements a COM server. (Exported function)',
    'DllRegisterServer':'The program implements a COM server. (Exported function)',
    'DllUnregisterServer':'The program implements a COM server. (Exported function)',
    'EnableExecuteProtectionSupport':'The code may modify the Data Execution Protection (DEP) settings of the host.',
    'EnumProcesses':'The code may enumerate through processes to find a process to inject into.',
    'EnumProcessModules':'The code may enumerate the loaded modules for injection.',
    'FindFirstFile':'The program may search through a directory and enumerate the filesystem.',
    'FindNextFile':'The program may search through a directory and enumerate the filesystem.',
    'FindResource':'The code may search for a resource in an executable or loaded DLL',
    'FindWindow':'The code searches for an open window on the desktop. (It may also contain anti-debugging)',
    'FtpPutFile':'The program may upload files to a remote FTP server.',
    'GetAdaptersInfo':'The code may obtain information about the MAC, network adapters on the system.',
    'GetAsyncKeyState':'The code may contain keylogger functionality.',
    'GetDC':'The code returns a handle to a device context for a window or the whole screen. (Screen Capture)',
    'GetForegroundWindow':'The code returns a handle to the window currently in the foreground of the desktop. (Keylogger)',
    'gethostbyname':'The code may perform a DNS lookup on a particular hostname. (C&C)',
    'gethostname':'The code may retrieve the hostname of the computer. (Backdoor)',
    'GetKeyState':'The code may obtain the status of a particular key on the keyboard. (Keylogger)',
    'GetModuleFilename':'The code may return the filename of a module that is loaded in the current process.',
    'GetModuleHandle':'The code may obtain a handle to an already loaded module. (Inject Code)',
    'GetProcAddress':'The code may retrieve the address of a function in a DLL loaded into memory.',
    'GetStartupInfo':'The code may get details about how the current process was configured to run',
    'GetSystemDefaultLangId':'The code may return the default language settings for the system.',
    'GetTempPath':'The code may return the temporary file path.',
    'GetThreadContext':'The code may read the context of a thread. (register values and current state)',
    'GetTickCount':'The code may retrieve the number of milliseconds since bootup. (Anti-debugging)',
    'GetVersionEx':'The code may return information about which version of Windows is currently running.',
    'GetWindowsDirectory':'The code may get the file path to the Windows directory.',
    'inet_addr':'The code may process IP addresses for network connectivity.',
    'InternetOpen':'The code may initialize the high-level Internet access functions from WinINet',
    'InternetOpenUrl':'The program may open a specific URL for a connection using FTP, HTTP, or HTTPS.',
    'InternetReadFile':'The program may read data from a previously opened URL.',
    'InternetWriteFile':'The program may write data to a previously opened URL.',
    'IsDebuggerPresent':'The code may check to see if the current process is being debugged. (Anti-debugging)',
    'IsNTAdmin':'The code checks if the user has administrator privileges.',
    'IsWoW64Process':'The code may check if it is running on a 64-bit operating system.',
    'LdrLoadDll':'The code uses a low-level function to load a DLL into a process and it may attempt to be stealthy.',
    'LoadLibrary':'The code loads a DLL into a process that may not have been loaded when the program started.',
    'LoadResource':'The code may load a resource from a PE file into memory.',
    'LsaEnumerateLogonSessions':'The code may enumerate through logon sessions on the current system.',
    'MapViewOfFile':'The code maps a file into memory and makes the contents of the file accessible via memory addresses.',
    'MapVirtualKey':'The code may translate a virtual-key code into a character value. (Keylogger)',
    'MmGetSystemRoutineAddress':'The code may retrieve the address of a function from another module. (Kernel code)',
    'Module32First':'The code may enumerate through modules loaded into a process. (Injector)',
    'Module32Next':'The code mya enumerate through modules loaded into a process. (Injector)',
    'NetScheduleJobAdd':'The code may submit a request for a program to be run at a specified date and time in the future.',
    'NetShareEnum':'The code may enumerate network shares.',
    'NtQueryDirectoryFile':'The code may get information about files in a directory. (Rootkit)',
    'NtQueryInformationProcess':'The code may return various information about a specified process. (Anti-debugging)',
    'NtSetInformationProcess':'The code may change the privilege level of a program or to bypass Data Execution Prevention (DEP).',
    'OleInitialize':'The code initialize the COM library.',
    'OpenMutex':'The code may open a handle to a mutual exclusion object to ensure that only a single instance is running.',
    'OpenProcess':'The code may open a handle to another process to read/write or to inject code.',
    'OpenSCManager':'The code may open a handle to the service control manager.',
    'OutputDebugString':'The code may output a string to a debugger if one is attached. (Anti-debugging)',
    'PeekNamedPipe':'The code may copy data from a named pipe without removing data from the pipe. (Reverse shell)',
    'Process32First':'The code may enumerate through processes to find a process to inject into.',
    'Process32Next':'The code may enumerate through processes to find a process to inject into.',
    'QueryPerformanceCounter':'The code may retrieve the value of the hardware-based performance counter. (Anti-debugging)',
    'QueueUserAPC':'The code may execute code for a different thread and inject code into another process.',
    'ReadProcessMemory':'The code may read the memory of a remote process.',
    'recv':'The code may receive data from a remote command-and-control server.',
    'RegisterHotKey':'The code may register a handler to be notified anytime a user enters a particular key combination.',
    'RegOpenKey':'The code may open a handle to a registry key for reading and editing.',
    'ResumeThread':'The code may resume a previously suspended thread for injection.',
    'RtlCreateRegistryKey':'The code may create a registry from kernel-mode code.',
    'RtlWriteRegistryValue':'The code may write a value to the registry from kernel-mode code.',
    'SamIConnect':'The code may connect to the Security Account Manager in order to make future calls that access credential information. (Hash-dumping)',
    'SamIGetPrivateData':'The code may query the private information about a specific user from the Security Account Manager (SAM) database. (Hash-dumping)',
    'SamQueryInformationUse':'The code may query information about a specific user in the Security Account Manager (SAM) database. (Hash-dumping)',
    'send':'The code may send data to a remote command-and-control server.',
    'SetFileTime':'The code may modify the creation/access/last modified time of a file.',
    'SetThreadContext':'The code may modify the context of a given thread for code injection.',
    'SetWindowsHookEx':'The code may set a hook function to be called whenever a certain event is called. (Keylogger)',
    'SfcTerminateWatcherThread':'The code may disable Windows file protection and modify the otherwise protected files.',
    'ShellExecute':'The code may execute another program and create a new process.',
    'StartServiceCtrlDispatcher':'The code may run as a service.',
    'SuspendThread':'The code may suspend a thread to modify it by performing code injection.',
    'system':'The code may run another program provided by some C runtime libraries. (wrapper function to CreateProcess.',
    'Thread32First':'The code may iterate through the threads of a process to find an appropriate thread to inject into.',
    'Thread32Next':'The code may iterate through the threads of a process to find an appropriate thread to inject into.',
    'Toolhelp32ReadProcessMemory':'The code may read the memory of a remote process.',
    'URLDownloadToFile':'The code may download a file from a web server and save it to disk.',
    'VirtualAllocEx':'The code may allocate memory in a remote process as part of process injection.',
    'VirtualProtectEx':'The code may change the protection on a region of memory from read-only to executable.',
    'WideCharToMultiByte':'The code may convert a Unicode string into an ASCII string.',
    'WinExec':'The code may execute another program by creating a new process.',
    'WlxLoggedOnSAS':'The code may perform Graphical Identification and Authentication (GINA) replacement.',
    'Wow64DisableWow64FsRedirection':'The code may disable file redirection that occurs in 32-bit files loaded on a 64-bit system.',
    'WriteProcessMemory':'The code may write data to a remote process as part of process injection.',
    'WSAStartup':'The code may initialize low-level network functionality.'
     }

# These lists are for renaming functions if they contain certain API names. Based on the script by Alexander Hanel.

# resource manipulation
launcher = ['LCH','FindResource','LoadResource','SizeofResource']
# injection attacks
process_injection = ['PSJ','VirtualAllocEx','WriteProcessMemory']
DLL_injection = ['DLJ','CreateToolhelp32Snapshot','Process32First','Process32Next', 'OpenProcess', 'CreateRemoteThread', 'WriteProcessMemory']
direct_injection = ['DRJ', 'VirtualAllocEx','WriteProcessMemory','CreateRemoteThread']
process_replacement = ['PRP', 'ZwUnmapViewOfSection','VirtualAllocEx','WriteProcessMemory','SetThreadContext','ResumeThread']
hook_injection = ['HKJ', 'SetWindowsHookEx','CallNextHookEx','UnhookWindowsHookEx']
APC_injection = ['ACJ', 'CreateRemoteThread','WaitForSingleObjectEx','WaitForMultipleObjectsEx','Sleep']
APC_userspace = ['AUJ', 'QueueUserAPC','WaitForSingleObjectEx','CreateToolhelp32Snapshot','Process32First','Process32Next','Thread32Next',\
                 'Thread32First','NtQuerySystemInformation','ZwQuerySystemInformation']
APC_kernelspace = ['AKJ', 'KeInitializeApc','KeInsertQueueApc']
# networking code
windows_networking = ['WNT','WSAStartup','getaddrinfo','socket','connect','send','recv','WSAGetLastError','InternetOpen','InternetConnect',\
                      'InternetOpenURL','InternetReadFile','InternetWriteFile','HTTPOpenRequest','HTTPQueryInfo','HTTPSendRequest',\
                      'URLDownloadToFile','CoInitialize','CoCreateInstance','Navigate','gethostbyname']
anti_debugging = ['ADB','IsDebuggerPresent','CheckRemoteDebuggerPresent','NtQueryInfromationProcess','OutputDebugString','FindWindow',\
                  'QueryPerformanceCounter','GetTickCount']
# anti-vm x86 instructions -> e.g. GetMnem(i) == "cpuid"
anti_vmx86 = ['AVM','sidt','sgdt','sldt','smsw','str','in','cpuid']

reg = [ 'REG', 'RegCloseKey' ,'RegConnectRegistryA' ,'RegConnectRegistryW' ,'RegCreateKeyA' ,'RegCreateKeyExA' ,'RegCreateKeyExW',\
        'RegCreateKeyW' ,'RegDeleteKeyA' ,'RegDeleteKeyW' ,'RegDeleteValueA' ,'RegDeleteValueW' ,'RegDisablePredefinedCache' ,\
        'RegDisablePredefinedCacheEx' ,'RegEnumKeyA' ,'RegEnumKeyExA' ,'RegEnumKeyExW' ,'RegEnumKeyW' ,'RegEnumValueA' ,\
        'RegEnumValueW' ,'RegFlushKey' ,'RegGetKeySecurity' ,'RegLoadKeyA' ,'RegLoadKeyW' ,'RegNotifyChangeKeyValue' ,\
        'RegOpenCurrentUser' ,'RegOpenKeyA' ,'RegOpenKeyExA' ,'RegOpenKeyExW' ,'RegOpenKeyW' ,'RegOpenUserClassesRoot' ,\
        'RegOverridePredefKey' ,'RegQueryInfoKeyA' ,'RegQueryInfoKeyW' ,'RegQueryMultipleValuesA' ,'RegQueryMultipleValuesW' ,\
        'RegQueryValueA' ,'RegQueryValueExA' ,'RegQueryValueExW' ,'RegQueryValueW' ,'RegReplaceKeyA' ,'RegReplaceKeyW' ,\
        'RegRestoreKeyA' ,'RegRestoreKeyW' ,'RegSaveKeyA' ,'RegSaveKeyExA' ,'RegSaveKeyExW' ,'RegSaveKeyW' ,'RegSetKeySecurity' ,\
        'RegSetValueA' ,'RegSetValueExA' ,'RegSetValueExW' ,'RegSetValueW' ,'RegUnLoadKeyA' ,'RegUnLoadKeyW', 'SHDeleteEmptyKeyA' ,\
        'SHDeleteEmptyKeyW' ,'SHDeleteKeyA' ,'SHDeleteKeyW' ,'SHOpenRegStream2A' ,'SHOpenRegStream2W' ,'SHOpenRegStreamA' ,\
        'SHOpenRegStreamW' ,'SHQueryInfoKeyA' ,'SHQueryInfoKeyW' ,'SHQueryValueExA' ,'SHQueryValueExW' ,'SHRegCloseUSKey' ,\
        'SHRegCreateUSKeyA' ,'SHRegCreateUSKeyW' ,'SHRegDeleteEmptyUSKeyA' ,'SHRegDeleteEmptyUSKeyW' ,'SHRegDeleteUSValueA' ,\
        'SHRegDeleteUSValueW' ,'SHRegDuplicateHKey' ,'SHRegEnumUSKeyA' ,'SHRegEnumUSKeyW' ,'SHRegEnumUSValueA' ,'SHRegEnumUSValueW'\
        ,'SHRegGetBoolUSValueA' ,'SHRegGetBoolUSValueW' ,'SHRegGetPathA' ,'SHRegGetPathW' ,'SHRegGetUSValueA' ,'SHRegGetUSValueW' ,\
        'SHRegGetValueA' ,'SHRegGetValueW' ,'SHRegOpenUSKeyA' ,'SHRegOpenUSKeyW' ,'SHRegQueryInfoUSKeyA' ,'SHRegQueryInfoUSKeyW' ,\
        'SHRegQueryUSValueA' ,'SHRegQueryUSValueW' ,'SHRegSetPathA' ,'SHRegSetPathW' ,'SHRegSetUSValueA' ,'SHRegSetUSValueW' ,\
        'SHRegWriteUSValueA' ,'SHRegWriteUSValueW' ,'SHDeleteOrphanKeyA' ,'SHDeleteOrphanKeyW' ,'SHDeleteValueA' ,'SHDeleteValueW' ,\
        'SHEnumKeyExA' ,'SHEnumKeyExW' ,'SHEnumValueA' ,'SHEnumValueW' ,'SHGetValueA' ,'SHGetValueW' ,'SHOpenRegStream2A' ,\
        'SHOpenRegStream2W' ,'SHOpenRegStreamA' ,'SHOpenRegStreamW' ,'SHQueryInfoKeyA' ,'SHQueryInfoKeyW' ,'SHQueryValueExA' ,\
        'SHQueryValueExW' ,'SHRegCloseUSKey' ,'SHRegCreateUSKeyA' ,'SHRegCreateUSKeyW' ,'SHRegDeleteEmptyUSKeyA' ,\
        'SHRegDeleteEmptyUSKeyW' ,'SHRegDeleteUSValueA' ,'SHRegDeleteUSValueW' ,'SHRegDuplicateHKey' ,'SHRegEnumUSKeyA' ,\
        'SHRegEnumUSKeyW' ,'SHRegEnumUSValueA' ,'SHRegEnumUSValueW' ,'SHRegGetBoolUSValueA' ,'SHRegGetBoolUSValueW' ,'SHRegGetPathA' ,\
        'SHRegGetPathW' ,'SHRegGetUSValueA' ,'SHRegGetUSValueW' ,'SHRegGetValueA' ,'SHRegGetValueW' ,'SHRegOpenUSKeyA' ,'SHRegOpenUSKeyW' ,\
        'SHRegQueryInfoUSKeyA' ,'SHRegQueryInfoUSKeyW' ,'SHRegQueryUSValueA' ,'SHRegQueryUSValueW' ,'SHRegSetPathA' ,'SHRegSetPathW' ,\
        'SHRegSetUSValueA' ,'SHRegSetUSValueW' ,'SHRegWriteUSValueA' ,'SHRegWriteUSValueW']
winsock = [ 'NET', 'FreeAddrInfoW', 'GetAddrInfoW', 'GetNameInfoW', 'WEP', 'WPUCompleteOverlappedRequest', 'WSAAccept', \
            'WSAAddressToStringA', 'WSAAddressToStringW', 'WSAAsyncGetHostByAddr', 'WSAAsyncGetHostByName', 'WSAAsyncGetProtoByName',\
            'WSAAsyncGetProtoByNumber', 'WSAAsyncGetServByName', 'WSAAsyncGetServByPort', 'WSAAsyncSelect', 'WSACancelAsyncRequest',\
            'WSACancelBlockingCall', 'WSACleanup', 'WSACloseEvent', 'WSAConnect', 'WSACreateEvent', 'WSADuplicateSocketA',\
            'WSADuplicateSocketW', 'WSAEnumNameSpaceProvidersA', 'WSAEnumNameSpaceProvidersW', 'WSAEnumNetworkEvents', 'WSAEnumProtocolsA',\
            'WSAEnumProtocolsW', 'WSAEventSelect', 'WSAGetLastError', 'WSAGetOverlappedResult', 'WSAGetQOSByName', \
            'WSAGetServiceClassInfoA', 'WSAGetServiceClassInfoW', 'WSAGetServiceClassNameByClassIdA', 'WSAGetServiceClassNameByClassIdW',\
            'WSAHtonl', 'WSAHtons', 'WSAInstallServiceClassA', 'WSAInstallServiceClassW', 'WSAIoctl', 'WSAIsBlocking', 'WSAJoinLeaf', \
            'WSALookupServiceBeginA', 'WSALookupServiceBeginW', 'WSALookupServiceEnd', 'WSALookupServiceNextA', 'WSALookupServiceNextW', \
            'WSANSPIoctl', 'WSANtohl', 'WSANtohs', 'WSAProviderConfigChange', 'WSARecv', 'WSARecvDisconnect', 'WSARecvFrom', \
            'WSARemoveServiceClass', 'WSAResetEvent', 'WSASend', 'WSASendDisconnect', 'WSASendTo', 'WSASetBlockingHook', 'WSASetEvent',\
            'WSASetLastError', 'WSASetServiceA', 'WSASetServiceW', 'WSASocketA', 'WSASocketW', 'WSAStartup', 'WSAStringToAddressA', \
            'WSAStringToAddressW', 'WSAUnhookBlockingHook', 'WSAWaitForMultipleEvents', 'WSApSetPostRoutine', 'WSCDeinstallProvider', \
            'WSCEnableNSProvider', 'WSCEnumProtocols', 'WSCGetProviderPath', 'WSCInstallNameSpace', 'WSCInstallProvider', 'WSCUnInstallNameSpace',\
            'WSCUpdateProvider', 'WSCWriteNameSpaceOrder', 'WSCWriteProviderOrder', '__WSAFDIsSet', 'accept', 'bind', 'closesocket', 'connect', \
            'freeaddrinfo', 'getaddrinfo', 'gethostbyaddr', 'gethostbyname', 'gethostname', 'getnameinfo', 'getpeername', 'getprotobyname', \
            'getprotobynumber', 'getservbyname', 'getservbyport', 'getsockname', 'getsockopt', 'htonl', 'htons', 'inet_addr', 'inet_ntoa', \
            'ioctlsocket', 'listen', 'ntohl', 'ntohs', 'recv', 'recvfrom', 'select', 'send', 'sendto', 'setsockopt', 'shutdown', 'socket']
WinINet = [ 'NET', 'CreateMD5SSOHash', 'DetectAutoProxyUrl', 'DllInstall', 'ForceNexusLookup', 'ForceNexusLookupExW', 'InternetAlgIdToStringA',\
            'InternetAlgIdToStringW', 'InternetAttemptConnect', 'InternetAutodial', 'InternetAutodialCallback', 'InternetAutodialHangup',\
            'InternetCanonicalizeUrlA', 'InternetCanonicalizeUrlW', 'InternetCheckConnectionA', 'InternetCheckConnectionW', \
            'InternetClearAllPerSiteCookieDecisions', 'InternetCloseHandle', 'InternetCombineUrlA', 'InternetCombineUrlW', \
            'InternetConfirmZoneCrossing', 'InternetConfirmZoneCrossingA', 'InternetConfirmZoneCrossingW', 'InternetConnectA',\
            'InternetConnectW', 'InternetCrackUrlA', 'InternetCrackUrlW', 'InternetCreateUrlA', 'InternetCreateUrlW', 'InternetDial',\
            'InternetDialA', 'InternetDialW', 'InternetEnumPerSiteCookieDecisionA', 'InternetEnumPerSiteCookieDecisionW', 'InternetErrorDlg',\
            'InternetFindNextFileA', 'InternetFindNextFileW', 'InternetFortezzaCommand', 'InternetGetCertByURL', 'InternetGetCertByURLA',\
            'InternetGetConnectedState', 'InternetGetConnectedStateEx', 'InternetGetConnectedStateExA', 'InternetGetConnectedStateExW',\
            'InternetGetCookieA', 'InternetGetCookieExA', 'InternetGetCookieExW', 'InternetGetCookieW', 'InternetGetLastResponseInfoA', \
            'InternetGetLastResponseInfoW', 'InternetGetPerSiteCookieDecisionA', 'InternetGetPerSiteCookieDecisionW', 'InternetGoOnline',\
            'InternetGoOnlineA', 'InternetGoOnlineW', 'InternetHangUp', 'InternetInitializeAutoProxyDll', 'InternetLockRequestFile',\
            'InternetOpenA', 'InternetOpenUrlA', 'InternetOpenUrlW', 'InternetOpenW', 'InternetQueryDataAvailable', 'InternetQueryFortezzaStatus',\
            'InternetQueryOptionA', 'InternetQueryOptionW', 'InternetReadFile', 'InternetReadFileExA', 'InternetReadFileExW', \
            'InternetSecurityProtocolToStringA', 'InternetSecurityProtocolToStringW', 'InternetSetCookieA', 'InternetSetCookieExA', \
            'InternetSetCookieExW', 'InternetSetCookieW', 'InternetSetDialState', 'InternetSetDialStateA', 'InternetSetDialStateW',\
            'InternetSetFilePointer', 'InternetSetOptionA', 'InternetSetOptionExA', 'InternetSetOptionExW', 'InternetSetOptionW', \
            'InternetSetPerSiteCookieDecisionA', 'InternetSetPerSiteCookieDecisionW', 'InternetSetStatusCallback', 'InternetSetStatusCallbackA',\
            'InternetSetStatusCallbackW', 'InternetShowSecurityInfoByURL', 'InternetShowSecurityInfoByURLA', 'InternetShowSecurityInfoByURLW', \
            'InternetTimeFromSystemTime', 'InternetTimeFromSystemTimeA', 'InternetTimeFromSystemTimeW', 'InternetTimeToSystemTime',\
            'InternetTimeToSystemTimeA', 'InternetTimeToSystemTimeW', 'InternetUnlockRequestFile', 'InternetWriteFile', 'InternetWriteFileExA',\
            'InternetWriteFileExW', 'IsHostInProxyBypassList', 'ParseX509EncodedCertificateForListBoxEntry', 'PrivacyGetZonePreferenceW', \
            'PrivacySetZonePreferenceW', 'ResumeSuspendedDownload', 'ShowCertificate', 'ShowClientAuthCerts', 'ShowSecurityInfo', \
            'ShowX509EncodedCertificate','UrlZonesDetach', '_GetFileExtensionFromUrl'] 
cache = [ 'NET','CommitUrlCacheEntryA', 'CommitUrlCacheEntryW', 'CreateUrlCacheContainerA', 'CreateUrlCacheContainerW', 'CreateUrlCacheEntryA',\
          'CreateUrlCacheEntryW', 'CreateUrlCacheGroup', 'DeleteIE3Cache', 'DeleteUrlCacheContainerA', 'DeleteUrlCacheContainerW', \
          'DeleteUrlCacheEntry', 'DeleteUrlCacheEntryA', 'DeleteUrlCacheEntryW', 'DeleteUrlCacheGroup', 'FindCloseUrlCache', 'FindFirstUrlCacheContainerA',\
          'FindFirstUrlCacheContainerW', 'FindFirstUrlCacheEntryA', 'FindFirstUrlCacheEntryExA', 'FindFirstUrlCacheEntryExW', 'FindFirstUrlCacheEntryW', \
          'FindFirstUrlCacheGroup', 'FindNextUrlCacheContainerA', 'FindNextUrlCacheContainerW', 'FindNextUrlCacheEntryA', 'FindNextUrlCacheEntryExA',\
          'FindNextUrlCacheEntryExW', 'FindNextUrlCacheEntryW', 'FindNextUrlCacheGroup', 'FreeUrlCacheSpaceA', 'FreeUrlCacheSpaceW', 'GetUrlCacheConfigInfoA', \
          'GetUrlCacheConfigInfoW', 'GetUrlCacheEntryInfoA', 'GetUrlCacheEntryInfoExA', 'GetUrlCacheEntryInfoExW', 'GetUrlCacheEntryInfoW', \
          'GetUrlCacheGroupAttributeA', 'GetUrlCacheGroupAttributeW', 'GetUrlCacheHeaderData', 'IncrementUrlCacheHeaderData', 'IsUrlCacheEntryExpiredA',\
          'IsUrlCacheEntryExpiredW', 'LoadUrlCacheContent', 'ReadUrlCacheEntryStream', 'RegisterUrlCacheNotification', 'RetrieveUrlCacheEntryFileA', \
          'RetrieveUrlCacheEntryFileW', 'RetrieveUrlCacheEntryStreamA', 'RetrieveUrlCacheEntryStreamW', 'RunOnceUrlCache', 'SetUrlCacheConfigInfoA',\
          'SetUrlCacheConfigInfoW', 'SetUrlCacheEntryGroup', 'SetUrlCacheEntryGroupA', 'SetUrlCacheEntryGroupW', 'SetUrlCacheEntryInfoA', 'SetUrlCacheEntryInfoW',\
          'SetUrlCacheGroupAttributeA', 'SetUrlCacheGroupAttributeW', 'SetUrlCacheHeaderData', 'UnlockUrlCacheEntryFile', 'UnlockUrlCacheEntryFileA', \
          'UnlockUrlCacheEntryFileW', 'UnlockUrlCacheEntryStream', 'UpdateUrlCacheContentPath']
ftp = [ 'FTP','FtpCommandA' ,'FtpCommandW' ,'FtpCreateDirectoryA' ,'FtpCreateDirectoryW' ,'FtpDeleteFileA' ,'FtpDeleteFileW' ,'FtpFindFirstFileA' ,\
        'FtpFindFirstFileW' ,'FtpGetCurrentDirectoryA' ,'FtpGetCurrentDirectoryW' ,'FtpGetFileA' ,'FtpGetFileEx' ,'FtpGetFileSize' ,'FtpGetFileW' ,\
        'FtpOpenFileA' ,'FtpOpenFileW' ,'FtpPutFileA' ,'FtpPutFileEx' ,'FtpPutFileW' ,'FtpRemoveDirectoryA' ,'FtpRemoveDirectoryW' ,'FtpRenameFileA' ,\
        'FtpRenameFileW' ,'FtpSetCurrentDirectoryA' ,'FtpSetCurrentDirectoryW']
gopher = [ 'GPR', 'GopherCreateLocatorA', 'GopherCreateLocatorW', 'GopherFindFirstFileA', 'GopherFindFirstFileW', 'GopherGetAttributeA', \
           'GopherGetAttributeW', 'GopherGetLocatorTypeA', 'GopherGetLocatorTypeW', 'GopherOpenFileA', 'GopherOpenFileW'] 
url = ['URL', 'UrlApplySchemeA' ,'UrlApplySchemeW' ,'UrlCanonicalizeA' ,'UrlCanonicalizeW' ,'UrlCombineA' ,'UrlCombineW' ,'UrlCompareA' ,\
       'UrlCompareW' ,'UrlCreateFromPathA' ,'UrlCreateFromPathW' ,'UrlEscapeA' ,'UrlEscapeW' ,'UrlGetLocationA' ,'UrlGetLocationW' ,'UrlGetPartA'\
       ,'UrlGetPartW' ,'UrlHashA' ,'UrlHashW' ,'UrlIsA' ,'UrlIsNoHistoryA' ,'UrlIsNoHistoryW' ,'UrlIsOpaqueA' ,'UrlIsOpaqueW' ,'UrlIsW' ,'UrlUnescapeA' ,'UrlUnescapeW']
dir = ['DIR','CreateDirectoryA', 'CreateDirectoryExA', 'CreateDirectoryExW', 'CreateDirectoryW', 'GetCurrentDirectoryA', 'GetCurrentDirectoryW',\
       'GetDllDirectoryA', 'GetDllDirectoryW', 'GetSystemDirectoryA', 'GetSystemDirectoryW', 'GetSystemWindowsDirectoryA', 'GetSystemWindowsDirectoryW',\
       'GetSystemWow64DirectoryA', 'GetSystemWow64DirectoryW', 'GetVDMCurrentDirectories', 'GetWindowsDirectoryA', 'GetWindowsDirectoryW', \
       'ReadDirectoryChangesW', 'RemoveDirectoryA', 'RemoveDirectoryW', 'SetCurrentDirectoryA', 'SetCurrentDirectoryW', 'SetDllDirectoryA',\
       'SetDllDirectoryW', 'SetVDMCurrentDirectories', 'SHCreateDirectory', 'SHCreateDirectoryExA', 'SHCreateDirectoryExW']
mutex = ['MTX','CreateMutexA', 'CreateMutexW', 'OpenMutexA', 'OpenMutexW', 'ReleaseMutex']
pipe = [ 'PIP', 'CallNamedPipeA', 'CallNamedPipeW', 'ConnectNamedPipe', 'CreateNamedPipeA', 'CreateNamedPipeW', 'CreatePipe', 'DisconnectNamedPipe',\
         'GetNamedPipeHandleStateA', 'GetNamedPipeHandleStateW', 'GetNamedPipeInfo', 'PeekNamedPipe', 'SetNamedPipeHandleState', 'TransactNamedPipe',\
         'WaitNamedPipeA', 'WaitNamedPipeW']
http = [ 'HTP', 'HttpAddRequestHeadersA', 'HttpAddRequestHeadersW', 'HttpCheckDavCompliance', 'HttpEndRequestA', 'HttpEndRequestW',\
         'HttpOpenRequestA', 'HttpOpenRequestW', 'HttpQueryInfoA', 'HttpQueryInfoW', 'HttpSendRequestA', 'HttpSendRequestExA', \
         'HttpSendRequestExW', 'HttpSendRequestW' ] 
enum = [ 'ENP', 'CreateToolhelp32Snapshot', 'Process32First' ,'Process32FirstW' ,'Process32Next' ,'Process32NextW']
hash = ['HAS', 'CryptCreateHash' ,'CryptDestroyHash' ,'CryptDuplicateHash' ,'CryptGetHashParam' ,'CryptHashData' ,'CryptHashSessionKey' ,\
        'CryptSetHashParam' ,'CryptSignHashA' ,'CryptSignHashW', 'FreeEncryptionCertificateHashList']
crypt = ['CRY', 'CryptAcquireContextA' ,'CryptAcquireContextW' ,'CryptContextAddRef' ,'CryptDecrypt' ,'CryptDeriveKey' ,'CryptDestroyKey' ,\
         'CryptDuplicateKey' ,'CryptEncrypt' ,'CryptEnumProviderTypesA' ,'CryptEnumProviderTypesW' ,'CryptEnumProvidersA' ,'CryptEnumProvidersW'\
         ,'CryptExportKey' ,'CryptGenKey' ,'CryptGenRandom' ,'CryptGetDefaultProviderA' ,'CryptGetDefaultProviderW' ,'CryptGetKeyParam' ,\
         'CryptGetProvParam' ,'CryptGetUserKey' ,'CryptImportKey' ,'CryptReleaseContext' ,'CryptSetKeyParam' ,'CryptSetProvParam' ,\
         'CryptSetProviderA' ,'CryptSetProviderExA' ,'CryptSetProviderExW' ,'CryptSetProviderW' ,'CryptVerifySignatureA' ,'CryptVerifySignatureW' ,\
         'DecryptFileA' ,'DecryptFileW', 'EncryptFileA' ,'EncryptFileW' ,'EncryptedFileKeyInfo' ,'EncryptionDisable', 'WriteEncryptedFileRaw', \
         'OpenEncryptedFileRawA' ,'OpenEncryptedFileRawW', 'DuplicateEncryptionInfoFile', 'SetUserFileEncryptionKey', 'ReadEncryptedFileRaw', \
         'RemoveUsersFromEncryptedFile', 'FileEncryptionStatusA', 'FileEncryptionStatusW', 'FreeEncryptedFileKeyInfo', 'CloseEncryptedFileRaw', \
         'AddUsersToEncryptedFile', 'QueryRecoveryAgentsOnEncryptedFile', 'QueryUsersOnEncryptedFile', 'ChainWlxLogoffEvent' ,'CryptAcquireContextU' ,\
         'CryptBinaryToStringA' ,'CryptBinaryToStringW' ,'CryptCloseAsyncHandle' ,'CryptCreateAsyncHandle' ,'CryptDecodeMessage' ,'CryptDecodeObject' ,\
         'CryptDecodeObjectEx' ,'CryptDecryptAndVerifyMessageSignature' ,'CryptDecryptMessage' ,'CryptEncodeObject' ,'CryptEncodeObjectEx' ,\
         'CryptEncryptMessage' ,'CryptEnumKeyIdentifierProperties' ,'CryptEnumOIDFunction' ,'CryptEnumOIDInfo' ,'CryptEnumProvidersU' ,'CryptExportPKCS8' ,\
         'CryptExportPublicKeyInfo' ,'CryptExportPublicKeyInfoEx' ,'CryptFindLocalizedName' ,'CryptFindOIDInfo' ,'CryptFormatObject' ,\
         'CryptFreeOIDFunctionAddress' ,'CryptGetAsyncParam' ,'CryptGetDefaultOIDDllList' ,'CryptGetDefaultOIDFunctionAddress' ,\
         'CryptGetKeyIdentifierProperty' ,'CryptGetMessageCertificates' ,'CryptGetMessageSignerCount' ,'CryptGetOIDFunctionAddress' ,\
         'CryptGetOIDFunctionValue' ,'CryptHashCertificate' ,'CryptHashMessage' ,'CryptHashPublicKeyInfo' ,'CryptHashToBeSigned' ,\
         'CryptImportPKCS8' ,'CryptImportPublicKeyInfo' ,'CryptImportPublicKeyInfoEx' ,'CryptInitOIDFunctionSet' ,'CryptInstallDefaultContext' ,\
         'CryptInstallOIDFunctionAddress' ,'CryptLoadSip' ,'CryptMemAlloc' ,'CryptMemFree' ,'CryptMemRealloc' ,'CryptMsgCalculateEncodedLength' ,\
         'CryptMsgClose' ,'CryptMsgControl' ,'CryptMsgCountersign' ,'CryptMsgCountersignEncoded' ,'CryptMsgDuplicate' ,'CryptMsgEncodeAndSignCTL' ,\
         'CryptMsgGetAndVerifySigner' ,'CryptMsgGetParam' ,'CryptMsgOpenToDecode' ,'CryptMsgOpenToEncode' ,'CryptMsgSignCTL' ,'CryptMsgUpdate' ,\
         'CryptMsgVerifyCountersignatureEncoded' ,'CryptMsgVerifyCountersignatureEncodedEx' ,'CryptProtectData' ,'CryptQueryObject' ,\
         'CryptRegisterDefaultOIDFunction' ,'CryptRegisterOIDFunction' ,'CryptRegisterOIDInfo' ,'CryptSIPAddProvider' ,\
         'CryptSIPCreateIndirectData' ,'CryptSIPGetSignedDataMsg' ,'CryptSIPLoad' ,'CryptSIPPutSignedDataMsg' ,'CryptSIPRemoveProvider' ,\
         'CryptSIPRemoveSignedDataMsg' ,'CryptSIPRetrieveSubjectGuid' ,'CryptSIPRetrieveSubjectGuidForCatalogFile' ,'CryptSIPVerifyIndirectData' ,\
         'CryptSetAsyncParam' ,'CryptSetKeyIdentifierProperty' ,'CryptSetOIDFunctionValue' ,'CryptSetProviderU' ,'CryptSignAndEncodeCertificate' ,\
         'CryptSignAndEncryptMessage' ,'CryptSignCertificate' ,'CryptSignHashU' ,'CryptSignMessage' ,'CryptSignMessageWithKey' ,\
         'CryptStringToBinaryA' ,'CryptStringToBinaryW' ,'CryptUninstallDefaultContext' ,'CryptUnprotectData' ,'CryptUnregisterDefaultOIDFunction' ,\
         'CryptUnregisterOIDFunction' ,'CryptUnregisterOIDInfo' ,'CryptVerifyCertificateSignature' ,'CryptVerifyCertificateSignatureEx' ,\
         'CryptVerifyDetachedMessageHash' ,'CryptVerifyDetachedMessageSignature' ,'CryptVerifyMessageHash' ,'CryptVerifyMessageSignature' ,\
         'CryptVerifyMessageSignatureWithKey' ,'CryptVerifySignatureU' ,'I_CertProtectFunction' ,'I_CertSrvProtectFunction' ,'I_CertSyncStore' ,\
         'I_CertUpdateStore' ,'I_CryptAddRefLruEntry' ,'I_CryptAddSmartCardCertToStore' ,'I_CryptAllocTls' ,'I_CryptCreateLruCache' ,\
         'I_CryptCreateLruEntry' ,'I_CryptDetachTls' ,'I_CryptDisableLruOfEntries' ,'I_CryptEnableLruOfEntries' ,'I_CryptEnumMatchingLruEntries' ,\
         'I_CryptFindLruEntry' ,'I_CryptFindLruEntryData' ,'I_CryptFindSmartCardCertInStore' ,'I_CryptFlushLruCache' ,'I_CryptFreeLruCache' ,\
         'I_CryptFreeTls' ,'I_CryptGetAsn1Decoder' ,'I_CryptGetAsn1Encoder' ,'I_CryptGetDefaultCryptProv' ,'I_CryptGetDefaultCryptProvForEncrypt' ,\
         'I_CryptGetFileVersion' ,'I_CryptGetLruEntryData' ,'I_CryptGetLruEntryIdentifier' ,'I_CryptGetOssGlobal' ,'I_CryptGetTls' ,'I_CryptInsertLruEntry' ,\
         'I_CryptInstallAsn1Module' ,'I_CryptInstallOssGlobal' ,'I_CryptReadTrustedPublisherDWORDValueFromRegistry' ,'I_CryptRegisterSmartCardStore' ,\
         'I_CryptReleaseLruEntry' ,'I_CryptRemoveLruEntry' ,'I_CryptSetTls' ,'I_CryptTouchLruEntry' ,'I_CryptUninstallAsn1Module' ,\
         'I_CryptUninstallOssGlobal' ,'I_CryptUnregisterSmartCardStore' ,'I_CryptWalkAllLruCacheEntries']
service = ['SRV', 'ChangeServiceConfig2A' ,'ChangeServiceConfig2W' ,'ChangeServiceConfigA' ,'ChangeServiceConfigW' ,'CloseServiceHandle' ,\
           'ControlService' ,'CreateServiceA' ,'CreateServiceW' ,'DeleteService' ,'EnumDependentServicesA' ,'EnumDependentServicesW' ,\
           'EnumServiceGroupW' ,'EnumServicesStatusA' ,'EnumServicesStatusExA' ,'EnumServicesStatusExW' ,'EnumServicesStatusW' ,\
           'GetServiceDisplayNameA' ,'GetServiceDisplayNameW' ,'GetServiceKeyNameA' ,'GetServiceKeyNameW' ,'I_ScPnPGetServiceName' ,\
           'I_ScSetServiceBitsA' ,'I_ScSetServiceBitsW' ,'LockServiceDatabase' ,'OpenServiceA' ,'OpenServiceW' ,'PrivilegedServiceAuditAlarmA' ,\
           'PrivilegedServiceAuditAlarmW' ,'QueryServiceConfig2A' ,'QueryServiceConfig2W' ,'QueryServiceConfigA' ,'QueryServiceConfigW' ,\
           'QueryServiceLockStatusA' ,'QueryServiceLockStatusW' ,'QueryServiceObjectSecurity' ,'QueryServiceStatus' ,'QueryServiceStatusEx' ,\
           'RegisterServiceCtrlHandlerA' ,'RegisterServiceCtrlHandlerExA' ,'RegisterServiceCtrlHandlerExW' ,'RegisterServiceCtrlHandlerW' ,\
           'SetServiceBits' ,'SetServiceObjectSecurity' ,'SetServiceStatus' ,'StartServiceA' ,'StartServiceCtrlDispatcherA' ,'StartServiceCtrlDispatcherW' ,\
           'StartServiceW' ,'UnlockServiceDatabase' ,'WdmWmiServiceMain']
file = ['FIL', 'CompareFileTime' ,'CopyFileA' ,'CopyFileExA' ,'CopyFileExW' ,'CopyFileW' ,'CopyLZFile' ,'CreateFileA' ,'CreateFileMappingA' ,\
        'CreateFileMappingW' ,'CreateFileW' ,'DeleteFileA' ,'DeleteFileW' ,'DosDateTimeToFileTime' ,'FileTimeToDosDateTime' ,\
        'FileTimeToLocalFileTime' ,'FileTimeToLocalFileTime' ,'FileTimeToSystemTime' ,'FlushFileBuffers' ,'FlushViewOfFile' ,\
        'GetCPFileNameFromRegistry' ,'GetCompressedFileSizeA' ,'GetCompressedFileSizeW' ,'GetFileAttributesA' ,'GetFileAttributesExA' ,\
        'GetFileAttributesExW' ,'GetFileAttributesW' ,'GetFileInformationByHandle' ,'GetFileSize' ,'GetFileSizeEx' ,'GetFileTime' ,\
        'GetFileType' ,'GetSystemTimeAsFileTime' ,'GetTempFileNameA' ,'GetTempFileNameW' ,'LZCloseFile' ,'LZCreateFileW' ,'LZOpenFileA',\
        'LZOpenFileW' ,'LocalFileTimeToFileTime' ,'LocalFileTimeToFileTime' ,'LockFile' ,'LockFileEx' ,'MapViewOfFile' ,'MapViewOfFileEx' ,\
        'MoveFileA' ,'MoveFileExA' ,'MoveFileExW' ,'MoveFileW' ,'MoveFileWithProgressA' ,'MoveFileWithProgressW' ,'OpenDataFile' ,'OpenFile' ,\
        'OpenFileMappingA' ,'OpenFileMappingW' ,'OpenProfileUserMapping' ,'PrivCopyFileExW' ,'PrivMoveFileIdentityW' ,'ReadFile' ,'ReadFileEx' ,\
        'ReplaceFile' ,'ReplaceFileA' ,'ReplaceFileW' ,'SetEndOfFile' ,'SetFileAttributesA' ,'SetFileAttributesW' ,'SetFilePointer' ,\
        'SetFilePointerEx' ,'SetFileShortNameA' ,'SetFileShortNameW' ,'SetFileTime' ,'SetFileValidData' ,'SystemTimeToFileTime' ,\
        'UnlockFile' ,'UnlockFileEx' ,'UnmapViewOfFile' ,'WriteFile' ,'WriteFileEx' ,'WriteFileGather' ,'GetFileSecurityA' ,\
        'GetFileSecurityW' ,'SetFileSecurityA' ,'SetFileSecurityW', 'CreateFileU']
os_info = [ 'OSI', 'GetComputerNameA' ,'GetComputerNameExA' ,'GetComputerNameExW' ,'GetComputerNameW' ,'GetDiskFreeSpaceA' ,\
            'GetDiskFreeSpaceExA' ,'GetDiskFreeSpaceExW' ,'GetDiskFreeSpaceW' ,'GetDriveTypeA' ,'GetDriveTypeW', 'GetVersion' ,\
            'GetVersionExA' ,'GetVersionExW', 'GetSystemInfo', 'GetSystemMetrics', 'CheckTokenMembership']
cert = ['CER','CertAddCRLContextToStore' ,'CertAddCRLLinkToStore' ,'CertAddCTLContextToStore' ,'CertAddCTLLinkToStore' ,\
        'CertAddCertificateContextToStore' ,'CertAddCertificateLinkToStore' ,'CertAddEncodedCRLToStore' ,'CertAddEncodedCertificateToStore' ,\
        'CertAddEncodedCertificateToSystemStoreA' ,'CertAddEncodedCertificateToSystemStoreW' ,'CertAddEnhancedKeyUsageIdentifier' ,\
        'CertAddSerializedElementToStore' ,'CertAddStoreToCollection' ,'CertAlgIdToOID' ,'CertCloseStore' ,'CertCompareCertificate' ,\
        'CertCompareCertificateName' ,'CertCompareIntegerBlob' ,'CertComparePublicKeyInfo' ,'CertControlStore' ,'CertCreateCTLContext' ,\
        'CertCreateCTLEntryFromCertificateContextProperties' ,'CertCreateCertificateChainEngine' ,'CertCreateCertificateContext' ,'CertCreateContext',\
        'CertCreateSelfSignCertificate' ,'CertDeleteCTLFromStore' ,'CertDeleteCertificateFromStore' ,'CertDuplicateCTLContext' ,\
        'CertDuplicateCertificateChain' ,'CertDuplicateCertificateContext' ,'CertDuplicateStore' ,'CertEnumCRLContextProperties' ,\
        'CertEnumCRLsInStore' ,'CertEnumCTLContextProperties' ,'CertEnumCTLsInStore' ,'CertEnumCertificateContextProperties' ,\
        'CertEnumCertificatesInStore' ,'CertEnumPhysicalStore' ,'CertEnumSubjectInSortedCTL' ,'CertEnumSystemStore' ,\
        'CertEnumSystemStoreLocation' ,'CertFindAttribute' ,'CertFindCRLInStore' ,'CertFindCertificateInCRL' ,'CertFindCertificateInStore',\
        'CertFindChainInStore' ,'CertFindExtension' ,'CertFindRDNAttr' ,'CertFindSubjectInCTL' ,'CertFindSubjectInSortedCTL' ,\
        'CertFreeCRLContext' ,'CertFreeCertificateChain' ,'CertFreeCertificateChainEngine' ,'CertFreeCertificateContext' ,'CertGetCRLContextProperty' ,\
        'CertGetCRLFromStore' ,'CertGetCTLContextProperty' ,'CertGetCertificateChain' ,'CertGetCertificateContextProperty' ,'CertGetEnhancedKeyUsage' ,\
        'CertGetIssuerCertificateFromStore' ,'CertGetNameStringA' ,'CertGetNameStringW' ,'CertGetPublicKeyLength' ,'CertGetStoreProperty' ,\
        'CertGetSubjectCertificateFromStore' ,'CertGetValidUsages' ,'CertIsRDNAttrsInCertificateName' ,'CertIsValidCRLForCertificate' ,\
        'CertNameToStrA' ,'CertNameToStrW' ,'CertOIDToAlgId' ,'CertOpenStore' ,'CertOpenSystemStoreA' ,'CertOpenSystemStoreW' ,'CertRDNValueToStrA',\
        'CertRDNValueToStrW' ,'CertRegisterPhysicalStore' ,'CertRegisterSystemStore' ,'CertRemoveEnhancedKeyUsageIdentifier' ,\
        'CertRemoveStoreFromCollection' ,'CertResyncCertificateChainEngine' ,'CertSaveStore' ,'CertSerializeCRLStoreElement' ,\
        'CertSerializeCertificateStoreElement' ,'CertSetCRLContextProperty' ,'CertSetCertificateContextPropertiesFromCTLEntry' ,\
        'CertSetCertificateContextProperty' ,'CertSetEnhancedKeyUsage' ,'CertSetStoreProperty' ,'CertStrToNameA' ,'CertStrToNameW' ,\
        'CertUnregisterPhysicalStore' ,'CertUnregisterSystemStore' ,'CertVerifyCRLRevocation' ,'CertVerifyCRLTimeValidity' ,\
        'CertVerifyCTLUsage' ,'CertVerifyCertificateChainPolicy' ,'CertVerifyCertificateChainPolicy' ,'CertVerifyRevocation' ,\
        'CertVerifySubjectCertificateContext','CertVerifyTimeValidity' ,'CertVerifyValidityNesting' ,'CloseCertPerformanceData' ,\
        'CollectCertPerformanceData' ,'CryptAcquireCertificatePrivateKey' ,'CryptFindCertificateKeyProvInfo' ,'CryptGetMessageCertificates' ,\
        'CryptHashCertificate' ,'CryptSignAndEncodeCertificate' ,'CryptSignCertificate' ,'CryptVerifyCertificateSignature' ,\
        'CryptVerifyCertificateSignatureEx' ,'I_CertProtectFunction' ,'I_CertSrvProtectFunction' ,'I_CertSyncStore' ,'I_CertUpdateStore' ,\
        'I_CryptAddSmartCardCertToStore' ,'I_CryptFindSmartCardCertInStore' ,'OpenCertPerformanceData' ,'PFXExportCertStore' ,'PFXExportCertStoreEx' ,'PFXImportCertStore'] 
file_s = ['SRC', 'FindFirstFileW', 'FindNextFileW', 'FindClose']
modify = ['MOD', 'WriteProcessMemory', 'ReadProcessMemory'] 
virtual = ['VIR', 'VirtualAlloc' ,'VirtualAllocEx' ,'VirtualBufferExceptionHandler' ,'VirtualFree' ,'VirtualFreeEx' ,'VirtualLock' ,
           'VirtualProtect' ,'VirtualProtectEx' ,'VirtualQuery' ,'VirtualQueryEx' ,'VirtualUnlock']
critical_section = [ 'CRT', 'DeleteCriticalSection' ,'EnterCriticalSection' ,'InitializeCriticalSection' ,
                     'InitializeCriticalSectionAndSpinCount' ,'LeaveCriticalSection' ,'SetCriticalSectionSpinCount' ,'TryEnterCriticalSection']

api_matrix = [ reg, winsock, WinINet, cache, ftp, gopher, dir, mutex, pipe, http, enum, hash, crypt, service, file, cert, os_info, file_s, modify, virtual, critical_section,\
               launcher, process_injection, DLL_injection, direct_injection, process_replacement, hook_injection, APC_injection, APC_injection, APC_userspace, APC_kernelspace,\
               windows_networking, anti_debugging]

def getAllStrings():
    #We want to use a specific string configuration
    stringList = idautils.Strings(default_setup = False)
    # Lets use C et UNICODE string
    stringList.setup(strtypes=Strings.STR_C | Strings.STR_UNICODE, ignore_instructions = True, display_only_existing_strings = True)

    parsedStringList = []
    #Get all strings
    for string in stringList:                
        if string:
            parsedStringList.append((str(string), string.ea))

    return parsedStringList
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
IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH = ""
def configurationNeed():
    return ["IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH", "IDA_PRO_TEXT_EXTRACTOR_EXTRACTED_FILE"]
            
def configurationProvision(utilityConfig=[]):
    global IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH
    global IDA_PRO_TEXT_EXTRACTOR_EXTRACTED_FILE
    IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH = utilityConfig[0]
    IDA_PRO_TEXT_EXTRACTOR_EXTRACTED_FILE = utilityConfig[1]


def sanitize_name(name):
    name = name.strip()
    if name.endswith("A"):
        name = name[:-1]
    elif name.endswith("W"):
        name = name[:-1]
    while name.startswith("_"):
        name = name[1:]
    return name

def getFuncDeclaration(func):
    if func != idc.BADADDR:
        ft = idc.GetType(func)
        if ft:
            return ft
        else:
            #print "-Type info not available!"
            return ""
    else:
        return ""    
  
def prefix_lines(lines):
    if not lines or len(lines) == 0:
        return lines
    result = [RESULT_PREFIX+line for line in lines.splitlines()]
    return "\n".join(result)
    
def prefix_lines_oa(lines):
    if not lines or len(lines) == 0:
        return lines
    result = [RESULT_PREFIX_OA+line for line in lines.splitlines()]
    return "\n".join(result)
    
def remove_prefixed_lines(lines):
    if not lines or len(lines) == 0:
        return lines
    result = [line for line in lines.splitlines() \
              if not line.startswith(RESULT_PREFIX)]
    return "\n".join(result)
    
def remove_prefixed_lines_oa(lines):
    if not lines or len(lines) == 0:
        return lines
    result = [line for line in lines.splitlines() \
              if not line.startswith(RESULT_PREFIX_OA)]
    return "\n".join(result)

  
def get_all_function_eas():
    result = []
    for fnum in xrange(idaapi.get_func_qty()):
        func = idaapi.getn_func(fnum)
        f_ea = func.startEA
        if f_ea != idaapi.BADADDR:
            result.append(f_ea)
    return result
    
def get_import_segments():
    result = []
    for seg_ea in idautils.Segments():
        seg = idaapi.getseg(seg_ea)
        if seg.type == idaapi.SEG_XTRN:
            result.append( (seg.startEA, seg.endEA) )
    return result
    
def u2signed(num):
    if num < 0x80000000:
        return num
    else:
        return num - 0x100000000
    
class Function(object):
    def __init__(self, start_ea):
        self.start_ea = start_ea
        
    def get_end_address(self):
        return "0x%x" % idc.GetFunctionAttr(self.start_ea, idc.FUNCATTR_END)
    def get_number_of_instructions(self):
        icount = 0
        for i in idautils.FuncItems(self.start_ea): icount = icount + 1
        return icount
    def get_size_of_argument_bytes(self):
        try:
            fframe = idc.GetFrame(self.start_ea)
            if fframe is not None:
                fret = idc.GetMemberOffset(fframe, " r")
            if fret is not -1:
                firstArg = fret + 4
            args = idc.GetStrucSize(fframe) - firstArg
            return args
        except:
            pass     
            return
    def get_number_of_arguments(self):
        try:
            args = self.get_size_of_argument_bytes()
            out = args/4
        except:
            out = 0
            pass
        return out
    def get_size_of_local_variables(self):
        try:
            locals = idc.GetFunctionAttr(self.start_ea, idc.FUNCATTR_FRSIZE)
            return locals
        except:
            pass
            return
    def get_function_flags(self):
        try:
            return idc.GetFunctionFlags(self.start_ea)
        except:
            pass
            return
    def get_name(self):
        return idaapi.get_func_name(self.start_ea)
    def get_demangled_name(self):
        mangled = idaapi.get_func_name(self.start_ea)
        demangled = idc.Demangle(mangled, idc.GetLongPrm(idc.INF_SHORT_DN))
        #demangled = idc.Demangle(mangled, idc.GetLongPrm(INF_LONG_DN))
        if  demangled == None:
             return "" #mangled
        else:
            print " --Demangling..."
            return demangled
    def get_instruction_eas(self):
        result = []
        for chunk in self.__get_chunks():
            ins_ea = idc.FindCode(chunk.startEA-1, DIRECTION_FORW)
            while ins_ea <= chunk.endEA and ins_ea != idc.BADADDR:
                result.append(ins_ea)
                ins_ea = idc.FindCode(ins_ea, DIRECTION_FORW)
        return result    
    def get_instructions(self):
        return [Instruction(iea, ) for iea in self.get_instruction_eas()]
    def get_code_refs_from(self):
        result = []
        for iea in self.get_instruction_eas():
            inst = Instruction(iea, )
            result += inst.get_code_refs_from()
        return list(set(result))
    def get_data_refs_from(self):
        result = []
        for iea in self.get_instruction_eas():
            inst = Instruction(iea, )
            result += inst.get_data_refs_from()
        return list(set(result))
    def set_comment(self, comment, repeatable = False):
        func = self.__get_func_t()
        idaapi.set_func_cmt(func, comment, repeatable)
    def get_comment(self, repeatable = False):
        func = self.__get_func_t()
        return idaapi.get_func_cmt(func, repeatable)
    def __get_chunks(self):
        func = self.__get_func_t()
        result = [func]
        ft_iter = idaapi.func_tail_iterator_t(func, self.start_ea)
        if ft_iter.first():
            result.append(ft_iter.chunk())
        while ft_iter.next():
            result.append(ft_iter.chunk())
        return result
    def __get_func_t(self):
        result = idaapi.get_func(self.start_ea)
        if not result:
            raise RuntimeError, \
                  "Cannot retrieve function information @ address %s" % \
                  self.start_ea
        return result
    def __repr__(self):
        return self.get_name()

class Instruction(object):
    def __init__(self, inst_ea):
        self.iea = inst_ea
        
    def get_code_refs_from(self):
        return idautils.CodeRefsFrom(self.iea, False)
    def get_data_refs_from(self):
        return idautils.DataRefsFrom(self.iea, False)
    def get_operands(self):
        result = []
        ins = self.__get_insn_t()
        if not ins:
            print >> sys.stderr, \
                  "Cannot retrieve operand information @ address %s" % \
                  hex(self.iea)
            return result
        for i in xrange(6):
            oper = ins[i]
            if oper.type != idaapi.o_void:
                result.append( Operand(i, self.iea, ) )
        return result
    def __get_insn_t(self):
        ins = idautils.DecodeInstruction(self.iea)
        if ins:
	    return ins
        return None
    def __repr__(self):        
        return idaapi.tag_remove( idaapi.generate_disasm_line(self.iea) )
        
class Operand(object):
    def __init__(self, oper_num, inst_ea):
        self.onum = oper_num
        self.iea = inst_ea
        
        
    def get_immediate(self):
        oper = self.__get_op_t()
        if not oper or oper.type != idaapi.o_imm:
            return None        
        value = oper.value
        if value in idautils.DataRefsFrom(self.iea):
            return None
        return value
    def get_string(self):
        mem = self.get_memory_address()
        if not mem:
            return None
        flags = idaapi.getFlags(mem)
        if not idaapi.isASCII(flags):
            return None
        tinfo = idaapi.opinfo_t()
        idaapi.get_opinfo(mem, 0, flags, tinfo)
        slen = idaapi.get_max_ascii_length(mem, tinfo.strtype)
        return idaapi.get_ascii_contents2(mem, slen, tinfo.strtype)
        
    def get_symbolicName(self):
        #Check if constant:
        value = self.get_immediate()
        if value is None:
            return None
        
        #Now lets try to see if it uses symbolic names
        operandCounter = 0
        operandText = GetOpnd(self.iea, self.onum)
        if (operandText != ""):
                if operandText[-1] == "h":
                    operandTextTemp = operandText[:-1]
                try:
                    result = int(operandTextTemp, 16)
                    return None
                except:
                    return operandText
        #End of symbolic names chases...
        
    def get_memory_address(self):
        oper = self.__get_op_t()
        if oper.type == idaapi.o_mem:
            return oper.addr
        elif oper.type == idaapi.o_imm and self.iea != idc.BADADDR:
            ref = oper.value
            if ref in idautils.DataRefsFrom(self.iea):
                return ref
        elif (oper.type == idaapi.o_displ or oper.type == idaapi.o_phrase) \
                 and not self.is_stackref():
            return oper.addr
        return None
    def is_stackref(self):
        oper = self.__get_op_t()
        if not oper.type in [idaapi.o_displ, idaapi.o_phrase]:
            return False
        offset = u2signed(oper.addr)
        return ( idaapi.get_stkvar(oper, offset) != None )
    def __get_op_t(self):
        ins = idautils.DecodeInstruction(self.iea)
        if not ins:
            return None
        else:
            return ins.Operands[self.onum]
             

 
#-----------------------------------------------------------------------
# IdaProExtractor 
# This class implements IDA Pro extraction capabilities. It also uses 
# a UI part (IdaProExtractorUI) in order to get 
# configuration selection from the User
#-----------------------------------------------------------------------
class IdaProTextExtractorScript():

    #
    # This method is in charge for features extraction coordination from an IdaPro Input source
    # it returns an array containing all source features built like:
    # [(functionName, [("searchTerm", "type") ..]), ..]
    # returns None if error
    # Input file singleFile should be built like:
    # (fileName, [func_ea, ..])
    #
    def pluginExtract(self):
        return self.getFunctionFeatures(self.getAllFunctionNamesAndEas())

    #
    # This method is used so plugin user could have the chance
    # to select functions to be extracted in a list of all the functions
    # that are inside a specific 
    #
    def getAllFunctionNamesAndEas(self):
        result = []
        allFuncEAS = get_all_function_eas()
        for ea in allFuncEAS:
            result.append((idaapi.get_func_name(ea), ea))
        return result
 
    #
    # This method aims at returning all extracted features for a 
    # specific range of function. Its returns a features list.
    #
    def getFunctionFeatures(self, funcEaList=None):
        result = []
        if funcEaList:
            for cidx, currFunc in enumerate(funcEaList):
                tempFunc = Function(currFunc[1])
                currFuncFeatures = self.extractFeatures(tempFunc)
                result.append(((tempFunc.get_name(),currFunc[1]), currFuncFeatures))
        #Check for strings!
        idbStringList = getAllStrings()
        
        for singleResult in result:
            for searchTerm in singleResult[1]:
                for singleString in idbStringList:
                    if searchTerm[1] in singleString[0]:
                        idbStringList.remove(singleString)
        
        alreadyInList = [] #This is used as a buffer to prevent duplicate strings
        for string in idbStringList:
            #Prevent duplicate strings
            if string[0] not in alreadyInList:
                #hash = hashlib.md5(string).hexdigest()
                result.append((("Orphan String " + str(string[0]), string[1]),[('s', str(string[0]))]))
                alreadyInList.append(string[0])
        #print len(idbStringList)
        #print result[0]        
        return result

    
    def extractFeatures(self, func):
        #print " --Extracting..."
        IDATA_SEGMENTS1 = get_import_segments()
        joint=[]
        name=[]
        demangle=[]
        constants=[]
        strlist=[]
        implist=[]
        impset = set()
        plist=[]
        rtype=[]
        arglist=[]
        numinst=[]
        numargs=[]
        argbytes=[]
        varbytes=[]
        fnflags=[]
        tagmal=[]
        tagapi=[]
        outcall=[]
        calllist=[]
        fname = func.get_name()
        dename = func.get_demangled_name()
        name.append(('n',fname))
        if dename:
            demangle.append(('ne',dename)) #ne: demangled C++ names
        for inst in func.get_instructions():
            for oper in inst.get_operands():
                val = oper.get_immediate()
                if val:
                    constants.append(('c', "%x" % val))
                    #Symbolic name can't be used in const we have to put it in strings
                    symbolicName = oper.get_symbolicName()
                    if symbolicName is not None and len(symbolicName) > 0:
                        strlist.append(('s',"%s" % symbolicName))
                    
                soper = oper.get_string()
                if soper:
                    if len(soper)>0:
                        #soper = replace_all(soper,BlackDict) 
                        strlist.append(('s',"%s" % soper))
                coderefs = inst.get_code_refs_from()
                for ref in coderefs:
                    if len([start for (start, end) in IDATA_SEGMENTS1 \
                            if start <= ref <= end]) > 0:
                        iname = idaapi.get_name(inst.iea, ref)
                        if iname:
                            impset.add( sanitize_name(iname) )
        for item in impset:
            implist.append( ( 'i', sanitize_name(item) ) )
        addr = func.start_ea 
        fend = idc.GetFunctionAttr(addr, idc.FUNCATTR_END)
        tt = getFuncDeclaration(addr)
        plist.append( ( 'p', tt ) ) #p: prototype
        params =  tt[tt.find("(")+1:tt.find(")")]
        lparams = params.split(',')
        sl = [(par.strip()) for par in lparams]
        for arg in sl:
            if arg:
                arglist.append( ( 'a', arg ) ) #a: arguments
        rt = tt[:tt.find(' ')]
        if rt:
            rtype.append( ( 'r', rt ) ) #r: return type    
        numinst.append( ( 'm', str(func.get_number_of_instructions()) ) ) #m: number of instructions
        g=func.get_number_of_arguments()
        if g:
            numargs.append( ( 'g', str(g) ) ) #g: number of arguments
        bbb=func.get_size_of_argument_bytes()
        if bbb:
            argbytes.append( ( 'b', str(bbb) ) ) #b: size of argument bytes
        varbytes.append( ( 'l', str(func.get_size_of_local_variables()) ) ) #l: size of local vars bytes
        fnflags.append( ( 'f', str(func.get_function_flags()) ) ) #f: function flags
        for elmntz in implist:
            if elmntz[1] in WinMalFuncInSight:
                tagmal.append(('d','MAL'))
        ad=0
        for api_row in api_matrix:
            l = api_row[0]
            apis = api_row[1:]
            for api in apis:
                ref_addrs = idautils.CodeRefsTo(idc.LocByName(api),0)
                for ref in ref_addrs:
                    func_name = idc.GetFunctionName(ref)
                    func_addr = idc.LocByName(func_name)
                    ad=addr 
                    if func_addr == ad:
                        tagapi.append(('t',l))
                    
                    
        bb=func.get_code_refs_from()
        outcall.append(('o', str( len(bb) ) )) # o: number of code refs from this function
        items = idautils.FuncItems(func.start_ea)
        for i in items:
            for xref in idautils.XrefsFrom(i, 0):
                if xref.type == idc.fl_CN or xref.type == idc.fl_CF:
                    dstf = idc.Name(xref.to)
                    calllist.append(('k', dstf )) # o: number of code refs from this function
                    demangled = idc.Demangle(dstf, idc.GetLongPrm(idc.INF_SHORT_DN))
                    if  demangled != None:
                        calllist.append(('ke', demangled )) #ke: demangled C++ call
        joint = name+demangle+constants+strlist+implist+rtype+arglist+numinst+numargs+argbytes+varbytes+fnflags+tagmal+tagapi+outcall+calllist
        z=fend - ad
        if z:
            joint.append(('z', str(z))) #function size (bytes)
        joint.append(('cx',str(len(constants))))
        joint.append(('sx',str(len(strlist))))
        joint.append(('mx',str(numinst[0][1])))
        if g:
            joint.append(('gx',str(numargs[0][1])))
        joint.append(('ix',str(len(implist))))
        joint.append(('dx',str(len(tagmal))))
        joint.append(('tx',str(len(tagapi))))
        joint.append(('ox',str(len(outcall))))
        joint.append(('kx',str(len(calllist))))
        return joint
        
#-----------------------------------------------------------------------
# __main__
# QA main for this module
#-----------------------------------------------------------------------
if __name__ == "__main__":
    
    print "Extractor initialization..."
    #Get our configuration from config manager
    configurationProvision(BSConfigurationManager.ConfigurationManager(None).provideConfiguration(configurationNeed()))
    print "BinSourcerer is ready for magic..."
    x = IdaProTextExtractorScript()
    print "Extracting. This could take a few minutes..."
    results = x.pluginExtract()
    print "Extraction completed. Saving results..."
    
    if not os.path.isdir(IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH):
        os.mkdir(IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH) 
    
    f = open(IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH + IDA_PRO_TEXT_EXTRACTOR_EXTRACTED_FILE, "w")
    for func in results:
        f.write(str(func) + "\n")
    f.close()
    print "Extraction results saved in " + IDA_PRO_TEXT_EXTRACTOR_EXTRACTION_PATH + IDA_PRO_TEXT_EXTRACTOR_EXTRACTED_FILE
    



    
