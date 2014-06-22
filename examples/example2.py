# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import sys

import QtRec
from QtRec import QtGui

from example1 import Example


def main():
	QtRec.log_file_name = 'mySave2.py'
	QtRec.restore = True

	app = QtGui.QApplication(sys.argv)
	win1 = Example()
	win2 = Example()
	sys.exit(app.exec_(main, locals()['main']))
	



if __name__ == '__main__':
	main()