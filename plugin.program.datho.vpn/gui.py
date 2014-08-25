#
# Copyright (C) 2014 Datho Digital Inc., All rights reserved
#
# Permission must be obtained from the copyright holder for any commercial use, distribution or modification of this software.
#


import xbmcgui
import xbmcplugin

import urllib
import config

from utils import Logger

def DialogOK(line1, line2='', line3=''):
    d = xbmcgui.Dialog()
    #d.ok(TITLE + ' - ' + VERSION, line1, line2 , line3)
    Logger.log("Dialog:%s %s %s" % (line1, line2 , line3), Logger.LOG_DEBUG)
    d.ok(config.TITLE, line1, line2 , line3)


def ShowBusy():
    busy = None
    try:
        busy = xbmcgui.WindowXMLDialog('DialogBusy.xml', '')
        busy.show()

        try:    busy.getControl(10).setVisible(False)
        except: pass
    except:
        busy = None

    return busy

def ShowSettings():
    config.ADDON.openSettings()


def addDir(args, label, mode, abrv='', thumbnail='', server='', isFolder=True, countryName = ''):
    #if thumbnail=''
    #    thumbnail = ICON


    u  = args[0]
    u += '?mode='     + str(mode)
    u += '&label='    + urllib.quote_plus(label)
    u += '&abrv='     + urllib.quote_plus(abrv)
    u += '&server='   + urllib.quote_plus(server)
    u += '&country='   + urllib.quote_plus(countryName)

    liz = xbmcgui.ListItem(label, iconImage=thumbnail, thumbnailImage=thumbnail)

    #liz.setProperty('Fanart_Image', FANART)

    xbmcplugin.addDirectoryItem(handle=int(args[1]), url=u, listitem=liz, isFolder=isFolder)