# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selector.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(868, 589)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(850, 530))
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tumorImage = QtWidgets.QLabel(self.frame)
        self.tumorImage.setMinimumSize(QtCore.QSize(620, 530))
        self.tumorImage.setText("")
        self.tumorImage.setScaledContents(True)
        self.tumorImage.setAlignment(QtCore.Qt.AlignCenter)
        self.tumorImage.setObjectName("tumorImage")
        self.horizontalLayout_3.addWidget(self.tumorImage)
        self.frame1 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame1.sizePolicy().hasHeightForWidth())
        self.frame1.setSizePolicy(sizePolicy)
        self.frame1.setMinimumSize(QtCore.QSize(170, 530))
        self.frame1.setMaximumSize(QtCore.QSize(170, 16777215))
        self.frame1.setBaseSize(QtCore.QSize(170, 530))
        self.frame1.setObjectName("frame1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.curDataset = QtWidgets.QLabel(self.frame1)
        self.curDataset.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.curDataset.setObjectName("curDataset")
        self.horizontalLayout.addWidget(self.curDataset)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(self.frame1)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.currentImageIndex = QtWidgets.QLabel(self.frame1)
        self.currentImageIndex.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.currentImageIndex.setObjectName("currentImageIndex")
        self.horizontalLayout_2.addWidget(self.currentImageIndex)
        self.label = QtWidgets.QLabel(self.frame1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.numOfWholeImages = QtWidgets.QLabel(self.frame1)
        self.numOfWholeImages.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numOfWholeImages.setObjectName("numOfWholeImages")
        self.horizontalLayout_2.addWidget(self.numOfWholeImages)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(17, 367, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.groupbox = QtWidgets.QGroupBox(self.frame1)
        self.groupbox.setMinimumSize(QtCore.QSize(152, 80))
        self.groupbox.setWhatsThis("")
        self.groupbox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupbox.setObjectName("groupbox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupbox)
        self.verticalLayout.setContentsMargins(10, 10, -1, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.benignButton = QtWidgets.QRadioButton(self.groupbox)
        self.benignButton.setChecked(True)
        self.benignButton.setObjectName("benignButton")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.benignButton)
        self.verticalLayout.addWidget(self.benignButton)
        self.cancerButton = QtWidgets.QRadioButton(self.groupbox)
        self.cancerButton.setObjectName("cancerButton")
        self.buttonGroup.addButton(self.cancerButton)
        self.verticalLayout.addWidget(self.cancerButton)
        self.verticalLayout_3.addWidget(self.groupbox)
        self.ambiguousCheckBox = QtWidgets.QCheckBox(self.frame1)
        self.ambiguousCheckBox.setObjectName("ambiguousCheckBox")
        self.verticalLayout_3.addWidget(self.ambiguousCheckBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.prevButton = QtWidgets.QPushButton(self.frame1)
        self.prevButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.prevButton.setObjectName("prevButton")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.prevButton)
        self.horizontalLayout_4.addWidget(self.prevButton)
        self.nextButton = QtWidgets.QPushButton(self.frame1)
        self.nextButton.setObjectName("nextButton")
        self.buttonGroup_2.addButton(self.nextButton)
        self.horizontalLayout_4.addWidget(self.nextButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3.addWidget(self.frame1)
        self.verticalLayout_4.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 868, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Dataset"))
        self.curDataset.setText(_translate("MainWindow", "0"))
        self.label_4.setText(_translate("MainWindow", "Current / Total"))
        self.currentImageIndex.setText(_translate("MainWindow", "1"))
        self.label.setText(_translate("MainWindow", "/"))
        self.numOfWholeImages.setText(_translate("MainWindow", "107"))
        self.groupbox.setTitle(_translate("MainWindow", "Type"))
        self.benignButton.setText(_translate("MainWindow", "Benign"))
        self.benignButton.setShortcut(_translate("MainWindow", "B"))
        self.cancerButton.setText(_translate("MainWindow", "Cancer"))
        self.cancerButton.setShortcut(_translate("MainWindow", "C"))
        self.ambiguousCheckBox.setText(_translate("MainWindow", "Ambiguous"))
        self.ambiguousCheckBox.setShortcut(_translate("MainWindow", "A"))
        self.prevButton.setText(_translate("MainWindow", "Prev"))
        self.prevButton.setShortcut(_translate("MainWindow", "Left"))
        self.nextButton.setText(_translate("MainWindow", "Next"))
        self.nextButton.setShortcut(_translate("MainWindow", "Right"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

