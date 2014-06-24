# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_normal.ui'
#
# Created: Sun Jun 22 22:19:12 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(543, 520)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton_2_rec = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2_rec.setGeometry(QtCore.QRect(370, 110, 98, 27))
        self.pushButton_2_rec.setObjectName(_fromUtf8("pushButton_2_rec"))
        self.pushButton_rec = QtGui.QPushButton(self.centralwidget)
        self.pushButton_rec.setGeometry(QtCore.QRect(370, 50, 98, 27))
        self.pushButton_rec.setObjectName(_fromUtf8("pushButton_rec"))
        self.tableWidget_rec = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget_rec.setGeometry(QtCore.QRect(70, 210, 256, 192))
        self.tableWidget_rec.setObjectName(_fromUtf8("tableWidget_rec"))
        self.tableWidget_rec.setColumnCount(0)
        self.tableWidget_rec.setRowCount(0)
        self.textEdit_rec = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_rec.setGeometry(QtCore.QRect(350, 320, 104, 78))
        self.textEdit_rec.setObjectName(_fromUtf8("textEdit_rec"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 543, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSave = QtGui.QMenu(self.menubar)
        self.menuSave.setObjectName(_fromUtf8("menuSave"))
        MainWindow.setMenuBar(self.menubar)
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionUndo = QtGui.QAction(MainWindow)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionRedo = QtGui.QAction(MainWindow)
        self.actionRedo.setObjectName(_fromUtf8("actionRedo"))
        self.menuSave.addAction(self.actionSave)
        self.menuSave.addAction(self.actionOpen)
        self.menuSave.addAction(self.actionUndo)
        self.menuSave.addAction(self.actionRedo)
        self.menubar.addAction(self.menuSave.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_2_rec.setText(_translate("MainWindow", "show", None))
        self.pushButton_rec.setText(_translate("MainWindow", "hide", None))
        self.menuSave.setTitle(_translate("MainWindow", "File", None))
        self.actionSave.setText(_translate("MainWindow", "save", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionOpen.setText(_translate("MainWindow", "open", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionUndo.setText(_translate("MainWindow", "undo", None))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z", None))
        self.actionRedo.setText(_translate("MainWindow", "redo", None))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Y", None))

