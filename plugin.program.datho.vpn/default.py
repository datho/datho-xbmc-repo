#
# Copyright (C) 2014 Datho Digital Inc., All rights reserved
#
# Permission must be obtained from the copyright holder for any commercial use, distribution or modification of this software.
#


import urllib
import xbmcplugin
import gui
from lib import common
from lib.vpnConnectorFactory import VPNConnectorFactory
from lib.vpnManager import VPNServerManager, NoConnectionError



_SETTINGS  = 100
_KILL      = 200
_SEPARATOR = 300
_COUNTRY   = 400
_VPN       = 500


arguments = sys.argv




def Main():
    common.CheckVersion()
    common.CheckUsername()

    gui.addDir(arguments, 'Configure VPN', _SETTINGS,  isFolder=False)
    gui.addDir(arguments, 'Disable VPN',   _KILL,      isFolder=False)
    gui.addDir(arguments, ' ',             _SEPARATOR, isFolder=False)

    try:
        for country in VPNServerManager.getInstance().getCountries():
            gui.addDir(arguments, country[0], _COUNTRY, abrv=country[1], thumbnail=country[2])
    except NoConnectionError:
        gui.DialogOK("It is not possible to connect to the remote server", "Check your network connection", "and try again")


def addCitiesForCountry(countryName):
    try:
        cities = VPNServerManager.getInstance().getCities(countryName)
        for city in cities:
            label = '%s (%d)' % (city[0], city[2])
            gui.addDir(arguments, label, _VPN, thumbnail=city[1], server=city[3], isFolder=False, countryName = countryName)
    except NoConnectionError:
        gui.DialogOK("It is not possible to connect to the remote server", "Check your network connection", "and try again")













def get_params():
    param=[]
    paramstring=arguments[2]
    if len(paramstring)>=2:
        params=arguments[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
           params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param



params = get_params()
mode     = -1

try:    mode = int(params['mode'])
except: pass




if mode == _COUNTRY:
    label = urllib.unquote_plus(params['label'])
    abrv  = urllib.unquote_plus(params['abrv'])
    countrySelected = abrv
    addCitiesForCountry(abrv)

elif mode == _VPN:
    label  = urllib.unquote_plus(params['label'])
    abrv   = urllib.unquote_plus(params['abrv'])
    server = urllib.unquote_plus(params['server'])
    country = urllib.unquote_plus(params['country'])

    city = label.rsplit(' (', 1)[0]
    vpnConnector = VPNConnectorFactory.getConnector(country, city, server)
    vpnConnector.connectToVPNServer()

elif mode == _SETTINGS:
    gui.ShowSettings()

elif mode == _KILL:
    vpnConnector = VPNConnectorFactory.getConnector()
    ret = vpnConnector.kill(showBusy=True)
    if ret:
        gui.DialogOK('VPN now disabled')
    else:
        gui.DialogOK('VPN is still enabled', 'There was an error while trying to disconnect OpenVPN')


elif mode == _SEPARATOR:
    pass

else:
    Main()


xbmcplugin.endOfDirectory(int(arguments[1]))

# This is for 0.3.1