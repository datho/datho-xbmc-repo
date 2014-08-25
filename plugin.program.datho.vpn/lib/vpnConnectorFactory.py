__author__ = 'martincad'

import config
from utils import Logger
from android import AndroidVPNConnector
from vpn import LinuxVPNConnector, OpenElecVPNConnector, RaspBMCVPNConnector, WindowsVPNConnector

class VPNConnectorFactory:

    @classmethod
    def getConnector(cls, countryName = '', cityName = '', serverAddress = ''):
        Logger.log("Operating System Configured:%s Country:%s city:%s server:%s" % (config.getOS(),countryName, cityName, serverAddress) )
        if config.isAndroid():
            Logger.log("Creating AndroidVPNConnector ...")
            return AndroidVPNConnector(countryName, cityName, serverAddress)
        elif config.isLinux():
            Logger.log("Creating LinuxVPNConnector ...")
            return LinuxVPNConnector(countryName, cityName, serverAddress)
        elif config.isWindows():
            Logger.log("Creating windowsVPNConnector ...")
            return WindowsVPNConnector(countryName, cityName, serverAddress)
        elif config.isOpenElec():
            Logger.log("Creating OpenElecVPNConnector ...")
            return OpenElecVPNConnector(countryName, cityName, serverAddress)
        elif config.isRaspBMC():
            Logger.log("Creating RaspBMCVPNConnector ...")
            return RaspBMCVPNConnector(countryName, cityName, serverAddress)
        raise Exception("Platform %s not supported" % config.getOS())