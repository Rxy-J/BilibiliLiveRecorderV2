import os
import sys
import json
import re
import time
import requests

from libs.flv2mp4 import flv2mp4
from Log.Log import Log
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QStyleFactory

from window import Ui_MainWindow

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.recordSavePath = None
        self.recordFile = None
        self.sourceFile = None
        self.targetPath = None
        self.liveSavePath.setPlaceholderText(ROOT_PATH)

        self.log = Log(ROOT_PATH, self)
        self.log.success("程序启动")


    def selectRecordSavePath_clicked(self):
        self.recordSavePath= QFileDialog.getExistingDirectory(self, "选择保存路径")
        self.liveSavePath.setText(self.recordSavePath)

    def start
    
    def selectSourceFile_clicked(self):
        self.sourceFile = QFileDialog.getOpenFileName(self, "选择要转换的文件")[0]
        self.rebuildSourceFilePath.setText(self.sourceFile)
        self.targetPath = "/".join(self.sourceFile.split("/")[:-1])
        self.rebuildTargetPath.setPlaceholderText(self.targetPath)
        self.log.success("源文件："+self.sourceFile)
        self.log.success("已设置默认保存目录为"+self.targetPath)

    def selectTargetPath_clicked(self):
        self.targetPath = QFileDialog.getExistingDirectory(self, "选择保存路径")
        self.rebuildTargetPath.setText(self.targetPath)
    
    def startRebuild_clicked(self):
        try:
            self.sourceFile = self.rebuildSourceFilePath.text()
            if not self.sourceFile :
                raise Exception("文件错误")
            elif self.sourceFile.split(".")[-1] != "flv":
                raise Exception("源文件不是flv格式，请重新选择")
            else:
                self.log.success("源文件--->"+self.sourceFile)
            temp = self.rebuildTargetPath.text()
            self.targetPath = temp if not temp == "" else self.targetPath
            targetFile = os.path.join(self.targetPath, self.sourceFile.split("/")[-1].split(".")[0]+".mp4")
            flv2mp4(self.sourceFile, targetFile)
            self.log.success("转码完成，文件保存到"+targetFile)
        except Exception as e:
            self.log.error(str(e))

    def startRecord_clicked(self):
        self.liveRoomId = self.liveNumber.text()
        if self.liveRoomId == "1":
            self.log.error("房间号错误")

        #######
        try:
            if not os.path.exists(RECORD_FILE_PATH) :
                os.mkdir(RECORD_FILE_PATH)
            if not os.path.exists(FFMPEG):
                raise Exception("ffmpeg.exe未找到，请检查本程序所在目录下是否有ffmpeg.exe")
            with open(REAL_PATH+"/config.json") as f:
                data = json.load(f)
            recorder = BiliBiliLiveRecorder(data["room_id"])
            monitor = Monitor(recordThread=recorder)
            print("Bilibili Live Recorder v{}".format(VERSION))
            print("Powered by Python")
            recorder.start()
            monitor.start()
            recorder.join()
            monitor.join()
        except Exception as e:
            print(str(e)+"==>"+str(e.__traceback__.tb_lineno))
#######################
        
    def clearInfo_clicked(self):
        self.messager.clear()

    def exit_clicked(self):
        self.log.success("程序退出")
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())