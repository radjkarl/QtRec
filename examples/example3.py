# -*- coding: utf-8 -*-
import sys

import QtRec
from QtRec import QtGui

from example1 import Example


def main():
	QtRec.log_file_name = 'mySave3.py'
	QtRec.restore = True
	
	main.win1 = Example()
	main.win2 = Example()
	sys.exit(app.exec_())



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	win3 = Example()
	main()