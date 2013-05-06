# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer/smooth_dialog.ui'
#
# Created: Mon May  6 16:55:01 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s

class Ui_Dialog(object):
  def setupUi(self, Dialog):
    Dialog.setObjectName(_fromUtf8("Dialog"))
    Dialog.resize(781, 608)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/General/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    Dialog.setWindowIcon(icon)
    self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
    self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
    self.horizontalLayout_2 = QtGui.QHBoxLayout()
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    self.verticalLayout = QtGui.QVBoxLayout()
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.label = QtGui.QLabel(Dialog)
    self.label.setAlignment(QtCore.Qt.AlignCenter)
    self.label.setObjectName(_fromUtf8("label"))
    self.verticalLayout.addWidget(self.label)
    self.horizontalLayout = QtGui.QHBoxLayout()
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    self.kizmkfzVSqz = QtGui.QRadioButton(Dialog)
    self.kizmkfzVSqz.setChecked(True)
    self.kizmkfzVSqz.setObjectName(_fromUtf8("kizmkfzVSqz"))
    self.horizontalLayout.addWidget(self.kizmkfzVSqz)
    self.qxVSqz = QtGui.QRadioButton(Dialog)
    self.qxVSqz.setObjectName(_fromUtf8("qxVSqz"))
    self.horizontalLayout.addWidget(self.qxVSqz)
    self.kizVSkfz = QtGui.QRadioButton(Dialog)
    self.kizVSkfz.setObjectName(_fromUtf8("kizVSkfz"))
    self.horizontalLayout.addWidget(self.kizVSkfz)
    self.verticalLayout.addLayout(self.horizontalLayout)
    self.plot = MPLWidget(Dialog)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
    self.plot.setSizePolicy(sizePolicy)
    self.plot.setObjectName(_fromUtf8("plot"))
    self.verticalLayout.addWidget(self.plot)
    self.horizontalLayout_2.addLayout(self.verticalLayout)
    self.widget = QtGui.QWidget(Dialog)
    self.widget.setObjectName(_fromUtf8("widget"))
    self.gridLayout = QtGui.QGridLayout(self.widget)
    self.gridLayout.setMargin(0)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.gridXmax = QtGui.QDoubleSpinBox(self.widget)
    self.gridXmax.setDecimals(6)
    self.gridXmax.setMinimum(-1.0)
    self.gridXmax.setMaximum(1.0)
    self.gridXmax.setSingleStep(0.001)
    self.gridXmax.setProperty("value", 0.01)
    self.gridXmax.setObjectName(_fromUtf8("gridXmax"))
    self.gridLayout.addWidget(self.gridXmax, 2, 3, 1, 1)
    self.sigmasCoupled = QtGui.QToolButton(self.widget)
    icon = QtGui.QIcon.fromTheme(_fromUtf8("system-lock-screen"))
    self.sigmasCoupled.setIcon(icon)
    self.sigmasCoupled.setCheckable(True)
    self.sigmasCoupled.setChecked(True)
    self.sigmasCoupled.setObjectName(_fromUtf8("sigmasCoupled"))
    self.gridLayout.addWidget(self.sigmasCoupled, 12, 0, 1, 1)
    spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
    self.gridLayout.addItem(spacerItem, 5, 3, 1, 1)
    self.sigmaY = QtGui.QDoubleSpinBox(self.widget)
    self.sigmaY.setEnabled(False)
    self.sigmaY.setDecimals(6)
    self.sigmaY.setMinimum(1e-06)
    self.sigmaY.setMaximum(1.0)
    self.sigmaY.setSingleStep(0.00025)
    self.sigmaY.setProperty("value", 0.0005)
    self.sigmaY.setObjectName(_fromUtf8("sigmaY"))
    self.gridLayout.addWidget(self.sigmaY, 12, 3, 1, 1)
    self.label_12 = QtGui.QLabel(self.widget)
    self.label_12.setObjectName(_fromUtf8("label_12"))
    self.gridLayout.addWidget(self.label_12, 4, 2, 1, 1)
    self.label_10 = QtGui.QLabel(self.widget)
    self.label_10.setObjectName(_fromUtf8("label_10"))
    self.gridLayout.addWidget(self.label_10, 2, 2, 1, 1)
    self.label_2 = QtGui.QLabel(self.widget)
    self.label_2.setObjectName(_fromUtf8("label_2"))
    self.gridLayout.addWidget(self.label_2, 10, 0, 1, 1)
    self.label_11 = QtGui.QLabel(self.widget)
    self.label_11.setObjectName(_fromUtf8("label_11"))
    self.gridLayout.addWidget(self.label_11, 3, 2, 1, 1)
    spacerItem1 = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
    self.gridLayout.addItem(spacerItem1, 13, 3, 1, 1)
    self.buttonBox = QtGui.QDialogButtonBox(self.widget)
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
    self.gridLayout.addWidget(self.buttonBox, 16, 0, 1, 4)
    self.label_8 = QtGui.QLabel(self.widget)
    self.label_8.setObjectName(_fromUtf8("label_8"))
    self.gridLayout.addWidget(self.label_8, 12, 2, 1, 1)
    self.label_5 = QtGui.QLabel(self.widget)
    self.label_5.setObjectName(_fromUtf8("label_5"))
    self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
    self.label_7 = QtGui.QLabel(self.widget)
    self.label_7.setObjectName(_fromUtf8("label_7"))
    self.gridLayout.addWidget(self.label_7, 10, 2, 1, 1)
    self.gridYmin = QtGui.QDoubleSpinBox(self.widget)
    self.gridYmin.setDecimals(6)
    self.gridYmin.setMinimum(-1.0)
    self.gridYmin.setMaximum(1.0)
    self.gridYmin.setSingleStep(0.001)
    self.gridYmin.setObjectName(_fromUtf8("gridYmin"))
    self.gridLayout.addWidget(self.gridYmin, 3, 3, 1, 1)
    spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
    self.gridLayout.addItem(spacerItem2, 9, 3, 1, 1)
    self.label_13 = QtGui.QLabel(self.widget)
    self.label_13.setAlignment(QtCore.Qt.AlignCenter)
    self.label_13.setObjectName(_fromUtf8("label_13"))
    self.gridLayout.addWidget(self.label_13, 0, 0, 1, 4)
    self.label_9 = QtGui.QLabel(self.widget)
    self.label_9.setObjectName(_fromUtf8("label_9"))
    self.gridLayout.addWidget(self.label_9, 1, 2, 1, 1)
    self.gridYmax = QtGui.QDoubleSpinBox(self.widget)
    self.gridYmax.setDecimals(6)
    self.gridYmax.setMinimum(-1.0)
    self.gridYmax.setMaximum(1.0)
    self.gridYmax.setSingleStep(0.001)
    self.gridYmax.setProperty("value", 0.025)
    self.gridYmax.setObjectName(_fromUtf8("gridYmax"))
    self.gridLayout.addWidget(self.gridYmax, 4, 3, 1, 1)
    self.gridSizeCoupled = QtGui.QToolButton(self.widget)
    icon = QtGui.QIcon.fromTheme(_fromUtf8("system-lock-screen"))
    self.gridSizeCoupled.setIcon(icon)
    self.gridSizeCoupled.setCheckable(True)
    self.gridSizeCoupled.setChecked(True)
    self.gridSizeCoupled.setObjectName(_fromUtf8("gridSizeCoupled"))
    self.gridLayout.addWidget(self.gridSizeCoupled, 8, 0, 1, 1)
    self.label_3 = QtGui.QLabel(self.widget)
    self.label_3.setObjectName(_fromUtf8("label_3"))
    self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
    self.label_4 = QtGui.QLabel(self.widget)
    self.label_4.setObjectName(_fromUtf8("label_4"))
    self.gridLayout.addWidget(self.label_4, 8, 2, 1, 1)
    self.gridSizeX = QtGui.QSpinBox(self.widget)
    self.gridSizeX.setEnabled(False)
    self.gridSizeX.setMinimum(10)
    self.gridSizeX.setMaximum(1000)
    self.gridSizeX.setSingleStep(10)
    self.gridSizeX.setProperty("value", 200)
    self.gridSizeX.setObjectName(_fromUtf8("gridSizeX"))
    self.gridLayout.addWidget(self.gridSizeX, 6, 3, 1, 1)
    self.gridXmin = QtGui.QDoubleSpinBox(self.widget)
    self.gridXmin.setDecimals(6)
    self.gridXmin.setMinimum(-1.0)
    self.gridXmin.setMaximum(1.0)
    self.gridXmin.setSingleStep(0.001)
    self.gridXmin.setProperty("value", -0.01)
    self.gridXmin.setObjectName(_fromUtf8("gridXmin"))
    self.gridLayout.addWidget(self.gridXmin, 1, 3, 1, 1)
    self.label_6 = QtGui.QLabel(self.widget)
    self.label_6.setObjectName(_fromUtf8("label_6"))
    self.gridLayout.addWidget(self.label_6, 6, 2, 1, 1)
    self.sigmaX = QtGui.QDoubleSpinBox(self.widget)
    self.sigmaX.setDecimals(6)
    self.sigmaX.setMinimum(1e-06)
    self.sigmaX.setMaximum(1.0)
    self.sigmaX.setSingleStep(0.00025)
    self.sigmaX.setProperty("value", 0.0005)
    self.sigmaX.setObjectName(_fromUtf8("sigmaX"))
    self.gridLayout.addWidget(self.sigmaX, 10, 3, 1, 1)
    spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout.addItem(spacerItem3, 15, 3, 1, 1)
    self.gridSizeY = QtGui.QSpinBox(self.widget)
    self.gridSizeY.setEnabled(False)
    self.gridSizeY.setMinimum(10)
    self.gridSizeY.setMaximum(1000)
    self.gridSizeY.setSingleStep(10)
    self.gridSizeY.setProperty("value", 200)
    self.gridSizeY.setObjectName(_fromUtf8("gridSizeY"))
    self.gridLayout.addWidget(self.gridSizeY, 8, 3, 1, 1)
    self.label_14 = QtGui.QLabel(self.widget)
    self.label_14.setObjectName(_fromUtf8("label_14"))
    self.gridLayout.addWidget(self.label_14, 14, 0, 1, 1)
    self.rSigmas = QtGui.QDoubleSpinBox(self.widget)
    self.rSigmas.setMinimum(1.0)
    self.rSigmas.setMaximum(10.0)
    self.rSigmas.setProperty("value", 3.0)
    self.rSigmas.setObjectName(_fromUtf8("rSigmas"))
    self.gridLayout.addWidget(self.rSigmas, 14, 3, 1, 1)
    self.horizontalLayout_2.addWidget(self.widget)
    self.verticalLayout_2.addLayout(self.horizontalLayout_2)

    self.retranslateUi(Dialog)
    QtCore.QObject.connect(self.kizmkfzVSqz, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.drawPlot)
    QtCore.QObject.connect(self.kizVSkfz, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.drawPlot)
    QtCore.QObject.connect(self.qxVSqz, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.drawPlot)
    QtCore.QObject.connect(self.gridSizeCoupled, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.gridSizeY.setDisabled)
    QtCore.QObject.connect(self.sigmasCoupled, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.sigmaY.setDisabled)
    QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
    QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
    QtCore.QObject.connect(self.gridXmin, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.updateSettings)
    QtCore.QObject.connect(self.gridXmax, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.updateSettings)
    QtCore.QObject.connect(self.gridYmin, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.updateSettings)
    QtCore.QObject.connect(self.gridYmax, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.updateSettings)
    QtCore.QObject.connect(self.sigmaX, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.updateSettings)
    QtCore.QObject.connect(self.sigmaY, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.updateSettings)
    QtCore.QObject.connect(self.gridSizeCoupled, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.updateGrid)
    QtCore.QObject.connect(self.sigmasCoupled, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.updateSettings)
    QtCore.QObject.connect(self.gridSizeCoupled, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.gridSizeX.setDisabled)
    QtCore.QMetaObject.connectSlotsByName(Dialog)
    Dialog.setTabOrder(self.gridXmin, self.gridXmax)
    Dialog.setTabOrder(self.gridXmax, self.gridYmin)
    Dialog.setTabOrder(self.gridYmin, self.gridYmax)
    Dialog.setTabOrder(self.gridYmax, self.gridSizeX)
    Dialog.setTabOrder(self.gridSizeX, self.gridSizeY)
    Dialog.setTabOrder(self.gridSizeY, self.sigmaX)
    Dialog.setTabOrder(self.sigmaX, self.sigmaY)
    Dialog.setTabOrder(self.sigmaY, self.rSigmas)
    Dialog.setTabOrder(self.rSigmas, self.buttonBox)
    Dialog.setTabOrder(self.buttonBox, self.kizmkfzVSqz)
    Dialog.setTabOrder(self.kizmkfzVSqz, self.qxVSqz)
    Dialog.setTabOrder(self.qxVSqz, self.kizVSkfz)
    Dialog.setTabOrder(self.kizVSkfz, self.gridSizeCoupled)
    Dialog.setTabOrder(self.gridSizeCoupled, self.sigmasCoupled)

  def retranslateUi(self, Dialog):
    Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Smooth Off-Specular", None, QtGui.QApplication.UnicodeUTF8))
    self.label.setText(QtGui.QApplication.translate("Dialog", "Off-Specular Preview", None, QtGui.QApplication.UnicodeUTF8))
    self.kizmkfzVSqz.setText(QtGui.QApplication.translate("Dialog", "(ki_z-kf_z) VS. Qz", None, QtGui.QApplication.UnicodeUTF8))
    self.qxVSqz.setText(QtGui.QApplication.translate("Dialog", "Qx VS. Qz", None, QtGui.QApplication.UnicodeUTF8))
    self.kizVSkfz.setText(QtGui.QApplication.translate("Dialog", "ki_z VS. kf_z", None, QtGui.QApplication.UnicodeUTF8))
    self.label_12.setText(QtGui.QApplication.translate("Dialog", "Y2", None, QtGui.QApplication.UnicodeUTF8))
    self.label_10.setText(QtGui.QApplication.translate("Dialog", "X2", None, QtGui.QApplication.UnicodeUTF8))
    self.label_2.setText(QtGui.QApplication.translate("Dialog", "Sigma", None, QtGui.QApplication.UnicodeUTF8))
    self.label_11.setText(QtGui.QApplication.translate("Dialog", "Y1", None, QtGui.QApplication.UnicodeUTF8))
    self.label_8.setText(QtGui.QApplication.translate("Dialog", "Y", None, QtGui.QApplication.UnicodeUTF8))
    self.label_5.setText(QtGui.QApplication.translate("Dialog", "Grid Region", None, QtGui.QApplication.UnicodeUTF8))
    self.label_7.setText(QtGui.QApplication.translate("Dialog", "X", None, QtGui.QApplication.UnicodeUTF8))
    self.label_13.setText(QtGui.QApplication.translate("Dialog", "Smoothing Parameters", None, QtGui.QApplication.UnicodeUTF8))
    self.label_9.setText(QtGui.QApplication.translate("Dialog", "X1", None, QtGui.QApplication.UnicodeUTF8))
    self.label_3.setText(QtGui.QApplication.translate("Dialog", "Grid Size", None, QtGui.QApplication.UnicodeUTF8))
    self.label_4.setText(QtGui.QApplication.translate("Dialog", "Y", None, QtGui.QApplication.UnicodeUTF8))
    self.label_6.setText(QtGui.QApplication.translate("Dialog", "X", None, QtGui.QApplication.UnicodeUTF8))
    self.label_14.setText(QtGui.QApplication.translate("Dialog", "R [Sigmas]", None, QtGui.QApplication.UnicodeUTF8))

from .mplwidget import MPLWidget
from . import icons_rc
