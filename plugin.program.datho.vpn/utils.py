#
# Copyright (C) 2014 Datho Digital Inc., All rights reserved
#
# Permission must be obtained from the copyright holder for any commercial use, distribution or modification of this software.
#

import re
try:
    import requests2 as requests
except:
    import requests

import xbmc


class Logger:

    LOG_DEBUG = xbmc.LOGDEBUG
    LOG_INFO = xbmc.LOGINFO
    LOG_WARNING = xbmc.LOGWARNING
    LOG_ERROR = xbmc.LOGERROR
    LOG_FATAL = xbmc.LOGFATAL

    @classmethod
    def log(cls, msg, level = LOG_INFO, prefix = "Datho VPN"):

        return xbmc.log("%s %s" % (prefix, msg), level)



def GetPublicNetworkInformation():

    url = 'http://www.ip2location.com/'

    response = requests.get(url)
    content = response.content
    Logger.log("GetPublicNetworkInformation: trying to get information ...", Logger.LOG_DEBUG)
    ipAddressMatch   = re.compile("<td><label>(.+?)</label></td>").findall(content)
    countryMatch   = re.compile("<td><label for=\"chkCountry\">(.+?)</label></td>").findall(content)
    cityMatch   = re.compile("<td><label for=\"chkRegionCity\">(.+?)</label></td>").findall(content)

    if len(ipAddressMatch)!=2 or len(countryMatch)!=2 or len(cityMatch)!=2:
        Logger.log("There was an error parsing network data from %s" % url)
        print "There was an error parsing the data"
        return None

    Logger.log("GetPublicNetworkInformation: ip:%s country:%s city:%s" % (ipAddressMatch[1], countryMatch[1], cityMatch[1]), Logger.LOG_DEBUG)
    return ipAddressMatch[1], countryMatch[1], cityMatch[1]
