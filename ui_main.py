# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.horizontalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSelectDirectory = QtWidgets.QAction(MainWindow)
        self.actionSelectDirectory.setObjectName("actionSelectDirectory")
        self.actionSelectFiles = QtWidgets.QAction(MainWindow)
        self.actionSelectFiles.setObjectName("actionSelectFiles")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionStop = QtWidgets.QAction(MainWindow)
        self.actionStop.setEnabled(False)
        self.actionStop.setObjectName("actionStop")
        self.actionUpload = QtWidgets.QAction(MainWindow)
        self.actionUpload.setObjectName("actionUpload")
        self.menu_file.addAction(self.actionSelectDirectory)
        self.menu_file.addAction(self.actionSelectFiles)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.actionStart)
        self.menu_file.addAction(self.actionStop)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.actionUpload)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.actionQuit)
        self.menu.addAction(self.actionAbout)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.toolBar.addAction(self.actionSelectDirectory)
        self.toolBar.addAction(self.actionSelectFiles)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionUpload)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)
        self.actionQuit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "红云电子书制作工具"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "文件名称"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "转换状态"))
        self.menu_file.setTitle(_translate("MainWindow", "文件(&F)"))
        self.menu.setTitle(_translate("MainWindow", "帮助"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSelectDirectory.setText(_translate("MainWindow", "选择目录"))
        self.actionSelectFiles.setText(_translate("MainWindow", "选择文件"))
        self.actionSelectFiles.setToolTip(_translate("MainWindow", "选择文件"))
        self.actionQuit.setText(_translate("MainWindow", "退出"))
        self.actionAbout.setText(_translate("MainWindow", "关于"))
        self.actionStart.setText(_translate("MainWindow", "开始转换"))
        self.actionStop.setText(_translate("MainWindow", "停止转换"))
        self.actionUpload.setText(_translate("MainWindow", "上传"))
        self.actionUpload.setToolTip(_translate("MainWindow", "上传电子书到红云服务器"))
