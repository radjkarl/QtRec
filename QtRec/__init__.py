# -*- coding: utf-8 -*-
'''
Qt + save, load, undo, redo
'''

__version__ = '0.1.0'
__author__ = 'Karl Bedrich'
__email__ = 'karl@bedrich.de'
__url__ = 'http://pypi.python.org/pypi/QtRec/'
__license__ = 'GPLv3'
__description__ = __doc__
__depencies__= [
		# "PyQt4", #is not installable through pip, but
		#"PySide", # but do I really want to force people to download pyside when they have PyQt installed?
		"fancytools >= 0.1.0"
	]
__classifiers__ = [
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Intended Audience :: Other Audience',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Scientific/Engineering :: Information Analysis',
		'Topic :: Scientific/Engineering :: Visualization',
		'Topic :: Software Development :: Libraries :: Python Modules',
		]



# This module is also imported for installing the package
# Load only the second part of the init if this package is installed and
# all depencies are fulfilled
import sys
QtRec = sys.modules.get('QtRec')
if QtRec:

	try:
	    from PyQt4 import QtCore
	except ImportError:
	    try:
	        from PySide import QtCore
	    except ImportError:
	        raise Exception("QtRec requires either PyQt4 or PySide; neither package could be imported.")

	from qtRecCore import QtRecCore
	import uic
	#import QtGui
	#import QtCore
	#from qtRecUic import QtRecUic
	QtRec.core = QtRecCore()
	#uic = QtRecUic()