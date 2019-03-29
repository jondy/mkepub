#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import json
import os
import re

from PyQt5.QtCore import QRegExp, QUrl
from PyQt5.QtGui import QTextCursor, QColor, QDesktopServices
from PyQt5.QtWidgets import QDialog, QMessageBox, QTextEdit

from ui_correct import Ui_CorrectDialog
from readers import find_reader


class CorrectDialog(QDialog, Ui_CorrectDialog):

    def __init__(self, parent):
        super(CorrectDialog, self).__init__(parent)
        self.setupUi(self)

        self.pushButtonSave.clicked.connect(self.saveFile)
        self.pushButtonApply.clicked.connect(self.applyRulers)
        self.pushButtonPreview.clicked.connect(self.previewRulers)
        self.pushButtonRedo.clicked.connect(self.textEdit.redo)
        self.pushButtonUndo.clicked.connect(self.textEdit.undo)
        self.pushButtonClearPreview.clicked.connect(self.clearPreview)

        self.pushButtonViewRuler.clicked.connect(self.viewRulers)
        self.pushButtonUpdateRuler.clicked.connect(self.loadRulers)

        self._filename = None
        self._rulers = []

    def loadFile(self, filename):
        self._filename = filename
        reader = find_reader(filename)
        reader.open(filename)
        lines = list(reader._iter_lines())
        self.textEdit.setPlainText(''.join(lines))
        reader.close()

        self.loadRulers()

    def previewRulers(self):
        plist = []
        for r in self._rulers:
            if r['type'] == 'char':
                plist.append('[{0}]'.format(r['from']))
            else:
                plist.append(r['from'])
        pat = QRegExp('|'.join(plist))
        selections = []
        self.textEdit.moveCursor(QTextCursor.Start)
        while True:
            if not self.textEdit.find(pat):
                break
            m = QTextEdit.ExtraSelection()
            m.cursor = QTextCursor(self.textEdit.textCursor())
            m.format.setBackground(QColor('#ffc107'))
            selections.append(m)
        self.textEdit.setExtraSelections(selections)

    def clearPreview(self):
        self.textEdit.setExtraSelections([])

    def applyRulers(self):
        self.clearPreview()
        text = self.textEdit.toPlainText()
        for r in self._rulers:
            if r['type'] == 'char':
                for i in range(len(r['from'])):
                    text = text.replace(r['from'][i], r['to'][i])
            else:
                pat = re.compile(r['from'], re.M)
                try:
                    text = re.sub(pat, r['to'], text)
                except Exception as e:
                    print(e, r['from'])
        self.textEdit.selectAll()
        self.textEdit.insertPlainText(text)
        # cur = self.textEdit.textCursor()
        # self.textEdit.setPlainText(text)
        self._showMessage('使用规则自动校正文本完成')

    def saveFile(self):
        self.clearPreview()
        if self._filename:
            with open(self._filename, 'w', encoding='utf-8') as f:
                f.write(self.textEdit.toPlainText())
            self._showMessage('保存成功')

    def reloadRuler(self):
        rtext = ''
        try:
            self._rulers = json.loads(rtext)
            self._showMessage('新规则已经生效')
        except Exception as e:
            self._showMessage('规则格式不正确：<br>{0}'.format(e))

    def saveRulers(self, filename):
        text = json.dumps(self._rulers, ensure_ascii=False, indent=2)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)

    def viewRulers(self):
        path = os.path.dirname(__file__)
        filename = os.path.join(path, 'rulers.txt')
        QDesktopServices.openUrl(QUrl.fromLocalFile(filename))

    def loadRulers(self):
        path = os.path.dirname(__file__)
        filename = os.path.join(path, 'rulers.txt')
        with open(filename, encoding='utf-8') as f:
            self._rulers = json.load(f)

    def _showMessage(self, msg):
        QMessageBox.information(self, '文本校正', msg)


if __name__ == '__main__':
    pass
