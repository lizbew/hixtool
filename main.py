# coding: utf-8

import sys
from PyQt4 import QtGui, QtCore
from uiMainWindow import MainWindow

def main():
    reload(sys)
    sys.setdefaultencoding('utf8')
    
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('vnpy.ico'))
    #app.setFont(BASIC_FONT)
    
    # import qdarkstyle
    # app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    
    mainWindow = MainWindow()
    mainWindow.showMaximized()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()
