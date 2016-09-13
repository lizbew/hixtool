# coding: utf-8

import webbrowser
from PyQt4 import QtGui, QtCore
import psutil

import datastore

class PanelSwitcher:
    def __init__(self, stackWidget, panelMap={}):
        self.stackWidget = stackWidget
        self.panelMap = panelMap

    def show(self, title):
        if title in self.panelMap:
            self.stackWidget.setCurrentWidget(self.panelMap[title])
    
    def title_list(self):
        return self.panelMap.keys()
        

class SidebarWidget(QtGui.QWidget):

    def __init__(self, switcher, parent=None):
        super(SidebarWidget, self).__init__(parent)
        self.switcher = switcher
        self.initUi()
        
    def initUi(self):
        
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        
        for t in self.switcher.title_list():
            btn = QtGui.QPushButton(t)
            btn.clicked.connect(self.showPanel)
            vbox.addWidget(btn)
        vbox.addStretch(1)
        
    def showPanel(self):
        s = self.sender()
        # print s.metaObject().className()
        #print s.text()
        self.switcher.show(s.text())
        

class LinkButtonWidget(QtGui.QWidget):
    
    def __init__(self, title, link):
        super(LinkButtonWidget, self).__init__()
        self.title = title
        self.link = link
        
        self.initUi()
        
    def initUi(self):
        btn1 = QtGui.QPushButton(self.title)
        btn1.clicked.connect(self.open_url)
        btn1.setToolTip(self.link)
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(btn1)
        vbox.addStretch(1)
        
        self.setLayout(vbox)
        
        
    def open_url(self):
        if self.link:
            webbrowser.open(self.link)


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


class LinksPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LinksPanel, self).__init__(parent)
        self.column = 5
        self.item_count = 0
        self.initUi()

    def initUi(self):
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)

    def addLink(self, title, url):
        link_wdg = LinkButtonWidget(title, url)
        self.grid.addWidget(link_wdg, self.item_count/self.column, self.item_count % self.column)
        self.item_count += 1

    def loadFromData(self, linkList):
        for l in linkList:
            self.addLink(l['title'], l['url'])


class PasswordManagePanel(QtGui.QSplitter):
    def __init__(self, parent=None):
        super(PasswordManagePanel, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.listview = QtGui.QListView()
        self.textedit = QtGui.QTextEdit()
        self.addWidget(self.listview)
        self.addWidget(self.textedit)


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
        
        # main area: grid layout
        stackWidget = QtGui.QStackedWidget(self)
        self.setCentralWidget(stackWidget)
        
        p1 = LinksPanel(self)
        stackWidget.addWidget(p1)
        # load from data files
        try:
            data_links = datastore.get_data_with_kind('links')
            if data_links:
                p1.loadFromData(data_links)
        except Exception as e:
            print e

        # password manage panel
        pmPanel = PasswordManagePanel(self)
        stackWidget.addWidget(pmPanel)
        
        m = {
            'links': p1,
            'password': pmPanel,
        }
        

        # sidebar
        widget = SidebarWidget(PanelSwitcher(stackWidget, m), self)
        
        sidebar_title = u'分类'
        side_dock = QtGui.QDockWidget(sidebar_title)
        side_dock.setWidget(widget)
        side_dock.setObjectName(sidebar_title)
        side_dock.setFeatures(side_dock.DockWidgetFloatable|side_dock.DockWidgetMovable)
        
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, side_dock)
        
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
        #d = QtGui.QColorDialog()
        #d.open()
        QtGui.QColorDialog.getColor()

    def getCpuMemory(self):
        """获取CPU和内存状态信息"""
        cpuPercent = psutil.cpu_percent()
        memoryPercent = psutil.virtual_memory().percent
        return u'CPU使用率：%d%%   内存使用率：%d%%' % (cpuPercent, memoryPercent)    
