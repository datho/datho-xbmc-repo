__author__ = 'martincad'

import time
import os
import json
import traceback

import xbmc

from vpn import VPNConnector
from utils import Logger
import gui
import config


class AndroidVPNConnector(VPNConnector):

    OPENVPN_CONNECT_ACTION = "CONNECT"
    OPENVPN_DISCONNECT_ACTION = "DISCONNECT"
    CONTROLLER_FINISH = "FINISH"


    def _shouldKillBeforeConnect(self):
        return False


    def kill(self, showBusy = False):
        busy = None
        if showBusy:
            busy = gui.ShowBusy()

        self._eraseRemoteControllerStatusFile()

        Logger.log("Android kill. Disconnecting first attemp...")

        # The Remote Controller needs two disconnects in case the VPN bind fails
        ret = self._disconnect(3)
        if ret!=self.DISCONNECT_OK:
            Logger.log("Android kill. Disconnecting second attemp...")
            ret = self._disconnect(30)

            if ret==self.DISCONNECT_OK:
                Logger.log("Disconnection Ok...the VPN must be disconnected now", Logger.LOG_DEBUG)
                pass
            elif ret==self.NO_RESPONSE:
                gui.DialogOK("Error when trying to Kill the VPN", "No notifications received from Remote Controller")
                Logger.log("Error when trying to Kill the VPN: No notifications received from Remote Controller", Logger.LOG_ERROR)
            elif ret==self.DISCONNECT_TIMEOUT:
                gui.DialogOK("Error when trying to disconnect the OpenVPN", "it did not disconnec", "Please retry")
                Logger.log("Error when trying to disconnect the OpenVPN: it did not disconnect", Logger.LOG_ERROR)
            else:
                gui.DialogOK("Unknown Error while disconnecting", "", "")
                Logger.log("Unknown Error while disconnecting", Logger.LOG_ERROR)

        self._stopRemoteController()

        if busy:
            busy.close()

        return ret==self.DISCONNECT_OK


    NO_RESPONSE = -1
    DISCONNECT_TIMEOUT = -2
    DISCONNECT_OK = 0

    # Returns
    # NO_RESPONSE
    # NOT_DISCONNECTED
    def _disconnect(self, timeout):
        ret = self._runRemoteController(self.OPENVPN_DISCONNECT_ACTION, timeout)
        if not ret:
            return self.NO_RESPONSE

        startTime = time.time()
        elapsed = 0
        status = None
        while elapsed < timeout:
            status = self._getCurrentStatus()
            Logger.log("Disconnect Checking Status:%s" % status, Logger.LOG_DEBUG)

            DISCONNECTED = 'NOPROCESS; No process running.; LEVEL_NOTCONNECTED'

            if DISCONNECTED in status:
                Logger.log("Disconnected Ok")
                return self.DISCONNECT_OK

            xbmc.sleep(1000)

            elapsed = time.time() - startTime
        print status
        return self.DISCONNECT_TIMEOUT



    def _eraseRemoteControllerStatusFile(self):
        for i in range(5):
            Logger.log("Trying to erase remote controller status file", Logger.LOG_DEBUG)
            try:
                os.remove(self._getRemoteControllerStatusFilePath())
                Logger.log("Trying to erase remote controller status file. Erase successfully", Logger.LOG_DEBUG)
                return
            except Exception, e:
                Logger.log("There was an error while trying to erase status file", Logger.LOG_ERROR)
                traceback.print_exc(e)
                xbmc.sleep(50)

    def _doConnect(self, busy = None):
        self._connectAndCheckStatus()
        self._stopRemoteController(3)


    def _connectAndCheckStatus(self, busy = None):

        # Erase the Remote Controller status file because if not the Controller appends into that file
        self._eraseRemoteControllerStatusFile()

        Logger.log("Android _doConnect starting ...", Logger.LOG_DEBUG)

        ret = self._runRemoteController(self.OPENVPN_CONNECT_ACTION, self._timeout)
        if not ret:
            gui.DialogOK("It was not possible to execute the VPN Remote Controller", "Please check if it is installed in your Android", "")
            return

        statusDone = False

        startTime = time.time()
        elapsed = 0
        MAX_TIMEOUT = 60
        statusGrabbed = False
        status = ''
        while elapsed < MAX_TIMEOUT:
            status = self._getCurrentStatus()
            Logger.log("Checking Status:%s" % status, Logger.LOG_DEBUG)

            ASSIGN_IP = 'ASSIGN_IP;'

            # Check if after the ASSIGN_IP notification a CONNECTED; SUCCESS is notified
            if ASSIGN_IP in status  and 'CONNECTED; SUCCESS' in status[status.find(ASSIGN_IP):]:
                Logger.log("VPN IP assigned and connected Ok", Logger.LOG_INFO)
                msg1, msg2, msg3 = self._connectionOkMessage()
                gui.DialogOK(msg1, msg2, msg3)
                statusGrabbed = True
                break

            elif 'USER_DID_NOT_APPROVE_THE_APP' in status:
                gui.DialogOK("The VPN Client was not approved", "Please try again", "")
                statusGrabbed = True
                break

            elif 'EXITING; auth-failure' in status:
                gui.DialogOK("There was an error while logging in", "Please check the credentials", "and try again")
                self.kill()
                statusGrabbed = True
                break

            xbmc.sleep(1000)
            elapsed = time.time() - startTime

        Logger.log("_GetCurrent status:::")
        print status
        if not statusGrabbed:
            gui.DialogOK("There was an error", "The VPN client was not able to connect", "please try again")
            Logger.log("ERROR it break the loop with timeout. Check the notification status", Logger.LOG_ERROR)

        if busy:
            busy.close()

        return statusGrabbed




    def _runRemoteController(self, action, timeout = 0):
        Logger.log("Android _runRemoteController starting with action:%s..." % action, Logger.LOG_DEBUG)
        runnerConfigFilePath = self._writeRemoteControllerConfig(action)

        params = {"CONFIG" : runnerConfigFilePath}
        jsonConfig = json.dumps(params)

        Logger.log("Executing Remote Controller", Logger.LOG_DEBUG)
        xbmc.executebuiltin('XBMC.StartAndroidActivity("com.datho.vpn.remote","","",'+jsonConfig+')')

        return self._waitUntilCommandProcessed(timeout)


    def _getCurrentStatus(self):
        data = ""
        try:
            file = open(self._getRemoteControllerStatusFilePath(), "r")
            data  = file.read(100000)
            # Remove the timestamp from the log
            #strippedLines = [' '.join(line.split(' ')[2:]) for line in lines]
            file.close()
        except IOError, e:

            if 'No such file or directory' in e.strerror:
                Logger.log("_getCurrentStatus file does not exist yet:%s" % self._getRemoteControllerStatusFilePath())
                return ""

            Logger.log("_getCurrentStatus exception reading Status File:%s" % str(e), Logger.LOG_INFO)
            traceback.print_exc()

        return data

    def _getRemoteControllerStatusFilePath(self):
        return os.path.join(config.PROFILE, 'status.txt')

    def _getRunnerConfigFilePath(self):
        return os.path.join(config.PROFILE, 'controller.config.txt')



    def _writeRemoteControllerConfig(self, action):

        openVPNConfigurationPath = self._getOpenVPNConfigPath()

        Logger.log("Android _writeRemoteControllerConfig starting ...", Logger.LOG_DEBUG)
        actionList = [self.CONTROLLER_FINISH, self.OPENVPN_CONNECT_ACTION, self.OPENVPN_DISCONNECT_ACTION]
        if action not in actionList:
            msg = "Action:*%s* is INVALID. It must be one of:%r" % (action, actionList)
            Logger.log(msg, Logger.LOG_FATAL)
            raise Exception(msg)

        Logger.log("Android _writeRemoteControllerConfig writing remotecontroller config file", Logger.LOG_DEBUG)
        runnerConfigFilePath = self._getRunnerConfigFilePath()
        notificationPath = os.path.join(config.PROFILE, 'status.txt')
        file = open(runnerConfigFilePath, "w+")
        file.write(action + "\n")
        file.write(openVPNConfigurationPath + "\r\n")
        file.write(notificationPath + "\r\n")
        file.close()
        Logger.log("Android _writeRemoteControllerConfig done", Logger.LOG_DEBUG)
        return runnerConfigFilePath


    def _stopRemoteController(self, timeout = 15):
        Logger.log("Android _forceAndroidControllerStop", Logger.LOG_DEBUG)
        ret = self._runRemoteController(self.CONTROLLER_FINISH, timeout)
        if not ret:
            Logger.log("Remote Controller did not respond the FINISH command", Logger.LOG_ERROR)
            gui.DialogOK("Error when trying terminate the Remote Controller", "No notifications received from Remote Controller")




    def _waitUntilCommandProcessed(self, timeoutSecs = 60):
        elapsed = 0
        to_sleep = 1
        while elapsed < timeoutSecs:
            Logger.log("_waitUntilCommandProcessed waiting for data to be read: %s" % self._getRunnerConfigFilePath(), Logger.LOG_DEBUG)
            file = open(self._getRunnerConfigFilePath(), "r")
            data = file.read()
            Logger.log("_waitUntilCommandProcessed data read: len:%d DATA:*%s*" % (len(data),data) , Logger.LOG_DEBUG)
            file.close()
            if not data:
                Logger.log("_waitUntilCommandProcessed data read returning", Logger.LOG_INFO)
                return True
            xbmc.sleep(to_sleep * 1000)
            elapsed += to_sleep


        Logger.log("_waitUntilCommandProcessed data was never read", Logger.LOG_INFO)

        return False
