#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import json
import re

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QTextCursor
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
        self.pushButtonResetRuler.clicked.connect(self.resetRuler)
        self.pushButtonReloadRuler.clicked.connect(self.reloadRuler)
        self.pushButtonClearPreview.clicked.connect(self.clearPreview)

        self._filename = None
        self._defaultRulers = []
        self._rulers = []

    def loadFile(self, filename, rulers=[]):
        self._filename = filename
        self._defaultRulers = rulers[:]
        self.resetRuler()
        reader = find_reader(filename)
        reader.open(filename)
        lines = list(reader._iter_lines())
        self.textEdit.setPlainText(''.join(lines))
        reader.close()

    def previewRulers(self):
        plist = []
        for r in self._rulers:
            if r['type'] == 'char':
                plist.append('[{0}]'.format(r['from']))
            else:
                plist.extend(r['from'])
        pat = QRegExp('|'.join(plist))
        selections = []
        self.textEdit.moveCursor(QTextCursor.Start)
        while True:
            if not self.textEdit.find(pat):
                break
            m = QTextEdit.ExtraSelection()
            m.cursor = QTextCursor(self.textEdit.textCursor())
            m.format.setBackground(Qt.yellow)
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
                    text = re.sub(r['from'][i], r['to'][i], text)
            else:
                for i in range(len(r['from'])):
                    pat = re.compile(r['from'][i], re.M)
                    text = re.sub(pat, r['to'][i], text)

        self.textEdit.setPlainText(text)
        self._showMessage('使用规则自动校正文本完成')

    def saveFile(self):
        self.clearPreview()
        if self._filename:
            with open(self._filename, 'w', encoding='utf-8') as f:
                f.write(self.textEdit.toPlainText())
            self._showMessage('保存成功')

    def reloadRuler(self):
        text = self.plainTextEdit.toPlainText()
        try:
            self._rulers = json.loads(text)
            self._showMessage('新规则已经生效')
        except Exception as e:
            self._showMessage('规则格式不正确：<br>{0}'.format(e))

    def resetRuler(self):
        self._rulers = self._defaultRulers[:]
        text = json.dumps(self._rulers, ensure_ascii=False, indent=2)
        self.plainTextEdit.setPlainText(text)

    def _showMessage(self, msg):
        QMessageBox.information(self, '文本校正', msg)


if __name__ == '__main__':
    pass
