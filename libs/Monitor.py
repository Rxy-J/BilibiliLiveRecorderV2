import threading
import time
from libs.parserSize import getSize

class Monitor(threading.Thread):
    def __init__(self, recordThread, window):
        super().__init__()
        self.recordThread = recordThread
        self.window = window
        self.log = window.log

    def run(self):
        pass

class SizeMonitor(Monitor):
    def __init__(self, recordThread, window):
        super().__init__(recordThread, window)

    
    def run(self):
        while not self.window.threadStop:
            while not self.recordThread.isRecord:
                time.sleep(3)
            while self.recordThread.isRecord and (not self.window.threadStop):
                size = getSize(self.recordThread.downloadSize)
                self.log.success("当前已下载==>{0}".format(size), self.recordThread.room_id)
                time.sleep(2)

class SpeedMonitor(Monitor):
    def __init__(self, recordThread, window):
        super().__init__(recordThread, window)

    def run(self):
        while not self.window.threadStop:
            while not self.recordThread.isRecord:
                time.sleep(3)
            lastSize = 0
            newSize = 0
            title = self.window.windowTitle()
            while self.recordThread.isRecord and (not self.window.threadStop):
                newSize = self.recordThread.downloadSize
                size = getSize(newSize - lastSize) + "/s"
                self.window.setWindowTitle(title+"  "+size)
                lastSize = newSize
                time.sleep(1)
            self.window.setWindowTitle(title)