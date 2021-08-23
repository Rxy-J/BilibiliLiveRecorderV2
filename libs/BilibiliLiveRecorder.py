import os
import requests
import time
import re
import threading
import flv2mp4

from datetime import datetime
from Live import BiliBiliLive

REAL_PATH = os.path.dirname(os.path.realpath(__file__))
LOG_PATH = REAL_PATH+"/log.log"
RECORD_FILE_PATH = REAL_PATH + "/recordFiles/"
DEFAULT_CHECK_INTERVAL = 60
TIMEOUT = 60*5
VERSION = "1.5.2"

class BiliBiliLiveRecorder(BiliBiliLive, threading.Thread):
    def __init__(self, room_id, logger, checkInterval=DEFAULT_CHECK_INTERVAL, recordFilePath=RECORD_FILE_PATH, timeout=TIMEOUT):
        BiliBiliLive.__init__(self, room_id)
        threading.Thread.__init__(self)
        self.log = logger # 日志模块
        self.checkInterval = checkInterval # 检测延迟
        self.recordFilePath = recordFilePath # 存放位置
        self.isRecord = False
        self.timeout = timeout
        self.downloadSize = 0

    def check(self):
        try:
            roomInfo = self.get_room_info()
            if roomInfo['status']:
                self.roomName = roomInfo["roomname"]
                if not self.isRecord:
                    self.log.success(self.roomName)
                self.isRecord = True
            else:
                self.isRecord = False
                self.log.success('等待开播')
        except Exception as e:
            self.log.error(str(e))
        return self.isRecord

    def record(self, recordFilename):
        while self.isRecord:
            try:
                self.downloadSize = 0
                recordUrl = self.get_live_urls()[0]
                self.log.success('√ 正在录制...')
                headers = {
                    'Accept-Encoding': 'identity',
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                    'Referer' : re.findall(r'(https://.*\/).*\.flv', recordUrl)[0],
                }
                response = requests.get(recordUrl, stream=True, headers=headers)
                with open(recordFilename, "ab") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk if chunk else None)
                        self.downloadSize += 1024
            except Exception as e:
                self.log.error(str(e))
            self.check()

    def run(self):
        while True:
            try:
                while not self.check():
                    time.sleep(self.checkInterval)
                streamTime = datetime.now().strftime("%Y-%m-%d %H%M")
                filename_flv = self.recordFilePath+"{0} {1}.flv".format(streamTime, self.roomName)
                filename_mp4 = self.recordFilePath+"{0} {1}.mp4".format(streamTime, self.roomName)
                self.record(filename_flv)
                self.log.success('录制完成' + filename_flv)
                flv2mp4.flv2mp4(filename_flv, filename_mp4)
                self.log.success("转码完成，文件保存到"+filename_mp4)
            except Exception as e:
                self.log.error(str(e))


