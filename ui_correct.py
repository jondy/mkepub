# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_correct.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CorrectDialog(object):
    def setupUi(self, CorrectDialog):
        CorrectDialog.setObjectName("CorrectDialog")
        CorrectDialog.resize(1099, 794)
        self.horizontalLayout = QtWidgets.QHBoxLayout(CorrectDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(CorrectDialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(CorrectDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButtonPreview = QtWidgets.QPushButton(self.frame)
        self.pushButtonPreview.setObjectName("pushButtonPreview")
        self.verticalLayout_2.addWidget(self.pushButtonPreview)
        self.pushButtonClearPreview = QtWidgets.QPushButton(self.frame)
        self.pushButtonClearPreview.setObjectName("pushButtonClearPreview")
        self.verticalLayout_2.addWidget(self.pushButtonClearPreview)
        self.pushButtonApply = QtWidgets.QPushButton(self.frame)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.verticalLayout_2.addWidget(self.pushButtonApply)
        self.pushButtonRedo = QtWidgets.QPushButton(self.frame)
        self.pushButtonRedo.setObjectName("pushButtonRedo")
        self.verticalLayout_2.addWidget(self.pushButtonRedo)
        self.pushButtonUndo = QtWidgets.QPushButton(self.frame)
        self.pushButtonUndo.setObjectName("pushButtonUndo")
        self.verticalLayout_2.addWidget(self.pushButtonUndo)
        self.pushButtonSave = QtWidgets.QPushButton(self.frame)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.verticalLayout_2.addWidget(self.pushButtonSave)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.pushButtonClose = QtWidgets.QPushButton(self.frame)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.verticalLayout_2.addWidget(self.pushButtonClose)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.pushButtonViewRuler = QtWidgets.QPushButton(self.frame)
        self.pushButtonViewRuler.setObjectName("pushButtonViewRuler")
        self.verticalLayout_2.addWidget(self.pushButtonViewRuler)
        self.pushButtonUpdateRuler = QtWidgets.QPushButton(self.frame)
        self.pushButtonUpdateRuler.setObjectName("pushButtonUpdateRuler")
        self.verticalLayout_2.addWidget(self.pushButtonUpdateRuler)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(CorrectDialog)
        self.pushButtonClose.clicked.connect(CorrectDialog.close)
        QtCore.QMetaObject.connectSlotsByName(CorrectDialog)

    def retranslateUi(self, CorrectDialog):
        _translate = QtCore.QCoreApplication.translate
        CorrectDialog.setWindowTitle(_translate("CorrectDialog", "校对文本文件"))
        self.pushButtonPreview.setText(_translate("CorrectDialog", "预览"))
        self.pushButtonClearPreview.setText(_translate("CorrectDialog", "清除"))
        self.pushButtonApply.setText(_translate("CorrectDialog", "应用"))
        self.pushButtonRedo.setText(_translate("CorrectDialog", "Redo"))
        self.pushButtonUndo.setText(_translate("CorrectDialog", "Undo"))
        self.pushButtonSave.setText(_translate("CorrectDialog", "保存"))
        self.pushButtonClose.setText(_translate("CorrectDialog", "关闭"))
        self.pushButtonViewRuler.setText(_translate("CorrectDialog", "查看规则"))
        self.pushButtonUpdateRuler.setText(_translate("CorrectDialog", "更新规则"))

