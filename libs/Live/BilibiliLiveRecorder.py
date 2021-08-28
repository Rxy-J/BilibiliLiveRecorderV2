
import os
import requests
import time
import re
import threading

from datetime import datetime

from .BilibiliLive import BiliBiliLive

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_CHECK_INTERVAL = 60


class BilibiliLiveRecorder(BiliBiliLive, threading.Thread):
    def __init__(self, room_id, recordFilePath, window, checkInterval=DEFAULT_CHECK_INTERVAL):
        BiliBiliLive.__init__(self, room_id)
        threading.Thread.__init__(self)
        self.window = window
        self.log = window.log  # 日志模块
        self.recordFilePath = recordFilePath  # 文件保存路径
        self.checkInterval = checkInterval  # 检测延迟
        self.isRecord = False
        self.downloadSize = 0

    def check(self):
        try:
            roomInfo = self.get_room_info()
            if roomInfo['status']:
                self.roomName = roomInfo["roomname"]
                self.isRecord = True
                self.log.success(self.roomName, self.room_id)
            else:
                self.isRecord = False
                self.log.success('等待开播')
            return self.isRecord
        except Exception as e:
            self.log.error(str(e), self.room_id)

    def record(self, recordFilename):
        try:
            self.downloadSize = 0
            recordUrl = self.get_live_urls()[0]
            self.log.success('√ 正在录制...', self.room_id)
            headers = {
                'Accept-Encoding': 'identity',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                'Referer': re.findall(r'(https://.*\/).*\.flv', recordUrl)[0],
            }
            response = requests.get(recordUrl, stream=True, headers=headers)

            f = open(recordFilename, "ab")
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk if chunk else None)
                self.downloadSize += 1024
                if self.window.threadStop:
                    self.isRecord = False
                    break
        except Exception as e:
            f.close()
            self.isRecord = False
            self.log.error(str(e), self.room_id)

    def run(self):
        while not self.window.threadStop:
            try:
                while not self.check():
                    time.sleep(self.checkInterval)
                streamTime = datetime.now().strftime("%Y-%m-%d %H%M")
                filename_flv = os.path.join(self.recordFilePath, "{0} {1}.flv".format(streamTime, self.roomName))
                while self.isRecord and (not self.window.threadStop):
                    self.record(filename_flv)
            except Exception as e:
                self.log.error(str(e), self.room_id)
            finally:
                self.log.success('录制保存到' + filename_flv, self.room_id)

