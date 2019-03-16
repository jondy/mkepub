#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import json
import logging
import os
import sys

from glob import glob

from PyQt5.QtCore import Qt, QDir, QSettings, QUrl, QFileInfo, \
    QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont, QDesktopServices, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, \
    QFileDialog, QTableWidgetItem

from transform import process_file, upload_file, save_result
from ui_main import Ui_MainWindow
from splitter import split_pdf_file, get_split_pages

COL_STATUS = 1
COL_UPLOAD = 2

__version__ = '0.1a2'


class EpubWorker(QThread):

    fileStart = pyqtSignal(int)
    fileEnd = pyqtSignal(int, dict)

    def __init__(self, filelist, parent=None):
        super(EpubWorker, self).__init__(parent)
        self.filelist = filelist
        self.request_stop = 0

    def run(self):
        row = 0
        for filename in self.filelist:
            if self.request_stop:
                break
            self.fileStart.emit(row)
            try:
                result = process_file(filename)
            except Exception as e:
                logging.exception(e)
                result = dict(err=str(e))
            self.fileEnd.emit(row, result)
            row += 1


class UploadWorker(QThread):

    fileStart = pyqtSignal(int)
    fileEnd = pyqtSignal(int, dict)

    def __init__(self, filelist, parent=None):
        super(UploadWorker, self).__init__(parent)
        self.filelist = filelist
        self.request_stop = 0

    def run(self):
        row = 0
        for filename in self.filelist:
            if self.request_stop:
                break
            self.fileStart.emit(row)
            result = upload_file(filename)
            self.fileEnd.emit(row, result)
            row += 1


