# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filtering.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(423, 484)
        MainWindow.setMinimumSize(QtCore.QSize(423, 473))
        MainWindow.setWindowOpacity(4.0)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 50, 191, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 130, 401, 271))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.btn_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search.setGeometry(QtCore.QRect(10, 90, 191, 31))
        self.btn_search.setObjectName("btn_search")
        self.btn_back = QtWidgets.QPushButton(self.centralwidget)
        self.btn_back.setGeometry(QtCore.QRect(10, 410, 191, 31))
        self.btn_back.setObjectName("btn_back")
        self.filter0 = QtWidgets.QPushButton(self.centralwidget)
        self.filter0.setGeometry(QtCore.QRect(0, 10, 100, 30))
        self.filter0.setAutoFillBackground(False)
        self.filter0.setStyleSheet("QPushButton {background-color:\"white\"}")
        self.filter0.setObjectName("filter0")
        self.filter1 = QtWidgets.QPushButton(self.centralwidget)
        self.filter1.setGeometry(QtCore.QRect(100, 10, 100, 30))
        self.filter1.setStyleSheet("QPushButton {background-color:None}")
        self.filter1.setObjectName("filter1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 423, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Статистика"))
        self.comboBox.setItemText(0, _translate("MainWindow", "все"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "баллы"))
        self.btn_search.setText(_translate("MainWindow", "Поиск"))
        self.btn_back.setText(_translate("MainWindow", "Назад"))
        self.filter0.setText(_translate("MainWindow", "по участникам"))
        self.filter1.setText(_translate("MainWindow", "все победители"))
