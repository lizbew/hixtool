# coding: utf-8

from PyQt4 import QtGui, QtCore
import psutil

import datastore

class SidebarWidget(QtGui.QWidget):

    def __init__(self):
        super(SidebarWidget, self).__init__()
        
        self.initUi()
        
    def initUi(self):
        btn1 = QtGui.QPushButton("Links")
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addStretch(1)
        
        self.setLayout(vbox)
        

class LinkButtonWidget(QtGui.QWidget):
    
    def __init__(self, title, link):
        super(LinkButtonWidget, self).__init__()
        self.title = title
        self.link = link
        
        self.initUi()
        
    def initUi(self):
        btn1 = QtGui.QPushButton(self.title)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(btn1)
        vbox.addStretch(1)
        
        self.setLayout(vbox)


class ContainerPanel(QtGui.QWidget):
    def __init__(self):
        super(ContainerPanel, self).__init__()
        self.widgetMap = {}
        self.initUi()
        
    def initUi(self):
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)
        
    def addWidget(self):
        pass

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.initUi()
        
    def initUi(self):
        self.setWindowTitle('Test')
        self.initWidgets()
        self.initMenu()
        self.initStatusBar()
        
        
    def initWidgets(self):
        # sidebar
        widget = SidebarWidget()
        
        sidebar_title = u'分类'
        side_dock = QtGui.QDockWidget(sidebar_title)
        side_dock.setWidget(widget)
        side_dock.setObjectName(sidebar_title)
        side_dock.setFeatures(side_dock.DockWidgetFloatable|side_dock.DockWidgetMovable)
        
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, side_dock)
        
        # main area: grid layout
        centralWidget = QtGui.QWidget()
        self.setCentralWidget(centralWidget)
        
        col_num = 5
        grid = QtGui.QGridLayout()
        
        btn2 = QtGui.QPushButton('haha')
        grid.addWidget(btn2, 0, 0)
        
        link1 = LinkButtonWidget('Baidu', 'http://www.baidu.com')
        grid.addWidget(link1, 0, 1)
        
        # load from data files
        try:
            data_links = datastore.get_data_with_kind('links')
            if data_links:
                i = 3
                for lnk in data_links:
                    link_wdg = LinkButtonWidget(lnk['title'], lnk['url'])
                    grid.addWidget(link_wdg, i/col_num, i % col_num)
                    i += 1
        except Exception as e:
            print e

        centralWidget.setLayout(grid)
    
    
    def initMenu(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu(u'文件')
        
        opAction = QtGui.QAction(u'打开', self)
        opAction.triggered.connect(self.showa)
        fileMenu.addAction(opAction)
        
    def initStatusBar(self):
        self.statusLabel = QtGui.QLabel()
        self.statusLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.statusBar().addPermanentWidget(self.statusLabel)
        self.statusLabel.setText(self.getCpuMemory())
        
    def showa(self):
        pass

    def getCpuMemory(self):
        """获取CPU和内存状态信息"""
        cpuPercent = psutil.cpu_percent()
        memoryPercent = psutil.virtual_memory().percent
        return u'CPU使用率：%d%%   内存使用率：%d%%' % (cpuPercent, memoryPercent)    
