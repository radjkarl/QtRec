# -*- coding: utf-8 -*-
import sys
QtRec = sys.modules['QtRec'] # get this module
from fancytools.utils import incrementName

class QtRecBase(object):
	'''
	Baseclass for all QtRec widgets.
	'''
	def __init__(self, origQtGuiClass, *args, **kwargs):
		self.save_only_last_log = True  #means: only the last log event would be
										#saved if not QtRec.save_history
		self.log_childs_inst = {}
		self.log_childs_name = {}
		self._logparent = None
		# take the log-name if given, elsewise use the class name
		name = kwargs.get('logname')
		if name:
			kwargs.pop('logname')
		else:
			name = self.__class__.__name__
		# for logging it's sometimes more usefull to use a instance-parent
		# than given through self.parent()
		p = kwargs.get('logparent')
		if p:
			self._logparent = p
			kwargs.pop('logparent')
		# init base class here after all foreign contents from kwargs are removed
		origQtGuiClass.__init__(self, *args, **kwargs)

		if not p:
			p = self.parent()
		if p:
			while p:
				# find closest parent that is an instance of QtRecBase
				# add this instance as child with an individual name to that
				# parents log-child-list
				#TODO1 invalid widget überspringen - wenn es keinen valid parent gibt: fehlermeldung
				if isinstance(p,QtRecBase):
					name = incrementName(p.log_childs_name.keys(), name)
					p.log_childs_inst[self] = name
					p.log_childs_name[name] = self
					break
				p = p.parent()
		#the top QGuiObject must be a window
		elif self == self.window():
			# add this window to the windows known by QtRec
			QtRec.core._windows.append(self)
		else:
			raise NameError('parent not given')


	def registerLogMethod(self, methodToLog, **kwargs):
		QtRec.core._log_positions[methodToLog] = []
		initArgs = kwargs.get('init')
		if initArgs:
			QtRec.core._initArgs[methodToLog] = initArgs
		override = kwargs.get('override')	
		if override:
			QtRec.core._overrideLast[methodToLog] = override


	#def createLogEvent2(self, method, signal):
	#		signal.connect(method)
	#		QtRec.core._log_signals[method] = signal



	def createLogEvent(self, methodToLog, getArgsMethod=None, **kwargs):
		#TODO: darauf hinweisen das das nur ne faule methode is
		'''
		add a class method here to log it everytime when called (implies registerLogMethod)
		
		getArgsMethod - function or list of functions to get the arguments for the methodToLog
				can also be a list of strings containing arguments emmited by the signal
				those args have to be formated like ARG or ARG0...9 for multiple args
				e.q.	[ 'ARG1.size().width()','ARG2.size().height()' ]
		override=True, default:False # whether each log event should override the last one
		init=(one or multiple init values given to the methodToLog, can also be a callable
		      to execute to return to the initial state)
		'''
		self.registerLogMethod(methodToLog, **kwargs)
		if not getArgsMethod:
			m = lambda args: QtRec.core.log(self, methodToLog, args) if QtRec.core._do_log else None
		elif not getArgsMethod.__code__.co_argcount: # lambda that takes no arguments
			m = lambda evt: QtRec.core.log(self, methodToLog, *getArgsMethod() ) if QtRec.core._do_log else None
		else:
			m = lambda *evt: QtRec.core.log(self, methodToLog, *getArgsMethod(*evt) ) if QtRec.core._do_log else None

# 		ev = kwargs.get('event')
# 		if ev:
# 			ev.connect(m)
# 			QtRec.core._log_signals[methodToLog] = ev
# 			QtRec.core._log_event_methods[methodToLog] = m
		return m

	def getLogChild(self, *names):
		'''
		return the instance of a log-child by given name
		multiple namnes are given iterate though the log-child-hirarchy and return
		the last one
		'''
		if names and names[0]:
			return self.log_childs_name[names[0]].getLogChild(names[1:])
		else:
			return self


	def logPath(self):
		'''
		return the window and the path down to be this instance
		'''
		window = self
		parent = self
		path = []
		while True: #the parent of the top-structure will be None
			#determine arg-name of child in parent:
			if parent._logparent:
				parent = parent._logparent
			else:
				parent = parent.parent()
			if not parent:
				break

			try:
				name = parent.log_childs_inst[window]
				path.insert(0,name)
			except AttributeError:
				pass # skip, if a parent is not instance of QtRecBase
			window = parent
		return window,path