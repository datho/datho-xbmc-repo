#
# Copyright (C) 2014 Datho Digital Inc., All rights reserved
#
# Permission must be obtained from the copyright holder for any commercial use, distribution or modification of this software.
#



import xbmcaddon
import xbmc

import os

ADDONID  = 'plugin.program.datho.vpn'
ADDON    =  xbmcaddon.Addon(ADDONID)
HOME     =  ADDON.getAddonInfo('path')
PROFILE  =  xbmc.translatePath(ADDON.getAddonInfo('profile'))
EXTERNAL = 0
TITLE    = 'Datho-Digital VPN'
VERSION  = '0.3.1'

COUNTRIES = {'AT' : 'Austria', 'AU':'Australia', 'BE':'Belguim', 'BR':'Brazil', 'CH':'Switzerland', 'DK':'Denmark', 'DE':'Germany', 'ES':'Spain', 'FR':'France', 'HU':'Hungary',  'JP':'Japan', 'KR':'South Korea', 'NL':'Netherlands', 'PL':'Poland', 'SE':'Sweden', 'SG':'Singapore', 'UK':'United Kingdom', 'US':'United  States'}
OpenVPNLogFilePath =  os.path.join(PROFILE, 'openvpn.log')
StdErrLogFilePath =  os.path.join(PROFILE, 'stderr.log')
IMAGES   =  os.path.join(HOME, 'resources', 'images')
ICON     =  os.path.join(HOME, 'icon.png')
FANART   =  os.path.join(HOME, 'fanart.jpg')
URL      =  'http://www.wlvpn.com/serverList.xml'


def getOS():
    return ADDON.getSetting('OS')

def isWindows():
    return getOS() == 'Windows'

def isLinux():
    return getOS() == 'Linux'

def isAndroid():
    return getOS() == 'Android'

def isOpenElec():
    return getOS() == 'OpenElec'

def isRaspBMC():
    return getOS() == 'RaspBMC'

def getSudo():
    if isWindows():
        return None, None

    sudopwd = None
    sudo    = ADDON.getSetting('SUDO') == 'true'

    if sudo:
        sudopwd = ADDON.getSetting('SUDOPASS')

    return sudo, sudopwd

def getUsername():
    return ADDON.getSetting('USER')

def getPassword():
    return ADDON.getSetting('PASS')

# Return True if User and Password are not empty
def CheckCredentialsEmpty():
    user = getUsername()
    pwd  = getPassword()
    return user is '' or pwd is ''

def getSetting(name, defaultValue ):
    try:
        return ADDON.getSetting('PASS')
    except Exception:
        return defaultValue

def getIntSetting(name, defaultValue ):
    value = int(defaultValue)
    try:
        value = ADDON.getSetting(name)
    except Exception:
        pass

    return int(value)

def getTimeout():
    return getIntSetting('TIMEOUT', 1800)

def getPort():
    return ADDON.getSetting('PORT')


def _getConfigDirPath():
    return os.path.join(HOME, 'resources', 'configs')

def getCertFilePath():
    """
    Returns the Path containing the Certificate used by OpenVPN
    :return:
    """
    root    = _getConfigDirPath()
    return os.path.join(root, 'vpn.crt')

def getOpenVPNTemplateConfigFilePath():
    """
        Returns the Template file path containing the default configuration parameters for OpenVPN
        this file should always keep unchanged
    :return:s
    """
    root    = _getConfigDirPath()
    return os.path.join(root, 'cfg.opvn')

def getOpenVPNRealConfigFilePath():
    """
    Returns the file path where the configuration file containing the OpenVPN Parameters is
    :return:aaa
    """
    return os.path.join(PROFILE, 'cfg.opvn')

def getActionUrl():
    return "http://localhost:8000/service/addon/"