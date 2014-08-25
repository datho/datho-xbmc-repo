#
# Copyright (C) 2014 Datho Digital Inc., All rights reserved
#
# Permission must be obtained from the copyright holder for any commercial use, distribution or modification of this software.
#




import xbmc
import contextmenu
import config

def runExternal(path):
    cmd = 'ActivateWindow(Programs,"plugin://%s/?mode=%d", return)' % (config.ADDONID, config.EXTERNAL)
    xbmc.executebuiltin(cmd)

def doMenu():
    folder = xbmc.getInfoLabel('Container.FolderPath')
    if config.ADDONID in folder:
        xbmc.executebuiltin('XBMC.Action(ContextMenu)')
        return
        
    choice   = 0
    path     = xbmc.getInfoLabel('ListItem.FolderPath')


    if len(path) > 0:
        menu = []
        menu.append(('Activate Datho-Digital VPN', 1))
        menu.append(('Datho-Digital VPN Settings', 2))
        menu.append(('Standard context menu',      0))

        choice = contextmenu.showMenu(config.ADDONID, menu)

    if choice == None:
        return

    if choice == 0:
        xbmc.executebuiltin('XBMC.Action(ContextMenu)')
        return

    if choice == 2:
        config.ADDON.openSettings()
        return

    if choice == 1:
        runExternal(path)

doMenu()
