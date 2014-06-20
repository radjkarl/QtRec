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
		self.logClicked = self.addLogEvent(self.click)
		self.clicked.connect(self.logClicked)
		self.save_only_last_log = False #not usefull for buttons



class QPushButton(origQtGui.QPushButton, _LogButton):
	def __init__(self, *args, **kwargs):
		_LogButton.__init__(self, origQtGui.QPushButton, *args,**kwargs)



class QLineEdit(origQtGui.QLineEdit, QtRecBase):
	
	def __init__(self, *args, **kwargs):
		QtRecBase.__init__(self, origQtGui.QLineEdit, *args,**kwargs)
		self.logTextChanged = self.addLogEvent(self.setText, init=self.text(), override=True)
		self.textChanged.connect(self.logTextChanged)



class QTableWidget(origQtGui.QTableWidget, QtRecBase):
	
	def __init__(self, *args, **kwargs):
		'''logs changing cell contents '''
		QtRecBase.__init__(self, origQtGui.QTableWidget, *args,**kwargs)
	#	self._init_state = {}
	#	self._last_cell = (0,0)
		self.logCellChanged = self.addLogEvent(
			self.setCellText,
			lambda row,col,
			self=self: (row, col, self.item(row, col).text()),
			#init=self._restoreInit
			)
		self.cellChanged.connect(self.logCellChanged)
	#	self.cellChanged.connect(self._saveInitState)
		self.save_only_last_log = False


	def setCellText(self, row,col,text):
		self._last_cell = (row,col)
		item = self.item(row,col)
		if not item:
			item = origQtGui.QTableWidgetItem()
			self.setItem(row,col,item)
		item.setText(text)



	#def _saveInitState(self, row,col):
		#'''save the state of the table before user interaction'''
		#if QtRec.core._QApp_running:
			#self.cellChanged.disconnect(self._saveInitState)
		#else:
			#if not self._init_state.get(row):
				#self._init_state[row] = {}
			#self._init_state[row][col] = self.item(row, col).text()


	#def _restoreInit(self):

		#row, col = self._last_cell
		#try:
			#item = self.item(row, col)
			#item.setText(self._init_state[row][col])
		#except KeyError:
			##reset
			#item = origQtGui.QTableWidgetItem()
			#self.setItem(row,col,item)



class _LogWindow(QtRecBase):
	'''Baseclass of QWidget and QMainWindow.
	Logs all resize and move events.'''
	def __init__(self, pClass, *args,**kwargs):
		QtRecBase.__init__(self,pClass, *args,**kwargs)
		self.resizeEvent = self.addLogEvent(
			self.setGeometry,
			lambda: self.geometry().getRect(),
			init=self.geometry().getRect(),
			override=True )
		self.moveEvent = self.addLogEvent(
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
		self.logSliderMoved = self.addLogEvent(
			self.setSliderPosition,
			init=self.sliderPosition(),
			override=True)
		self.sliderMoved.connect(self.logSliderMoved)


# if a called class is not existing in this module use the class of the
# normal QtGui and print an error
FallBack(__name__, origQtGui, QtRec.core.print_class_not_found)
