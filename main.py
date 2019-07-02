# !/usr/bin/python3

import sys, os, json
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout,
                             QVBoxLayout, QPushButton, QLabel,
                             QTabBar, QFrame, QStackedLayout, QTabWidget,
                             QLineEdit)
from PyQt5.QtGui import QIcon, QWindow, QImage
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWebEngineWidgets import *


class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()


class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")
        self.CreateApp()
        self.setMaximumSize(1366, 768)

    def CreateApp(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create Tabs
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.CloseTab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)

        # self.tabbar.addTab("Tab 1")
        # self.tabbar.addTab("Tab 2")

        self.tabbar.setCurrentIndex(0)

        # Keep Track Of Tabs
        self.tabCount = 0
        self.tabs = []

        # Create Address Bar
        self.Toolbar = QWidget()
        self.ToolbarLayout = QHBoxLayout()
        self.addressbar = AddressBar()

        self.Toolbar.setLayout(self.ToolbarLayout)
        self.ToolbarLayout.addWidget(self.addressbar)

        self.AddTabButton = QPushButton("+")
        self.addressbar.returnPressed.connect(self.BrowseTo)
        self.AddTabButton.clicked.connect(self.AddTab)

        self.ToolbarLayout.addWidget(self.AddTabButton)

        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)

        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.Toolbar)
        self.layout.addWidget(self.container)

        self.setLayout(self.layout)

        self.AddTab()

        self.show()

    def CloseTab(self, i):
        self.tabbar.removeTab(i)

    def AddTab(self):
        i = self.tabCount

        # set self.tabs<#> = Qwidget
        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].layout.setContentsMargins(0, 0, 0, 0)


        # For Tab Switching
        self.tabs[i].setObjectName("tab" + str(i))

        # Create  WebView within the tabs top level widget
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("https://google.com"))

        self.tabs[i].content.titleChanged.connect(lambda: self.setTabContent(i, "title"))
        self.tabs[i].content.iconChanged.connect(lambda: self.setTabContent(i, "icon"))

        # add widget to tab.layout
        self.tabs[i].layout.addWidget(self.tabs[i].content)

        # Add tabLayout to .layout
        self.tabs[i].setLayout(self.tabs[i].layout)

        # Add and Set new Tabs content to the stack widget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        # create tab on tabbar, repreasenting this tab
        # set tabData to tab<#> So it knows what self.tabs[#] it needs  to control
        self.tabbar.addTab("New Tab")
        self.tabbar.setTabData(i, {object: "tab" + str(i), "initial": i})
        self.tabbar.setCurrentIndex(i)

        self.tabCount += 1

    def SwitchTab(self, i):
        tab_data = self.tabbar.tabData(i)

        tab_content = self.findChild(QWidget, tab_data)
        self.container.layout.setCurrentWidget(tab_content)

    def BrowseTo(self):
        text = self.addressbar.text()
        i = self.tabbar.currentIndex()
        tab = self.tabbar.tabData(i)
        wv = self.findChild(QWidget, tab).content

        if "http" not in text:
            if "." not in text:
                url = "https://google.com/?q=" + text
            else:
                url = "https://" + text
        else:
            url = text

        wv.load(QUrl.fromUserInput(url))

    def SetTabContent(self, i, type):
        tab_Name = self.tabs[i].objectName()

        count = 0
        running = True

        while running:
            tab_data_name = self.tabbar.tabData(count)

            if count >= 99:
                running = False

            if tab_Name == tab_data_name["object"]:
                if type == "title":
                    newTitle = self.findChild(QWidget, tab_Name).content.title()
                    self.tabbar.setTabText(count, newTitle)
                elif type == "icon":
                    newIcon = self.findChild(QWidget, tab_Name).content.icon()
                    self.tabbar.setTabIcon(count, newIcon)

                running = False
            else:
                count += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = App()
    # until it exit run the program
    sys.exit(app.exec_())
