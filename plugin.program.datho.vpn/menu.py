#
#       Copyright (C) 2014 Datho Digital Inc
#       Martin Candurra (martincandurra@dathovpn.com)
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
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