class PdfSplitWorker(QThread):

    fileStart = pyqtSignal(int)
    fileEnd = pyqtSignal(int, dict)

    def __init__(self, filename, cmdlist, parent=None):
        super(PdfSplitWorker, self).__init__(parent)
        self.filename = filename
        self.cmdlist = cmdlist
        self.request_stop = 0

    def run(self):
        row = 0
        path = os.path.abspath(os.path.dirname(__file__))
        src = self.filename
        for dest, pages in self.cmdlist:
            if self.request_stop:
                break
            self.fileStart.emit(row)
            try:
                ret, msg = split_pdf_file(src, dest, pages, cwd=path)
                result = dict(err=msg) if ret else dict()
            except Exception as e:
                logging.exception(e)
                result = dict(err=str(e))
            self.fileEnd.emit(row, result)
            row += 1


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, options):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('logo.ico'))
        self._options = options

        self._settings = QSettings('Dashingsoft', 'YanHong Editor')
        self._lastPath = self._settings.value('lastPath', QDir.currentPath())

        self.actionSelectDirectory.triggered.connect(self.selectDirectory)
        self.actionSelectFiles.triggered.connect(self.selectFiles)
        self.actionStart.triggered.connect(self.startTransform)
        self.actionStop.triggered.connect(self.stopTransform)
        self.actionUpload.triggered.connect(self.uploadFiles)
        self.actionSplitPdf.triggered.connect(self.splitPdfFile)
        self.actionAbout.triggered.connect(self.about)
        self.actionHelp.triggered.connect(self.showHelp)

        self._filelist = []
        self._result = []
        self._worker = None

    def _showMessage(self, msg):
        QMessageBox.information(self, self.windowTitle(), msg)

    def _setLastPath(self, path):
        self._lastPath = path
        self._settings.setValue('lastPath', path)

    def _initFileList(self, filelist):
        w = self.tableWidget
        for i in range(w.rowCount()):
            w.removeRow(0)

        row = 0
        for filename in filelist:
            w.insertRow(row)
            w.setItem(row, 0, QTableWidgetItem(os.path.basename(filename)))
            row += 1
        w.horizontalHeader().setSectionResizeMode(3)
        self._filelist = filelist

    def selectDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, '选择目录',
                                                     self._lastPath)
        if directory:
            self._setLastPath(directory)
            filelist = glob(os.path.join(directory, '*.txt'))
            if filelist:
                self._initFileList(filelist)
            else:
                QMessageBox.information(self, '选择目录', '在选择的目录下面没有任何 .txt 文件')

    def selectFiles(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, '选择文件',
            self._lastPath, '文本文件 (*.txt)',
            options=options)

        if files:
            self._setLastPath(os.path.dirname(files[0]))
            self._initFileList(files)

    def _selectPdfFile(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, '选择文件',
            self._lastPath, 'PDF 文件 (*.pdf)',
            options=options)

        if files:
            self._setLastPath(os.path.dirname(files[0]))
            return files[0]

    def splitPdfFile(self):
        filename = self._selectPdfFile()
        if filename is None:
            return

        pagesize = self._options['pdf'].get('split_size', 20.0)
        pagelist = get_split_pages(filename, size=pagesize)
        if not pagelist:
            self._showMessage('小文件无需分割')
            return
        pagelist = ['%d-%d' % (x, y) for x, y in pagelist]

        w = self.tableWidget
        for i in range(w.rowCount()):
            w.removeRow(0)
        path = os.path.dirname(filename)
        name = os.path.splitext(os.path.basename(filename))[0]
        destlist = []
        for row in range(len(pagelist)):
            destname = '%s-%d.pdf' % (name, row + 1)
            destlist.append(os.path.join(path, destname))
            w.insertRow(row)
            w.setItem(row, 0, QTableWidgetItem(destname))

        self._splitPdf(filename, pagelist, destlist)

    def _splitPdf(self, filename, pagelist, destlist):
        worker = PdfSplitWorker(filename, zip(destlist, pagelist))
        worker.fileStart.connect(self.handleFileStart)
        worker.fileEnd.connect(self.handleFileEnd)
        worker.start()

        self._worker = worker
        self.actionStop.setEnabled(True)

    def showHelp(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile('README.html'))

    def about(self):
        QMessageBox.about(self, '关于', '延安红云平台编辑辅助工具 ' + __version__)

    def startTransform(self):
        if self._filelist:
            self._transformFiles()
        else:
            QMessageBox.information(self, self.windowTitle(), '请首先选择目录或者文件')

    def stopTransform(self):
        if self._worker:
            self._worker.request_stop = 1

    def uploadFiles(self):
        pass

    @pyqtSlot(int)
    def handleFileStart(self, row):
        w = self.tableWidget
        w.setCurrentCell(row, 0)
        w.setItem(row, COL_STATUS, QTableWidgetItem('正在生成...'))

    @pyqtSlot(int, dict)
    def handleFileEnd(self, row, result):
        w = self.tableWidget
        if 'err' in result:
            w.item(row, COL_STATUS).setText('生成失败: %s' % result['err'])
            w.item(row, COL_STATUS).setBackground(Qt.darkGray)
        else:
            w.item(row, COL_STATUS).setText('成功完成')
            w.item(row, COL_STATUS).setBackground(Qt.lightGray)
        self._result.append(result)

    @pyqtSlot()
    def handleWorkerFinished(self):
        self.tableWidget.setCurrentItem(None)
        if not self._worker.request_stop:
            output = save_result(self._filelist, self._result)
            msg = ('文件转换完成，所有文件存放在目录：',
                   os.path.abspath('output'), '',
                   '上传列表已经保存在文件: %s, 是否查看?' % output)
            reply = QMessageBox.question(self,
                                         self.windowTitle(),
                                         '<br>'.join(msg))
            if reply == QMessageBox.Yes:
                QDesktopServices.openUrl(
                    QUrl.fromLocalFile(QFileInfo(output).absoluteFilePath()))
        self._worker = None
        self.actionStart.setEnabled(True)
        self.actionStop.setEnabled(False)

    def _transformFiles(self):
        worker = EpubWorker(self._filelist, parent=self)
        worker.fileStart.connect(self.handleFileStart)
        worker.fileEnd.connect(self.handleFileEnd)
        worker.finished.connect(self.handleWorkerFinished)
        worker.start()

        self._worker = worker
        self.actionStart.setEnabled(False)
        self.actionStop.setEnabled(True)


def main():
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'config.json')) as f:
        conf = json.load(f)
        
    app = QApplication(sys.argv)
    font = QFont('宋体')
    pointsize = font.pointSize()
    font.setPixelSize(pointsize*90/72)
    app.setFont(font)

    window = MainWindow(conf)
    window.show()

    try:
        ret = app.exec_()
    except Exception as e:
        QMessageBox.critical(window, window.windowTitle(), str(e))
        if sys.flags.debug:
            raise
        ret = -1
    sys.exit(ret)


if __name__ == '__main__':
    main()
