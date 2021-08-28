import os
import sys

from libs.flv2mp4 import flv2mp4
from libs.record import record
from Log.Logger import Logger
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QStyleFactory

from window import Ui_MainWindow

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_RECORD_FILE_PATH = os.path.join(ROOT_PATH, "recordFiles")
DEFAULT_FFMPEG = os.path.join(ROOT_PATH, "libs/ffmpeg.exe")

class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        if not os.path.exists(DEFAULT_RECORD_FILE_PATH):
            os.makedirs(DEFAULT_RECORD_FILE_PATH)
        self.recordSavePath = DEFAULT_RECORD_FILE_PATH
        self.recordFile = None
        self.sourceFile = None
        self.targetPath = None
        self.liveSavePath.setPlaceholderText(self.recordSavePath)
        self.log = Logger(ROOT_PATH, self)
        self.threadStop = False

        self.log.success("程序启动")

    ######## 录制部分 ############

    def selectRecordSavePath_clicked(self):
        self.recordSavePath= QFileDialog.getExistingDirectory(self, "选择保存路径")
        self.liveSavePath.setText(self.recordSavePath)

    def startRecord_clicked(self):
        self.threadStop = False
        recorder = record(self)
        recorder.start()
    
    def stopRecord_clicked(self):
        self.threadStop = True

    ######## 录制部分 ############
    
    ######## 转码部分 ############

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
            if not os.path.exists(DEFAULT_FFMPEG):
                raise Exception("ffmpeg.exe未找到，请检查本程序所在目录的libs下是否有ffmpeg.exe")
            if not self.sourceFile :
                raise Exception("文件错误")
            elif self.sourceFile.split(".")[-1] != "flv":
                raise Exception("源文件不是flv格式，请重新选择")
            else:
                self.log.success("源文件--->"+self.sourceFile)
            temp = self.rebuildTargetPath.text()
            self.targetPath = temp if not temp == "" else self.targetPath
            targetFile = os.path.join(self.targetPath, self.sourceFile.split("/")[-1].split(".")[0]+".mp4")
            flv2mp4(DEFAULT_FFMPEG, self.sourceFile, targetFile)
            self.log.success("转码完成，文件保存到"+targetFile)
        except Exception as e:
            self.log.error(str(e))

    ######## 转码部分 ############
     
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


