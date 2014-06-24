from PyQt4.uic import compileUi
from QtRec.uic import insertRec

def build(): 
    with open('ui_normal.py', 'w') as pyGui:
        compileUi('ui_normal.ui', pyGui)
    #with open('ui_normal.py', 'r') as pyGui:
    insertRec('_rec', 'ui_normal.py', 'ui_rec.py')



if __name__ == '__main__':
    build()
    