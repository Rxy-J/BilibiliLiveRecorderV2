import threading

from libs.Monitor import SizeMonitor, SpeedMonitor
from libs.Live.BilibiliLiveRecorder import BilibiliLiveRecorder

class record(threading.Thread):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def run(self):
        try:
            liveRoomId = self.window.liveNumber.text()
            self.window.recordSavePath = self.window.recordSavePath if not self.window.liveSavePath.text() else self.window.liveSavePath.text()
            recorder = BilibiliLiveRecorder(liveRoomId, self.window.recordSavePath, self.window)
            sizemonitor = SizeMonitor(recorder, self.window)
            speedmonitor = SpeedMonitor(recorder, self.window)
            recorder.start()
            sizemonitor.start()
            speedmonitor.start()  
            recorder.join()
        except Exception as e:
            self.window.log.error(str(e))