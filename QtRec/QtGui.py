# -*- coding: utf-8 -*-
'''
All classes given in this module are morking like normal QtGui classes
but are also able to record certain events named as 'logEvents'
'''



#foreign
import traceback
import sys
# get either PyQt or PySide depending on whats installed
try:
	from PyQt4 import QtGui as origQtGui
except ImportError:
	try:
		from PySide import QtGui as origQtGui
	except ImportError:
		raise Exception("QtRec requires either PyQt4 or PySide; neither package could be imported.")

from fancytools.pystructure import FallBack

#own
from qtRecBase import QtRecBase
QtRec = sys.modules['QtRec'] # get this module



class QApplication(origQtGui.QApplication):
	def exec_(self, func_to_register=None, funcLocals={}):
		'''
		connect all local attributes of a given function to it (like in methods with self.xxx
		to allow a later access
		
		Restores the saved state through executing the log-file scrips
		'''
		QtRec.core._QApp_running = True

		if func_to_register:
			QtRec.core.main_function = func_to_register
			for name, attr in funcLocals.iteritems():
				setattr(func_to_register,name, attr)
		if QtRec.core.restore:
			try:
				for line in open(QtRec.core.log_file_name,'r').readlines():
					try:
						exec(line)
					except:
						print traceback.print_exc()
			except IOError:
				pass
		origQtGui.QApplication.exec_()



class _LogButton(QtRecBase):
	'''
	Base class for all buttons to log
	'''
	def __init__(self,pclass, *args,**kwargs):
		QtRecBase.__init__(self, pclass, *args,**kwargs)
		self.logClicked = self.createLogEvent(self.click)
		self.clicked.connect(self.logClicked)
		self.save_only_last_log = False #not usefull for buttons



class QPushButton(origQtGui.QPushButton, _LogButton):
	def __init__(self, *args, **kwargs):
		_LogButton.__init__(self, origQtGui.QPushButton, *args,**kwargs)



class QLineEdit(origQtGui.QLineEdit, QtRecBase):
	
	def __init__(self, *args, **kwargs):
		QtRecBase.__init__(self, origQtGui.QLineEdit, *args,**kwargs)
		self.logTextChanged = self.createLogEvent(self.setText, init=self.text(), override=True)
		self.textChanged.connect(self.logTextChanged)



class QTableWidget(origQtGui.QTableWidget, QtRecBase):
	
	def __init__(self, *args, **kwargs):
		'''logs changing cell contents '''
		QtRecBase.__init__(self, origQtGui.QTableWidget, *args,**kwargs)
		self._registered_cells = []
		self.cellChanged.connect(self.logCellChanged)
		self.save_only_last_log = False


	def logCellChanged(self,row, col):
		if QtRec.core._do_log:
			s = '%s,%s' %(row, col)
			print s, self._registered_cells
			if s not in self._registered_cells:
				# log the empty state to be able to undo the first entry
				QtRec.core.log(self,self.setCellText, row, col, None)
				self._registered_cells.append(s)
		#	else:
			text = self.item(row, col).text()
			if text:
				QtRec.core.log(self, self.setCellText, row, col, text )


	def setCellText(self, row,col,text):
		if text == None:
			self.takeItem(row, col)
			try:
				self._registered_cells.remove('%s,%s' %(row, col))
			except ValueError:
				pass
		else:
			item = self.item(row,col)
			if not item:
				# log the empty state to be able to undo the first entry
			#	QtRec.core.log(self,self.takeItem,row, col)
				item = origQtGui.QTableWidgetItem()
				self.setItem(row,col,item)
			item.setText(text)





class _LogWindow(QtRecBase):
	'''Baseclass of QWidget and QMainWindow.
	Logs all resize and move events.'''
	def __init__(self, pClass, *args,**kwargs):
		QtRecBase.__init__(self,pClass, *args,**kwargs)
		self.resizeEvent = self.createLogEvent(
			self.setGeometry,
			lambda: self.geometry().getRect(),
			init=self.geometry().getRect(),
			override=True )
		self.moveEvent = self.createLogEvent(
			self.move,
			lambda evt: (evt.pos().x(),evt.pos().y()),
			init=(self.pos().x(), self.pos().y()),
			override=True )



class QWidget(origQtGui.QWidget, _LogWindow):
	def __init__(self, *args,**kwargs):
		_LogWindow.__init__(self, origQtGui.QWidget, *args,**kwargs)



class QMainWindow(origQtGui.QMainWindow, _LogWindow):
	def __init__(self, *args,**kwargs):
		_LogWindow.__init__(self, origQtGui.QWidget, *args,**kwargs)



class QMenu(origQtGui.QMenu, QtRecBase):
	def __init__(self, *args,**kwargs):
		QtRecBase.__init__(self, origQtGui.QMenu, *args,**kwargs)



class QSlider(origQtGui.QSlider, QtRecBase):
	'''
	Logs Slide movements'''
	def __init__(self, *args,**kwargs):
		QtRecBase.__init__(self, origQtGui.QSlider, *args,**kwargs)
		self.logSliderMoved = self.createLogEvent(
			self.setSliderPosition,
			init=self.sliderPosition(),
			override=True)
		self.sliderMoved.connect(self.logSliderMoved)


# if a called class is not existing in this module use the class of the
# normal QtGui and print an error
FallBack(__name__, origQtGui, QtRec.core.print_class_not_found)
