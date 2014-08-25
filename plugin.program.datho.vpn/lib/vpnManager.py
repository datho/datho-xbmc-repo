#
# Copyright (C) 2014 Datho Digital Inc., All rights reserved
#
# Permission must be obtained from the copyright holder for any commercial use, distribution or modification of this software.
#

import re
import os
import time
import urllib2

import config
from utils import Logger

class NoConnectionError(Exception):
    pass

class VPNContainer():
    def __init__(self, items):
        self.server   = items[0]
        self.capacity = int(items[1])
        self.city     = items[2]
        self.abrv     = items[3]
        self.icon     = os.path.join(config.IMAGES, self.abrv.lower()+'.png') # items[4]
        self.ip       = items[5]
        self.status   = int(items[6])
        self.visible  = items[7] == '1'
        self.country  = self.abrv
        if config.COUNTRIES.has_key(self.country):
                self.country = config.COUNTRIES[self.country]
        self.mustShow = self.status == 1 and self.visible

class VPNServerManager:

    URL      =  'http://www.wlvpn.com/serverList.xml'
    REGEX = 'server name="(.+?)" capacity="(.+?)" city="(.+?)" country="(.+?)" icon="(.+?)" ip="(.+?)" status="(.+?)" visible="(.+?)"'
    TIMEOUT = 15 * 60
    _instance = None


    @classmethod
    def getInstance(cls):
        if cls._instance is None or cls._instance._isContentOld():
            cls._instance = VPNServerManager()
            cls._instance._init()
        return cls._instance

    def _isContentOld(self):
        # If the last time the content was grabbed from the web is more than 15 minutes ago
        return (time.time() - self.lastContentUpdateTimestamp > self.TIMEOUT)

    def _getItems(self):
        try:
            html  = GetContentFromUrl(self.URL)
            return re.compile(self.REGEX).findall(html)
        except urllib2.URLError, e:
            Logger.log("There was an error while getting content from remote server")
            raise NoConnectionError("There was an error while getting content from remote server")

    def _init(self):
        self.lastContentUpdateTimestamp = time.time()

        items = self._getItems()

        self.countryMap = {}
        self.cityByCountryMap = {}

        for item in items:
            vpn = VPNContainer(item)
            if vpn.country not in self.countryMap:
                if vpn.mustShow:
                    self.countryMap[vpn.abrv] = [vpn.country, vpn.abrv, vpn.icon]

            if not vpn.mustShow:
                continue

            cities = self.cityByCountryMap.get(vpn.abrv, [] )
            self.cityByCountryMap[vpn.abrv] = cities
            cities.append([vpn.city, vpn.icon, vpn.capacity, vpn.ip])

        self.countries = self.countryMap.values()
        self.countries.sort()


    def getCities(self, countryAbrv):
        if countryAbrv not in self.cityByCountryMap:
            Logger.log("Country %s not in map:%r" % (countryAbrv, self.cityByCountryMap.keys()), Logger.LOG_ERROR)
        l = self.cityByCountryMap[ countryAbrv ]
        l.sort()
        return l

    def getCountries(self):
        return self.countries


def GetContentFromUrl(url, agent = ''):
    req = urllib2.Request(url)
    req.add_header('User-Agent', agent)

    response = urllib2.urlopen(req)
    html     = response.read()
    response.close()
    return html