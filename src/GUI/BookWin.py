# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BookWin.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(730, 413)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelHeader = QtWidgets.QLabel(self.centralwidget)
        self.labelHeader.setGeometry(QtCore.QRect(30, 20, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelHeader.setFont(font)
        self.labelHeader.setObjectName("labelHeader")
        self.btnAddBook = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddBook.setGeometry(QtCore.QRect(20, 320, 201, 51))
        self.btnAddBook.setObjectName("btnAddBook")
        self.btnSelectFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnSelectFile.setGeometry(QtCore.QRect(480, 340, 210, 31))
        self.btnSelectFile.setObjectName("btnSelectFile")
        self.labelPicture = QtWidgets.QLabel(self.centralwidget)
        self.labelPicture.setGeometry(QtCore.QRect(480, 60, 210, 260))
        self.labelPicture.setText("")
        self.labelPicture.setObjectName("labelPicture")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(160, 70, 291, 221))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEditTitle = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditTitle.setObjectName("lineEditTitle")
        self.verticalLayout.addWidget(self.lineEditTitle)
        self.lineEditAuthor = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditAuthor.setObjectName("lineEditAuthor")
        self.verticalLayout.addWidget(self.lineEditAuthor)
        self.lineEditPublisher = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditPublisher.setObjectName("lineEditPublisher")
        self.verticalLayout.addWidget(self.lineEditPublisher)
        self.lineEditDate = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEditDate.setObjectName("lineEditDate")
        self.verticalLayout.addWidget(self.lineEditDate)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 80, 125, 201))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelTitle = QtWidgets.QLabel(self.layoutWidget1)
        self.labelTitle.setObjectName("labelTitle")
        self.verticalLayout_2.addWidget(self.labelTitle)
        self.labelAuthor = QtWidgets.QLabel(self.layoutWidget1)
        self.labelAuthor.setObjectName("labelAuthor")
        self.verticalLayout_2.addWidget(self.labelAuthor)
        self.labelPublisher = QtWidgets.QLabel(self.layoutWidget1)
        self.labelPublisher.setObjectName("labelPublisher")
        self.verticalLayout_2.addWidget(self.labelPublisher)
        self.labelDate = QtWidgets.QLabel(self.layoutWidget1)
        self.labelDate.setObjectName("labelDate")
        self.verticalLayout_2.addWidget(self.labelDate)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Adding Book"))
        self.labelHeader.setText(_translate("MainWindow", "Add a new book"))
        self.btnAddBook.setText(_translate("MainWindow", "Add"))
        self.btnSelectFile.setText(_translate("MainWindow", "Select file"))
        self.labelTitle.setText(_translate("MainWindow", "Title :"))
        self.labelAuthor.setText(_translate("MainWindow", "Author :"))
        self.labelPublisher.setText(_translate("MainWindow", "Publisher :"))
        self.labelDate.setText(_translate("MainWindow", "Publication date :"))
