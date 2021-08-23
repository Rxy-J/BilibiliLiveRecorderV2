import threading
import time
from datetime import datetime

class Monitor(threading.Thread):
    def __init__(self, recordThread):
        super().__init__()
        self.recordThread = recordThread

    def run(self):
        while True:
            while not self.recordThread.isRecord:
                time.sleep(3)
            while self.recordThread.isRecord:
                size = self.transform(self.recordThread.downloadSize)
                size_info = "\r"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"[INFO]:直播间【{0}】当前已下载==>{1}".format(self.recordThread.room_id, size)
                print("\r"+" "*len(size_info), end="")
                print(size_info, end="")
                time.sleep(1)
            print("")

    def transform(self, size):
        counter = 0
        while size > 1024:
            counter += 1
            size /= 1024
        size = round(size, 2)
        if counter == 0:
            size = str(size)+"bytes"
        elif counter == 1:
            size = str(size)+"KB"
        elif counter == 2:
            size = str(size)+"MB"
        elif counter == 3:
            size = str(size)+"GB"
        elif counter == 4:
            size = str(size)+"TB"
        elif counter == 5:
            size = str(size)+"PB"
        elif counter == 6:
            size = str(size)+"ZB"
        else:
            size = "您太离谱了"
        
        return size