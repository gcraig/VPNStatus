#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools, glob
import SysTrayIcon
import win32ras 
import os
import sys
import ConfigParser

class VPNStatus:

    hover_text = "ITSy VPN"
    grasHandle = None
    debug = 1

    script_dir = os.path.realpath(os.path.dirname(sys.argv[0]))
    icon_connected = script_dir + '\\vpn-connected.ico'
    icon_disconnected = script_dir + '\\vpn-disconnected.ico'

    def connect(self, sysTrayIcon):
        print 'Connecting ...'
        vpn, pw = win32ras.GetEntryDialParams(None, 'ITSy VPN')
        rasHandle, retCode = win32ras.Dial(None, None, vpn, None)
        self.grasHandle = rasHandle
        if self.debug is 1: 
            print('retCode=%s' % retCode) 
            print('rasHandle=%s' % rasHandle)        
            print('grasHandle=%s' % self.grasHandle)
        if rasHandle is not None:
            sysTrayIcon.icon = self.icon_connected # "vpn-connected.ico"
            sysTrayIcon.refresh_icon()
            print 'Connected.'

    def disconnect(self, sysTrayIcon):
        print 'Disconnecting ...'
        if self.debug is 1: 
            print('grasHandle=%s' % self.grasHandle)
        if self.grasHandle is not None:
            win32ras.HangUp(self.grasHandle)
            self.grasHandle = None
        sysTrayIcon.icon = self.icon_disconnected # "vpn-disconnected.ico"
        sysTrayIcon.refresh_icon()
        print 'Disconnected.'
    
    def bye(self, sysTrayIcon):
        self.disconnect(sysTrayIcon)
        print 'Bye, then.'
    
    def __init__(self):
        menu_options = (('Connect', self.icon_connected, self.connect),
                    ('Disconnect', self.icon_disconnected, self.disconnect))
        SysTrayIcon.SysTrayIcon(self.icon_disconnected, self.hover_text,
        menu_options, on_quit=self.bye, default_menu_index=1)

if __name__ == '__main__':
    VPNStatus()
