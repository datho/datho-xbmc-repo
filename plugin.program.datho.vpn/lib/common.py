__author__ = 'martincad'

import gui
import config
from utils import Logger

def CheckVersion():
    prev = config.ADDON.getSetting('VERSION')
    curr = config.VERSION

    msg = 'Welcome to Datho VPN %s' % config.VERSION

    Logger.log(msg, Logger.LOG_ERROR)
    gui.DialogOK(msg)

    if prev == curr:
        return

    config.ADDON.setSetting('VERSION', curr)


    if prev == '0.0.0':
        gui.DialogOK(msg)


def CheckUsername():
    if config.CheckCredentialsEmpty():
        gui.DialogOK('Please enter your username and password')
        gui.ShowSettings()

