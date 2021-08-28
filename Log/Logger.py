# coding = utf-8
import os

from datetime import datetime
from PyQt5 import QtWidgets

LOG_PATH = "Log"
LOG_FILE = "log.log"

class Logger:
    def __init__(self, rootPath, window):
        self.window = window
        self.logPath = os.path.join(rootPath, LOG_PATH)
        self.logFile = os.path.join(self.logPath, LOG_FILE)
        if not os.path.exists(self.logPath):
            os.mkdir(self.logPath)

    def success(self, logInfo, roomId=None):
        logTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not roomId == None :
            log = logTime+"[INFO]: 直播间【{0}】 {1}".format(roomId, logInfo)
        else :
            log = logTime+"[INFO]: {0}".format(logInfo)
        self.window.messager.append(log)
        self.cursor=self.window.messager.textCursor()
        self.window.messager.moveCursor(self.cursor.End)
        QtWidgets.QApplication.processEvents() #一定加上这个功能，不然有卡顿
        with open(self.logFile, "a", encoding="UTF-8") as f:
            f.write(log+"\n")
        print(log)
    
    def error(self, logInfo, roomId=None):
        logTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not roomId == None :
            log = logTime+"[ERROR]: 直播间【{0}】 {1}".format(roomId, logInfo)
        else :
            log = logTime+"[ERROR]: {0}".format(logInfo)
        self.window.messager.append(log)
        self.cursor=self.window.messager.textCursor()
        self.window.messager.moveCursor(self.cursor.End)
        QtWidgets.QApplication.processEvents() #一定加上这个功能，不然有卡顿
        with open(self.logFile, "a", encoding="UTF-8") as f:
            f.write(log+"\n")
        print(log)