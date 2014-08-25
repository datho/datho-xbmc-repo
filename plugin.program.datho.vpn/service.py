#
# Copyright (C) 2014 Datho Digital Inc., All rights reserved
#
# Permission must be obtained from the copyright holder for any commercial use, distribution or modification of this software.
#




import os
import traceback

import xbmc
from utils import Logger

import config

KEYMAP  = 'datho_vpn_menu.xml'


def DeleteKeymap():
    path = os.path.join(xbmc.translatePath('special://userdata/keymaps'), KEYMAP)

    tries = 5
    while os.path.exists(path) and tries > 0:
        tries -= 1 
        try: 
            os.remove(path) 
            break 
        except: 
            xbmc.sleep(500)


def UpdateKeymap():
    DeleteKeymap()

    if config.ADDON.getSetting('CONTEXT')  == 'true':
        src = os.path.join(config.HOME, 'resources', 'keymaps', KEYMAP)
        dst = os.path.join(xbmc.translatePath('special://userdata/keymaps'), KEYMAP)

        import shutil
        shutil.copy(src, dst)

    xbmc.sleep(1000)
    xbmc.executebuiltin('Action(reloadkeymaps)')  



class MyMonitor(xbmc.Monitor):
    def __init__(self):
        xbmc.Monitor.__init__(self)
        self.context = config.ADDON.getSetting('CONTEXT')  == 'true'
        self.context = not self.context
        self.onSettingsChanged()


    def onSettingsChanged(self):
        context = config.ADDON.getSetting('CONTEXT')  == 'true'

        if self.context == context:
            return

        self.context = context
        
        UpdateKeymap()
        

monitor = MyMonitor()


while (not xbmc.abortRequested):
    xbmc.sleep(1000)


del monitor
from lib import vpn

try:
    Logger.log("Service main code executed", Logger.LOG_DEBUG)

    vpnConnector = vpn.VPNConnectorFactory.getConnector()
    ret = vpnConnector.kill(showBusy=True)
except Exception:
    Logger.log("Exception raised while trying to execute service main")
    traceback.print_exc()