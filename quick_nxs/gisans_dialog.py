# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/gisans_dialog.ui'
#
# Created: Tue Feb 19 15:37:13 2013
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
    Dialog.resize(600, 600)
    self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
    self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
    self.splitter = QtGui.QSplitter(Dialog)
    self.splitter.setOrientation(QtCore.Qt.Vertical)
    self.splitter.setObjectName(_fromUtf8("splitter"))
    self.widget_3 = QtGui.QWidget(self.splitter)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(2)
    sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
    self.widget_3.setSizePolicy(sizePolicy)
    self.widget_3.setObjectName(_fromUtf8("widget_3"))
    self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_3)
    self.horizontalLayout_2.setMargin(0)
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    self.verticalLayout_5 = QtGui.QVBoxLayout()
    self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
    self.label_9 = QtGui.QLabel(self.widget_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
    self.label_9.setSizePolicy(sizePolicy)
    self.label_9.setAlignment(QtCore.Qt.AlignCenter)
    self.label_9.setObjectName(_fromUtf8("label_9"))
    self.verticalLayout_5.addWidget(self.label_9)
    self.widget_4 = QtGui.QWidget(self.widget_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
    self.widget_4.setSizePolicy(sizePolicy)
    self.widget_4.setObjectName(_fromUtf8("widget_4"))
    self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_4)
    self.horizontalLayout_3.setMargin(0)
    self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
    self.label_11 = QtGui.QLabel(self.widget_4)
    self.label_11.setObjectName(_fromUtf8("label_11"))
    self.horizontalLayout_3.addWidget(self.label_11)
    self.iMax = QtGui.QDoubleSpinBox(self.widget_4)
    self.iMax.setMinimum(-30.0)
    self.iMax.setMaximum(30.0)
    self.iMax.setSingleStep(0.05)
    self.iMax.setObjectName(_fromUtf8("iMax"))
    self.horizontalLayout_3.addWidget(self.iMax)
    self.verticalLayout_5.addWidget(self.widget_4)
    self.label_10 = QtGui.QLabel(self.widget_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
    self.label_10.setSizePolicy(sizePolicy)
    self.label_10.setAlignment(QtCore.Qt.AlignCenter)
    self.label_10.setObjectName(_fromUtf8("label_10"))
    self.verticalLayout_5.addWidget(self.label_10)
    self.widget_5 = QtGui.QWidget(self.widget_3)
    self.widget_5.setObjectName(_fromUtf8("widget_5"))
    self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget_5)
    self.horizontalLayout_4.setMargin(0)
    self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
    self.label_12 = QtGui.QLabel(self.widget_5)
    self.label_12.setObjectName(_fromUtf8("label_12"))
    self.horizontalLayout_4.addWidget(self.label_12)
    self.iMin = QtGui.QDoubleSpinBox(self.widget_5)
    self.iMin.setMinimum(-30.0)
    self.iMin.setMaximum(30.0)
    self.iMin.setSingleStep(0.05)
    self.iMin.setProperty("value", -6.0)
    self.iMin.setObjectName(_fromUtf8("iMin"))
    self.horizontalLayout_4.addWidget(self.iMin)
    self.verticalLayout_5.addWidget(self.widget_5)
    self.plotShowList = QtGui.QListWidget(self.widget_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.plotShowList.sizePolicy().hasHeightForWidth())
    self.plotShowList.setSizePolicy(sizePolicy)
    self.plotShowList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self.plotShowList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    self.plotShowList.setProperty("showDropIndicator", False)
    self.plotShowList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    self.plotShowList.setObjectName(_fromUtf8("plotShowList"))
    self.verticalLayout_5.addWidget(self.plotShowList)
    self.horizontalLayout_2.addLayout(self.verticalLayout_5)
    self.scrollArea = QtGui.QScrollArea(self.widget_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(2)
    sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
    self.scrollArea.setSizePolicy(sizePolicy)
    self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
    self.resultImageArea = QtGui.QWidget()
    self.resultImageArea.setGeometry(QtCore.QRect(0, 0, 476, 287))
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.resultImageArea.sizePolicy().hasHeightForWidth())
    self.resultImageArea.setSizePolicy(sizePolicy)
    self.resultImageArea.setObjectName(_fromUtf8("resultImageArea"))
    self.verticalLayout_4 = QtGui.QVBoxLayout(self.resultImageArea)
    self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
    self.resultImageLayout = QtGui.QHBoxLayout()
    self.resultImageLayout.setObjectName(_fromUtf8("resultImageLayout"))
    self.verticalLayout_4.addLayout(self.resultImageLayout)
    self.scrollArea.setWidget(self.resultImageArea)
    self.horizontalLayout_2.addWidget(self.scrollArea)
    self.widget_2 = QtGui.QWidget(self.splitter)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
    self.widget_2.setSizePolicy(sizePolicy)
    self.widget_2.setObjectName(_fromUtf8("widget_2"))
    self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
    self.horizontalLayout.setMargin(0)
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    self.frame = QtGui.QFrame(self.widget_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(2)
    sizePolicy.setVerticalStretch(1)
    sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
    self.frame.setSizePolicy(sizePolicy)
    self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
    self.frame.setFrameShadow(QtGui.QFrame.Raised)
    self.frame.setObjectName(_fromUtf8("frame"))
    self.verticalLayout = QtGui.QVBoxLayout(self.frame)
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.lambdaPlot = MPLWidget(self.frame)
    self.lambdaPlot.setObjectName(_fromUtf8("lambdaPlot"))
    self.verticalLayout.addWidget(self.lambdaPlot)
    self.horizontalLayout.addWidget(self.frame)
    self.verticalWidget = QtGui.QWidget(self.widget_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
    self.verticalWidget.setSizePolicy(sizePolicy)
    self.verticalWidget.setObjectName(_fromUtf8("verticalWidget"))
    self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalWidget)
    self.verticalLayout_3.setMargin(0)
    self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
    self.widget = QtGui.QWidget(self.verticalWidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
    self.widget.setSizePolicy(sizePolicy)
    self.widget.setObjectName(_fromUtf8("widget"))
    self.gridLayout = QtGui.QGridLayout(self.widget)
    self.gridLayout.setMargin(0)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.numberSlices = QtGui.QSpinBox(self.widget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.numberSlices.sizePolicy().hasHeightForWidth())
    self.numberSlices.setSizePolicy(sizePolicy)
    self.numberSlices.setMinimum(1)
    self.numberSlices.setMaximum(50)
    self.numberSlices.setProperty("value", 4)
    self.numberSlices.setObjectName(_fromUtf8("numberSlices"))
    self.gridLayout.addWidget(self.numberSlices, 5, 3, 1, 1)
    self.label_3 = QtGui.QLabel(self.widget)
    self.label_3.setObjectName(_fromUtf8("label_3"))
    self.gridLayout.addWidget(self.label_3, 3, 4, 1, 1)
    self.label_7 = QtGui.QLabel(self.widget)
    self.label_7.setObjectName(_fromUtf8("label_7"))
    self.gridLayout.addWidget(self.label_7, 0, 2, 1, 1)
    self.projectionMethod = QtGui.QComboBox(self.widget)
    self.projectionMethod.setObjectName(_fromUtf8("projectionMethod"))
    self.projectionMethod.addItem(_fromUtf8(""))
    self.gridLayout.addWidget(self.projectionMethod, 6, 3, 1, 2)
    self.lambdaMin = QtGui.QDoubleSpinBox(self.widget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lambdaMin.sizePolicy().hasHeightForWidth())
    self.lambdaMin.setSizePolicy(sizePolicy)
    self.lambdaMin.setDecimals(3)
    self.lambdaMin.setMinimum(1.9)
    self.lambdaMin.setMaximum(9.0)
    self.lambdaMin.setSingleStep(0.025)
    self.lambdaMin.setProperty("value", 2.0)
    self.lambdaMin.setObjectName(_fromUtf8("lambdaMin"))
    self.gridLayout.addWidget(self.lambdaMin, 3, 3, 1, 1)
    self.label_2 = QtGui.QLabel(self.widget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
    self.label_2.setSizePolicy(sizePolicy)
    self.label_2.setObjectName(_fromUtf8("label_2"))
    self.gridLayout.addWidget(self.label_2, 4, 2, 1, 1)
    self.label = QtGui.QLabel(self.widget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
    self.label.setSizePolicy(sizePolicy)
    self.label.setObjectName(_fromUtf8("label"))
    self.gridLayout.addWidget(self.label, 3, 2, 1, 1)
    spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout.addItem(spacerItem, 7, 3, 1, 1)
    self.label_5 = QtGui.QLabel(self.widget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
    self.label_5.setSizePolicy(sizePolicy)
    self.label_5.setObjectName(_fromUtf8("label_5"))
    self.gridLayout.addWidget(self.label_5, 5, 2, 1, 1)
    self.label_4 = QtGui.QLabel(self.widget)
    self.label_4.setObjectName(_fromUtf8("label_4"))
    self.gridLayout.addWidget(self.label_4, 4, 4, 1, 1)
    self.lambdaMax = QtGui.QDoubleSpinBox(self.widget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lambdaMax.sizePolicy().hasHeightForWidth())
    self.lambdaMax.setSizePolicy(sizePolicy)
    self.lambdaMax.setDecimals(3)
    self.lambdaMax.setMinimum(1.9)
    self.lambdaMax.setMaximum(9.0)
    self.lambdaMax.setSingleStep(0.025)
    self.lambdaMax.setProperty("value", 5.0)
    self.lambdaMax.setObjectName(_fromUtf8("lambdaMax"))
    self.gridLayout.addWidget(self.lambdaMax, 4, 3, 1, 1)
    self.label_6 = QtGui.QLabel(self.widget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
    self.label_6.setSizePolicy(sizePolicy)
    self.label_6.setObjectName(_fromUtf8("label_6"))
    self.gridLayout.addWidget(self.label_6, 6, 2, 1, 1)
    self.pushButton = QtGui.QPushButton(self.widget)
    self.pushButton.setObjectName(_fromUtf8("pushButton"))
    self.gridLayout.addWidget(self.pushButton, 7, 2, 1, 1)
    self.line = QtGui.QFrame(self.widget)
    self.line.setFrameShape(QtGui.QFrame.HLine)
    self.line.setFrameShadow(QtGui.QFrame.Sunken)
    self.line.setObjectName(_fromUtf8("line"))
    self.gridLayout.addWidget(self.line, 2, 2, 1, 1)
    self.label_8 = QtGui.QLabel(self.widget)
    self.label_8.setObjectName(_fromUtf8("label_8"))
    self.gridLayout.addWidget(self.label_8, 1, 2, 1, 1)
    self.gridQy = QtGui.QSpinBox(self.widget)
    self.gridQy.setMinimum(20)
    self.gridQy.setMaximum(300)
    self.gridQy.setSingleStep(10)
    self.gridQy.setProperty("value", 50)
    self.gridQy.setObjectName(_fromUtf8("gridQy"))
    self.gridLayout.addWidget(self.gridQy, 0, 3, 1, 1)
    self.gridQz = QtGui.QSpinBox(self.widget)
    self.gridQz.setMinimum(20)
    self.gridQz.setMaximum(300)
    self.gridQz.setSingleStep(10)
    self.gridQz.setProperty("value", 50)
    self.gridQz.setObjectName(_fromUtf8("gridQz"))
    self.gridLayout.addWidget(self.gridQz, 1, 3, 1, 1)
    self.verticalLayout_3.addWidget(self.widget)
    self.buttonBox = QtGui.QDialogButtonBox(self.verticalWidget)
    self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
    self.verticalLayout_3.addWidget(self.buttonBox)
    self.horizontalLayout.addWidget(self.verticalWidget)
    self.verticalLayout_2.addWidget(self.splitter)

    self.retranslateUi(Dialog)
    QtCore.QObject.connect(self.lambdaMin, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.lambdaRangeChanged)
    QtCore.QObject.connect(self.lambdaMax, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.lambdaRangeChanged)
    QtCore.QObject.connect(self.numberSlices, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), Dialog.numberSlicesChanged)
    QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("pressed()")), Dialog.createProjectionPlots)
    QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
    QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
    QtCore.QObject.connect(self.plotShowList, QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")), Dialog.changePlotSelection)
    QtCore.QObject.connect(self.iMin, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.changePlotScale)
    QtCore.QObject.connect(self.iMax, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.changePlotScale)
    QtCore.QMetaObject.connectSlotsByName(Dialog)

  def retranslateUi(self, Dialog):
    Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
    self.label_9.setText(QtGui.QApplication.translate("Dialog", "I-Max", None, QtGui.QApplication.UnicodeUTF8))
    self.label_11.setText(QtGui.QApplication.translate("Dialog", "10^", None, QtGui.QApplication.UnicodeUTF8))
    self.label_10.setText(QtGui.QApplication.translate("Dialog", "I-Min", None, QtGui.QApplication.UnicodeUTF8))
    self.label_12.setText(QtGui.QApplication.translate("Dialog", "10^", None, QtGui.QApplication.UnicodeUTF8))
    self.label_3.setText(QtGui.QApplication.translate("Dialog", "Å", None, QtGui.QApplication.UnicodeUTF8))
    self.label_7.setText(QtGui.QApplication.translate("Dialog", "Grid Points Qy", None, QtGui.QApplication.UnicodeUTF8))
    self.projectionMethod.setItemText(0, QtGui.QApplication.translate("Dialog", "Binning", None, QtGui.QApplication.UnicodeUTF8))
    self.label_2.setText(QtGui.QApplication.translate("Dialog", "λ-Max", None, QtGui.QApplication.UnicodeUTF8))
    self.label.setText(QtGui.QApplication.translate("Dialog", "λ-Min", None, QtGui.QApplication.UnicodeUTF8))
    self.label_5.setText(QtGui.QApplication.translate("Dialog", "No. of Slices", None, QtGui.QApplication.UnicodeUTF8))
    self.label_4.setText(QtGui.QApplication.translate("Dialog", "Å", None, QtGui.QApplication.UnicodeUTF8))
    self.label_6.setText(QtGui.QApplication.translate("Dialog", "Projection Method", None, QtGui.QApplication.UnicodeUTF8))
    self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create Preview", None, QtGui.QApplication.UnicodeUTF8))
    self.label_8.setText(QtGui.QApplication.translate("Dialog", "Grid Points Qz", None, QtGui.QApplication.UnicodeUTF8))

from mplwidget import MPLWidget
