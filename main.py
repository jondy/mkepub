#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys

from glob import glob

from PyQt5.QtCore import Qt, QDir, QSettings, QUrl, QFileInfo, \
    QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, \
    QFileDialog, QTableWidgetItem

from ui_main import Ui_MainWindow

# from transform import process_file, save_result

from openpyxl import load_workbook


def save_result(result, filename=None):
    filename = 'upload-yyyy-mm-dd-hh-mi-ss.xlsx'
    template = os.path.join(os.path.dirname(__file__), 'upload.xltx')
    wb = load_workbook(template)
    wb.template = False

    start_row = 4
    filename_col = 'A'
    page_col = 'C'
    total_col = 'D'
    non_blank_col = 'E'
    han_col = 'F'
    price_col = 'G'
    price = 450.0
    money_col = 'H'
    money_formula = '=F{row}/1000*G{row}'

    ws = wb.active
    row = start_row
    for name, counter in result:
        if counter is None:
            continue
        page, total, han, blank = counter
        rs = str(row)
        ws[filename_col + rs] = os.path.basename(name)
        ws[page_col + rs] = page
        ws[total_col + rs] = total
        ws[non_blank_col + rs] = total - blank
        ws[han_col + rs] = han
        ws[price_col + rs] = price
        ws[money_col + rs] = money_formula.format(row=row)
        row += 1

    sum_formula = '=sum({col}%d:{col}%d)' % (start_row, row-1)
    rs = str(row)
    ws[filename_col + rs] = '总计'
    ws[page_col + rs] = sum_formula.format(col=page_col)
    ws[total_col + rs] = sum_formula.format(col=total_col)
    ws[non_blank_col + rs] = sum_formula.format(col=non_blank_col)
    ws[han_col + rs] = sum_formula.format(col=han_col)
    ws[money_col + rs] = sum_formula.format(col=money_col)

    wb.save(filename)
    wb.close()

    return filename


def process_file(filename):
    pass


class CountWorker(QThread):

    fileStart = pyqtSignal(int)
    fileEnd = pyqtSignal(int, tuple)

    def __init__(self, filelist, parent=None):
        super(CountWorker, self).__init__(parent)
        self.filelist = filelist

    def run(self):
        row = 0
        for filename in self.filelist:
            self.fileStart.emit(row)
            result = process_file(filename)
            self.fileEnd.emit(row, result)
            row += 1


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self._settings = QSettings('Dashingsoft', 'Word-Counter')
        self._lastPath = self._settings.value('lastPath', QDir.currentPath())

        self.actionAbout.triggered.connect(self.about)
        self.actionCountDirectory.triggered.connect(self.countDirectory)
        self.actionCountFile.triggered.connect(self.countFile)
        self.actionAbout.triggered.connect(self.about)

        self._filelist = []

    def _setLastPath(self, path):
        self._lastPath = path
        self._settings.setValue('lastPath', path)

    def countDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, '选择目录',
                                                     self._lastPath)
        if directory:
            self._setLastPath(directory)
            filelist = glob(os.path.join(directory, '*.xlsx'))
            if filelist:
                self._countFiles(filelist)

    def countFile(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, '选择统计文件',
            self._lastPath, 'Excel 2007(*.xlsx)',
            options=options)

        if files:
            self._setLastPath(os.path.dirname(files[0]))
            self._countFiles(files)

    def about(self):
        QMessageBox.about(self, '关于', '中文字符统计工具')

    @pyqtSlot(int)
    def handleFileStart(self, row):
        w = self.tableWidget
        w.setCurrentCell(row, 0)
        w.setItem(row, 4, QTableWidgetItem('正在统计...'))

    @pyqtSlot(int, tuple)
    def handleFileEnd(self, row, result):
        w = self.tableWidget
        if result is None:
            w.item(row, 4).setText('统计失败')
            w.item(row, 4).setBackground(Qt.red)
        else:
            w.setItem(row, 1, QTableWidgetItem(str(result[1])))
            w.setItem(row, 2, QTableWidgetItem(str(result[3])))
            w.setItem(row, 3, QTableWidgetItem(str(result[2])))
            w.item(row, 4).setText('统计完成')
            w.item(row, 4).setBackground(Qt.lightGray)
        filename = self._filelist[row]
        self._filelist[row] = os.path.basename(filename), result

    @pyqtSlot()
    def handleWorkerFinished(self):
        self.tableWidget.setCurrentItem(None)

        output = save_result(self._filelist)
        reply = QMessageBox.question(
            self, '统计结束', '统计结果已经保存在文件: %s, 是否查看?' % output)
        if reply == QMessageBox.Yes:
            QDesktopServices.openUrl(
                QUrl.fromLocalFile(QFileInfo(output).absoluteFilePath()))

    def _countFiles(self, filelist):
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
        worker = CountWorker(filelist, parent=self)
        worker.fileStart.connect(self.handleFileStart)
        worker.fileEnd.connect(self.handleFileEnd)
        worker.finished.connect(self.handleWorkerFinished)
        worker.start()


def main():
    app = QApplication(sys.argv)
    font = QFont('宋体')
    pointsize = font.pointSize()
    font.setPixelSize(pointsize*90/72)
    app.setFont(font)

    window = MainWindow()
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
