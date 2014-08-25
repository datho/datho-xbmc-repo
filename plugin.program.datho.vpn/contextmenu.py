#
# Copyright (C) 2014 Datho Digital Inc., All rights reserved
#
# Permission must be obtained from the copyright holder for any commercial use, distribution or modification of this software.
#


import xbmc
import xbmcgui
import xbmcaddon
import os

ACTION_BACK          = 92
ACTION_PARENT_DIR    = 9
ACTION_PREVIOUS_MENU = 10
ACTION_CONTEXT_MENU  = 117

ACTION_LEFT  = 1
ACTION_RIGHT = 2
ACTION_UP    = 3
ACTION_DOWN  = 4


class ContextMenu(xbmcgui.WindowXMLDialog):

    def __new__(cls, addonID, menu):
        return super(ContextMenu, cls).__new__(cls, 'contextmenu.xml', xbmcaddon.Addon(addonID).getAddonInfo('path'))
        

    def __init__(self, addonID, menu):
        super(ContextMenu, self).__init__()
        self.menu = menu

        
    def onInit(self):
        self.list      = self.getControl(3000)
        self.params    = None
        self.paramList = []

        for item in self.menu:
            self.paramList.append(item[1])
            title = item[0]
            liz   = xbmcgui.ListItem(title)
            self.list.addItem(liz)

        self.setFocus(self.list)

           
    def onAction(self, action):
        actionId = action.getId()


        if actionId in [ACTION_CONTEXT_MENU, ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK, ACTION_CONTEXT_MENU]:
            return self.close()


    def onClick(self, controlId):
        if controlId != 3001:
            index = self.list.getSelectedPosition()        
            try:    self.params = self.paramList[index]
            except: self.params = None

        self.close()
        

    def onFocus(self, controlId):
        pass


def showMenu(addonID, menu):
    menu = ContextMenu(addonID, menu)
    menu.doModal()
    params = menu.params
    del menu
    return params