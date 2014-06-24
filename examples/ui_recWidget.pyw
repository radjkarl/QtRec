
from ui_rec import Ui_MainWindow
import QtRec
from QtRec import QtGui

 #TODO:
 #show/hide-buttons gehen nicht
 #QtRec.open
 #undo und redo richten
 #alles schön benennen und dokumentieren
 
class Gui(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        # Set up the user interface from Designer.
        self.setupUi(self)
        
        # connect save, load, undo, redo with QtRec methods
        self.actionSave.triggered.connect(QtRec.core.save)
       # self.actionOpen.triggered.connect(QtRec.core.open)
        self.actionUndo.triggered.connect(QtRec.core.undo)
        self.actionRedo.triggered.connect(QtRec.core.redo)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    gui = Gui()
    gui.show()
    sys.exit(app.exec_())