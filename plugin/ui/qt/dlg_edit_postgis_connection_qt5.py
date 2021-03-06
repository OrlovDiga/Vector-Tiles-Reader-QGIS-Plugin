# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/dlg_edit_postgis_connection.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgEditPostgisConnection(object):
    def setupUi(self, DlgEditPostgisConnection):
        DlgEditPostgisConnection.setObjectName("DlgEditPostgisConnection")
        DlgEditPostgisConnection.resize(523, 253)
        self.gridLayout = QtWidgets.QGridLayout(DlgEditPostgisConnection)
        self.gridLayout.setObjectName("gridLayout")
        self.btnCancel = QtWidgets.QPushButton(DlgEditPostgisConnection)
        self.btnCancel.setObjectName("btnCancel")
        self.gridLayout.addWidget(self.btnCancel, 1, 2, 1, 1)
        self.btnSave = QtWidgets.QPushButton(DlgEditPostgisConnection)
        self.btnSave.setObjectName("btnSave")
        self.gridLayout.addWidget(self.btnSave, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.Connection = QtWidgets.QGroupBox(DlgEditPostgisConnection)
        self.Connection.setObjectName("Connection")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Connection)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.txtpgName = QtWidgets.QLineEdit(self.Connection)
        self.txtpgName.setObjectName("txtpgName")
        self.gridLayout_2.addWidget(self.txtpgName, 0, 2, 1, 1)
        self.lblpgHost = QtWidgets.QLabel(self.Connection)
        self.lblpgHost.setObjectName("lblpgHost")
        self.gridLayout_2.addWidget(self.lblpgHost, 1, 0, 1, 1)
        self.lblpgUsername = QtWidgets.QLabel(self.Connection)
        self.lblpgUsername.setObjectName("lblpgUsername")
        self.gridLayout_2.addWidget(self.lblpgUsername, 3, 0, 1, 1)
        self.txtpgUsername = QtWidgets.QLineEdit(self.Connection)
        self.txtpgUsername.setObjectName("txtpgUsername")
        self.gridLayout_2.addWidget(self.txtpgUsername, 3, 2, 1, 1)
        self.lblpgPort = QtWidgets.QLabel(self.Connection)
        self.lblpgPort.setObjectName("lblpgPort")
        self.gridLayout_2.addWidget(self.lblpgPort, 2, 0, 1, 1)
        self.txtpgHost = QtWidgets.QLineEdit(self.Connection)
        self.txtpgHost.setObjectName("txtpgHost")
        self.gridLayout_2.addWidget(self.txtpgHost, 1, 2, 1, 1)
        self.lblpgDatabase = QtWidgets.QLabel(self.Connection)
        self.lblpgDatabase.setObjectName("lblpgDatabase")
        self.gridLayout_2.addWidget(self.lblpgDatabase, 5, 0, 1, 1)
        self.lblpgPassword = QtWidgets.QLabel(self.Connection)
        self.lblpgPassword.setObjectName("lblpgPassword")
        self.gridLayout_2.addWidget(self.lblpgPassword, 4, 0, 1, 1)
        self.lblpgName = QtWidgets.QLabel(self.Connection)
        self.lblpgName.setObjectName("lblpgName")
        self.gridLayout_2.addWidget(self.lblpgName, 0, 0, 1, 1)
        self.txtpgPassword = QtWidgets.QLineEdit(self.Connection)
        self.txtpgPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtpgPassword.setObjectName("txtpgPassword")
        self.gridLayout_2.addWidget(self.txtpgPassword, 4, 2, 1, 1)
        self.chkpgStorePassword = QtWidgets.QCheckBox(self.Connection)
        self.chkpgStorePassword.setChecked(True)
        self.chkpgStorePassword.setObjectName("chkpgStorePassword")
        self.gridLayout_2.addWidget(self.chkpgStorePassword, 6, 0, 1, 3)
        self.spinpgPort = QtWidgets.QSpinBox(self.Connection)
        self.spinpgPort.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinpgPort.setMinimum(0)
        self.spinpgPort.setMaximum(65535)
        self.spinpgPort.setObjectName("spinpgPort")
        self.gridLayout_2.addWidget(self.spinpgPort, 2, 2, 1, 1)
        self.txtpgDatabase = QtWidgets.QLineEdit(self.Connection)
        self.txtpgDatabase.setObjectName("txtpgDatabase")
        self.gridLayout_2.addWidget(self.txtpgDatabase, 5, 2, 1, 1)
        self.gridLayout.addWidget(self.Connection, 0, 0, 1, 3)

        self.retranslateUi(DlgEditPostgisConnection)
        self.btnCancel.clicked.connect(DlgEditPostgisConnection.reject)
        self.btnSave.clicked.connect(DlgEditPostgisConnection.accept)
        QtCore.QMetaObject.connectSlotsByName(DlgEditPostgisConnection)
        DlgEditPostgisConnection.setTabOrder(self.txtpgName, self.txtpgHost)
        DlgEditPostgisConnection.setTabOrder(self.txtpgHost, self.spinpgPort)
        DlgEditPostgisConnection.setTabOrder(self.spinpgPort, self.txtpgUsername)
        DlgEditPostgisConnection.setTabOrder(self.txtpgUsername, self.txtpgPassword)
        DlgEditPostgisConnection.setTabOrder(self.txtpgPassword, self.chkpgStorePassword)
        DlgEditPostgisConnection.setTabOrder(self.chkpgStorePassword, self.btnSave)
        DlgEditPostgisConnection.setTabOrder(self.btnSave, self.btnCancel)

    def retranslateUi(self, DlgEditPostgisConnection):
        _translate = QtCore.QCoreApplication.translate
        DlgEditPostgisConnection.setWindowTitle(_translate("DlgEditPostgisConnection", "Dialog"))
        self.btnCancel.setText(_translate("DlgEditPostgisConnection", "Cancel"))
        self.btnSave.setText(_translate("DlgEditPostgisConnection", "Save"))
        self.Connection.setTitle(_translate("DlgEditPostgisConnection", "GroupBox"))
        self.lblpgHost.setText(_translate("DlgEditPostgisConnection", "Host"))
        self.lblpgUsername.setText(_translate("DlgEditPostgisConnection", "Username"))
        self.lblpgPort.setText(_translate("DlgEditPostgisConnection", "Port"))
        self.lblpgDatabase.setText(_translate("DlgEditPostgisConnection", "Database"))
        self.lblpgPassword.setText(_translate("DlgEditPostgisConnection", "Password"))
        self.lblpgName.setText(_translate("DlgEditPostgisConnection", "Name"))
        self.chkpgStorePassword.setText(_translate("DlgEditPostgisConnection", "Save Password"))
