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
