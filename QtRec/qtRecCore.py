# -*- coding: utf-8 -*-

#foreign
import __main__
#import codecs
from time import time, gmtime, strftime
#import os
#own
from fancytools.fcollections import MultiList
from fancytools.io import legalizeValues

#TODO: wie kann ich alle attribute besser dokumentieren - wenn sie hier irgendwo im quellcode liegen
#entweder: #: - damit sollten die in spinx erscheiden
#oder from variables import *
# wird sie keiner lesen...
class QtRecCore(object):
	'''
	Core functionality of QtRec including log, save, undo, redo
	'''
	def __init__(self):

		self.save_time_stamp = True #: write the time of each event in the save file
		self.save_history = True    #: Activate this if you want to save the complete history
							   #: and not just the current state
							   #: e.g. Text field:
							   #: True would save all intermediate states
							   #: False would only save the last one
		self.log_file_name = 'saved.py' #: the name of the save file
		self.restore = True		   #: should the last saved state restored when a new session is started?
	#	self.write_mode = 'w'	   #: 'w'->write || 'a'->append ... to save file
		
		self.main_function = None   #: could be the <main> function if all started from a def main
									 #: is None if all commands of the executed script are mounted
									 #: in that module and not nested in eg. a main function
									 #: see the examples for the different possible methods
		
		self.print_class_not_found = True #: in case a module is imported from QtRec.QtGui that is not existent
									 #: print a warning
		
		
		self._QApp_running = False
		self._windows = []       # list of all gui windows
		self._initArgs = {}      # {method:init_args} - stores the args for initializing/first call of a method/signal
		self._log_positions = {} # {method:[list_of_pos_in_log]}
		self._overrideLast = {}  # {method:True/False} # whether of override the last call of the same method/signal
		self._logList = MultiList('param', 'method', 'args', 'time') # this list is appended at every log event
		self._do_log = True
		self._logstep = -1       #a counter, +=1 at every log and redo event, -=1 at every undo event
		self._undone_methods = [] # a temp list filled at every undo event for corection of the log list / log positions



	def log(self, param, method, *args):
		if self._do_log and self._QApp_running:
			#if self._QApp_running:
			if len(args) == 1:
				args = args[0]
			for method,index in self._undone_methods:
					self._logList.pop(-1)
					self._log_positions[method].pop(index)
			self._undone_methods = []
			l = len(self._logList)
			if self._overrideLast.get(method) and self._logList.method and self._logList.method[-1] == method:
				self._logList[-1] = ( param, method, args, time() )
			else:
				p = self._log_positions.get(method)
				if p:
					p.append(l)
				else:
					self._log_positions[method] =  [l]
				self._logList.append( ( param, method, args, time() ) )
			self._logstep = len(self._logList) - 1


	def undo(self):
		'''remove first tableCell has add. empty undo '''
		if self._logstep >= 0:		
			self._do_log = False

			method = self._logList.method[self._logstep]

			i = self._log_positions[method].index(self._logstep)
			print method, i, self._log_positions[method], self._logstep
			self._undone_methods.append((method, i))
			if i == 0: #param has not further log-positions: set it to init value
				initargs = self._initArgs.get(method)
				if initargs!=None:
					self._execMethod(method, initargs)
			else:
				prev_param_log = self._log_positions[method][i-1]
				args = self._logList.args[prev_param_log]#TODO: ist nicht prev. sondern gleicher log
				method = self._logList.method[prev_param_log]
				self._execMethod(method, args)

			self._logstep -= 1
			self._do_log = True


	def _execMethod(self, method, args):
		#try:
		method(*args)
		#except TypeError:#not multiple args
	#		method(args)

	def redo(self):
		'TODO: doesnt work as expected'
		if self._logstep < len(self._logList):
			self._do_log = False

			method = self._logList.method[self._logstep]
			i = self._log_positions[method].index(self._logstep)
			if i != len(self._log_positions[method])-1:
				try:
					self._undone_methods.remove((method, i))
				except ValueError:
					pass
				next_param_log = self._log_positions[method][i+1]
				args = self._logList.args[next_param_log]#TODO: ist nicht prev. sondern gleicher log
				method = self._logList.method[next_param_log]
				self._execMethod(method, args)

				self._logstep += 1
			self._do_log = True


	def save(self):
		'''save the session with the given log_file_name'''
		return self.saveAs(self.log_file_name)


	def saveAs(self, logName):
		nameDict = {}
		windowDict = {}
	
		#writeHeader = not os.path.exists(logName) or self.write_mode == 'w'
		with open(logName, 'w') as logFile:
			#if writeHeader: #if new save file
			logFile.write(
'''#!/usr/bin/env python
# -*- coding: utf-8 *-*

# this file stores all method-calls though the preference-tabs
# of the Gui. Though this procedure all entries of the are stores chonologically
# This allows you to reload the whole case or to use is for following individual
# problems even without using the Gui

# The following calls were generated while using the Gui:''')
			logFile.write('\n')
			importlist = []
			for win in self._windows:
			#reset all earlier given param param names:
				self._resetLogName(win)
				windowDict[win] = self._getWindowName(win, importlist)
			if importlist:
				if len(importlist) > 1:
					importlist = str(tuple(importlist)).replace("'",'')
				else:
					importlist = importlist[0]
				logFile.write('from __main__ import %s\n\n' %importlist )
			else:
				print 'WARNING: no log-able instances found in __main__ and __main__.main'
			#for all logged methods:
			for n,(param, method, value, time) in enumerate(self._logList):
				if n == self._logstep:
					break
				last_log_pos = self._log_positions[method][-1]
				if (self.save_history or not param.save_only_last_log or last_log_pos == n):##### not param.removed and
					#do log:
					value = legalizeValues(value)
					#format time-string if wanted
					if self.save_time_stamp:
						timeName = "time='%s'" %self._timeToStr(time)
					else:
						timeName = ''
					(window,paramPath) = param.logPath()
					winName = windowDict[window]
					if param == window:
						logFile.write("%s.%s(%s) #%s\n" %(winName,method.__name__, value, timeName) )
					#if param only one time used
					elif not param._log_name and last_log_pos == n:
						#get param and exec. its method directly
						logFile.write( "%s.getLogChild(%s).%s(%s) # %s\n" %(winName,
							str(paramPath)[1:-1],method.__name__, value, timeName) )
					#else param is used multiple times - therefore it is usefull to give him a name:
					else:
						if not param._log_name:
							#no name given jet
							paramName = ''
							for p in paramPath:
								paramName += p[:4]
							n = nameDict.get(paramName)
							if not n:#paramName not used so far
								nameDict[paramName] = 1
							else:#append ParamName with individual number
								n += 1
								nameDict[paramName] = n
								paramName += str(n)
							#name the param:
							logFile.write("%s = %s.getLogChild(%s)\n" %(paramName,
								winName, str(paramPath)[1:-1]) )
							#let the param know its name
							param._log_name = paramName
						logFile.write("%s.%s(%s) #%s\n" %(paramName,method.__name__, value, timeName) )
		print "startscript: %s written" %logName


	def _getWindowName(self, master, importlist):
		for name, attr in __main__.__dict__.iteritems():
			if self.main_function and attr == self.main_function:
				for name, attr in self.main_function.__dict__.iteritems():
					if attr == master:
						if not self.main_function.__name__ in importlist:
							importlist.append(self.main_function.__name__)
						return self.main_function.__name__ +'.'+name
			if attr == master:
				importlist.append(name)
				return name


	@staticmethod
	def _timeToStr(time_since_epoch):
		'''format the time since epoch to a human readable string'''
		return strftime("%d.%m.%Y|%H:%M:%S", gmtime(time_since_epoch))


	def _resetLogName(self, inst):
		inst._log_name = False
		for child in inst.log_childs_inst.keys():
			self._resetLogName(child)