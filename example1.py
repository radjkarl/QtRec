# -*- coding: utf-8 -*-
import sys

import QtRec
from QtRec import QtGui



class Example(QtGui.QWidget):

	def __init__(self):
		super(Example, self).__init__()
		QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
		self.setToolTip('This is a <b>QWidget</b> widget')
		self.btn = QtGui.QTableWidget(12, 3, self)

		self.btn2 = QtGui.QPushButton('Save', self)
		self.btn2.clicked.connect(QtRec.core.save)
		self.btn2.clicked.disconnect(self.btn2.logClicked)

		self.btn3 = QtGui.QLineEdit('Hello', self)
		self.btn3.move(400, 50)

		self.btn4 = QtGui.QPushButton('undo', self)
		self.btn4.move(400, 150)
		self.btn4.clicked.disconnect(self.btn4.logClicked)
		self.btn4.clicked.connect(QtRec.core.undo)

		self.btn5 = QtGui.QPushButton('redo', self)
		self.btn5.move(400, 250)
		self.btn5.clicked.connect(QtRec.core.redo)

		self.resize(600,500)
		self.setWindowTitle('Tooltips')
		self.show()


QtRec.core.log_file_name = 'mySave1.py'
QtRec.core.restore = True
QtRec.core.write_mode = 'a'

app = QtGui.QApplication(sys.argv)
win1 = Example()
#win2 = Example()


sys.exit(app.exec_())

